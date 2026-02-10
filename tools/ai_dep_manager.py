import os
import sys
import ast
import re
import json
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

def _read_text(p):
    try:
        return Path(p).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def _list_py_files(root):
    files = []
    for base, dirs, names in os.walk(root):
        dn = os.path.basename(base).lower()
        if dn in {"venv", ".venv", "__pycache__", ".git"}:
            continue
        if "site-packages" in base.replace("\\", "/"):
            continue
        for n in names:
            if n.endswith(".py"):
                files.append(os.path.join(base, n))
    return files

def scan_imports(root):
    mods = set()
    for f in _list_py_files(root):
        src = _read_text(f)
        if not src:
            continue
        try:
            t = ast.parse(src)
        except Exception:
            continue
        for n in ast.walk(t):
            if isinstance(n, ast.Import):
                for a in n.names:
                    mods.add(a.name.split(".")[0])
            elif isinstance(n, ast.ImportFrom):
                if n.module:
                    mods.add(n.module.split(".")[0])
    return sorted(mods)

_pkg_map = {
    "bs4": "beautifulsoup4",
    "sklearn": "scikit-learn",
    "PIL": "pillow",
    "yaml": "pyyaml",
    "Crypto": "pycryptodome",
    "cv2": "opencv-python",
    "tensorflow_gpu": "tensorflow",
    "torchvision": "torchvision",
    "IPython": "ipython",
    "jinja2": "Jinja2",
}

def module_to_package(m):
    return _pkg_map.get(m, m)

def _http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "ppmm-ai/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def _http_post_json(url, payload, timeout=15):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "ppmm-ai/1.0", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def pypi_json(pkg):
    u = "https://pypi.org/pypi/{}/json".format(urllib.parse.quote(pkg))
    try:
        b = _http_get(u)
        return json.loads(b.decode("utf-8"))
    except Exception:
        return None

def versions_for(pkg):
    d = pypi_json(pkg)
    if not d:
        return []
    rel = d.get("releases", {})
    vs = sorted(rel.keys(), key=lambda x: _version_key(x))
    return vs

def latest_for(pkg):
    d = pypi_json(pkg)
    if not d:
        return None
    i = d.get("info", {})
    v = i.get("version")
    return v

def _version_key(v):
    m = re.match(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?", v)
    if not m:
        return (0, 0, 0, v)
    a = [int(x) if x is not None else 0 for x in m.groups()]
    return (a[0], a[1], a[2], v)

def parse_requires_dist(s):
    m = re.match(r"^\s*([A-Za-z0-9_.+-]+)\s*(\(([^)]+)\))?\s*$", s or "")
    if not m:
        return None, []
    name = m.group(1)
    specs = []
    if m.group(3):
        parts = [x.strip() for x in m.group(3).split(",")]
        for p in parts:
            mm = re.match(r"^(==|>=|<=|>|<|~=)\s*([A-Za-z0-9_.+-]+)$", p)
            if mm:
                specs.append((mm.group(1), mm.group(2)))
    return name, specs

def requires_for_version(pkg, ver):
    d = pypi_json(pkg)
    if not d:
        return []
    info = d.get("info", {})
    if info.get("version") == ver and info.get("requires_dist"):
        return info.get("requires_dist") or []
    rel = d.get("releases", {}).get(ver, [])
    if rel and isinstance(rel, list):
        md = d.get("info", {}).get("requires_dist") or []
        return md
    return info.get("requires_dist") or []

def spec_satisfies(ver, op, target):
    a = _version_key(ver)
    b = _version_key(target)
    if op == "==":
        return ver == target
    if op == ">=":
        return a >= b
    if op == "<=":
        return a <= b
    if op == ">":
        return a > b
    if op == "<":
        return a < b
    if op == "~=":
        aa = _version_key(ver)
        bb = _version_key(target)
        return aa[0] == bb[0] and aa >= bb
    return True

def check_compatibility(pkg, ver, current):
    reqs = requires_for_version(pkg, ver)
    conflicts = []
    for r in reqs or []:
        name, specs = parse_requires_dist(r)
        if not name:
            continue
        cur = current.get(name)
        if not cur:
            continue
        ok = True
        for op, tgt in specs:
            if not spec_satisfies(cur, op, tgt):
                ok = False
                break
        if not ok:
            conflicts.append({"dep": name, "current": cur, "required": specs})
    return conflicts

def suggest_resolutions(conflicts, current):
    out = []
    for c in conflicts:
        dep = c["dep"]
        vs = versions_for(dep)
        best = None
        for v in reversed(vs):
            ok = True
            for op, tgt in c["required"]:
                if not spec_satisfies(v, op, tgt):
                    ok = False
                    break
            if ok:
                best = v
                break
        if best:
            out.append({"package": dep, "suggested": best})
        else:
            out.append({"package": dep, "suggested": None})
    return out

def read_project_packages(root):
    conf = os.path.join(root, "project.toml")
    pkgs = {}
    if os.path.exists(conf):
        txt = _read_text(conf)
        insec = False
        for ln in txt.splitlines():
            s = ln.strip()
            if s.startswith("[") and s.endswith("]"):
                insec = s.lower() == "[packages]"
                continue
            if insec and "=" in s:
                k, v = s.split("=", 1)
                name = k.strip()
                val = v.strip().strip('"').strip("'")
                if val:
                    pkgs[name] = val
    req = os.path.join(root, "requirements.txt")
    if os.path.exists(req):
        for ln in _read_text(req).splitlines():
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            mm = re.match(r"^([A-Za-z0-9_.+-]+)(?:==([A-Za-z0-9_.+-]+))?", s)
            if mm:
                name = mm.group(1)
                ver = mm.group(2) or ""
                pkgs[name] = ver
    return pkgs

def gen_requirements(root, used):
    lines = []
    for m in used:
        p = module_to_package(m)
        latest = latest_for(p)
        if not latest:
            lines.append(p)
            continue
        mm = re.match(r"^(\d+)\.(\d+)\.(\d+)", latest)
        if not mm:
            lines.append("{}=={}".format(p, latest))
            continue
        major = int(mm.group(1))
        minor = int(mm.group(2))
        next_major = major + 1
        rng = ">={}.{}.0,<{}.0.0".format(major, minor, next_major)
        lines.append("{} ({})".format(p, rng))
    Path(os.path.join(root, "requirements.txt")).write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path(os.path.join(root, "requirements-dev.txt")).write_text("\n".join(sorted(lines)) + "\n", encoding="utf-8")
    return lines

def health_dashboard(root, current):
    rows = []
    for p, v in sorted(current.items()):
        latest = latest_for(p) or ""
        up = ""
        if latest and v and _version_key(latest) > _version_key(v):
            up = "outdated"
        vc = osv_vuln_count(p)
        rows.append({"package": p, "current": v, "latest": latest, "status": up, "vulns": vc})
    md = ["# Dependency Health", "", "| Package | Current | Latest | Status | Vulns |", "|---|---|---|---|---|"]
    for r in rows:
        md.append("| {} | {} | {} | {} | {} |".format(r["package"], r["current"], r["latest"], r["status"], r["vulns"]))
    Path(os.path.join(root, "dependency-health.md")).write_text("\n".join(md) + "\n", encoding="utf-8")
    return rows

def osv_vuln_count(pkg):
    try:
        resp = _http_post_json("https://api.osv.dev/v1/query", {"package": {"name": pkg, "ecosystem": "PyPI"}})
        vs = resp.get("vulns") or []
        return len(vs)
    except Exception:
        return 0

def find_impacted_files_pandas(root):
    files = []
    patt = re.compile(r"\bDataFrame\.append\s*\(")
    patt2 = re.compile(r"\.append\s*\(")
    for f in _list_py_files(root):
        txt = _read_text(f)
        if not txt:
            continue
        if "import pandas" not in txt and "from pandas" not in txt:
            continue
        if patt.search(txt) or patt2.search(txt):
            files.append(f)
    return files

def upgrade_assistant(root, pkg):
    current = read_project_packages(root)
    target_latest = latest_for(pkg)
    if not target_latest:
        print("Package not found")
        return 1
    conflicts = check_compatibility(pkg, target_latest, current)
    res = suggest_resolutions(conflicts, current)
    print("AI Analysis:")
    print("✓ {} upgrade target {}".format(pkg, target_latest))
    if conflicts:
        for c in conflicts:
            reqs = ", ".join(["{}{}".format(op, tgt) for op, tgt in c["required"]])
            print("⚠ {} requires {} while current is {}".format(c["dep"], reqs, c["current"]))
    if pkg.lower() == "pandas":
        files = find_impacted_files_pandas(root)
        if files:
            print("❌ Breaking change: DataFrame.append removed")
            print("Impact: {} files".format(len(files)))
            print("Files: {}".format(", ".join(files)))
    if res:
        print("Resolution suggestions:")
        for r in res:
            print("- {} → {}".format(r["package"], r["suggested"] or "manual review"))
    return 0

def auto_resolve(root, pkg):
    current = read_project_packages(root)
    target_latest = latest_for(pkg)
    if not target_latest:
        print("Package not found")
        return 1
    conflicts = check_compatibility(pkg, target_latest, current)
    res = suggest_resolutions(conflicts, current)
    new = dict(current)
    new[pkg] = target_latest
    for r in res:
        if r["suggested"]:
            new[r["package"]] = r["suggested"]
    lines = []
    for k, v in sorted(new.items()):
        if v:
            lines.append("{}=={}".format(k, v))
        else:
            lines.append(k)
    Path(os.path.join(root, "requirements-resolved.txt")).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote requirements-resolved.txt")
    return 0

def analyze_cmd(args):
    root = os.path.abspath(args.path or ".")
    mods = scan_imports(root)
    pkgs = [module_to_package(m) for m in mods]
    print("Detected packages:")
    for p in pkgs:
        print(p)
    return 0

def gen_cmd(args):
    root = os.path.abspath(args.path or ".")
    used = scan_imports(root)
    lines = gen_requirements(root, used)
    print("Generated requirements files")
    return 0

def dashboard_cmd(args):
    root = os.path.abspath(args.path or ".")
    current = read_project_packages(root)
    rows = health_dashboard(root, current)
    print("Wrote dependency-health.md")
    return 0

def upgrade_cmd(args):
    root = os.path.abspath(args.path or ".")
    return upgrade_assistant(root, args.package)

def resolve_cmd(args):
    root = os.path.abspath(args.path or ".")
    return auto_resolve(root, args.package)

def main():
    ap = argparse.ArgumentParser(prog="ppmm-ai")
    sub = ap.add_subparsers(dest="cmd")
    a1 = sub.add_parser("analyze")
    a1.add_argument("--path", default=".")
    a1.set_defaults(func=analyze_cmd)
    a2 = sub.add_parser("gen")
    a2.add_argument("--path", default=".")
    a2.set_defaults(func=gen_cmd)
    a3 = sub.add_parser("dashboard")
    a3.add_argument("--path", default=".")
    a3.set_defaults(func=dashboard_cmd)
    a4 = sub.add_parser("upgrade")
    a4.add_argument("package")
    a4.add_argument("--path", default=".")
    a4.set_defaults(func=upgrade_cmd)
    a5 = sub.add_parser("resolve")
    a5.add_argument("package")
    a5.add_argument("--path", default=".")
    a5.set_defaults(func=resolve_cmd)
    args = ap.parse_args()
    if not hasattr(args, "func"):
        ap.print_help()
        return 1
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
