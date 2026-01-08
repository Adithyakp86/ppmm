# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          | EOL Date   |
| ------- | ------------------ | ---------- |
| 1.1.x   | :white_check_mark: | TBD        |
| 1.0.x   | :white_check_mark: | 2026-12-31 |
| < 1.0   | :x:                | 2024-12-31 |

- **Current Release:** 1.1.0
- **Previous Release:** 1.0.0-alpha
- **LTS:** Versions 1.0.x and above receive security updates for 12 months

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.** This could allow attackers to exploit the vulnerability before users have a chance to update.

### Responsible Disclosure

If you discover a security vulnerability in PPM, please report it privately to:

📧 **Email:** Check the repository for security contact or open a private discussion

**Include in your report:**
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if any)
- Your contact information

### What to Expect

1. **Acknowledgment** - We will acknowledge receipt within 48 hours
2. **Investigation** - We will investigate and assess severity (2-5 business days)
3. **Communication** - We will keep you updated on our progress
4. **Fix Development** - We will develop and test a fix (7-14 days depending on complexity)
5. **Coordination** - We will coordinate disclosure timing with you
6. **Release** - We will publish a security patch and advisory
7. **Credit** - We will credit you in the security advisory (if desired)

### Severity Levels

We classify vulnerabilities based on impact:

- **Critical** - Unauthorized access, code execution, or data compromise
  - Priority: Immediate patch
  - Disclosure: After patch is released

- **High** - Significant security impact, privilege escalation
  - Priority: 1-2 weeks
  - Disclosure: After patch is released

- **Medium** - Moderate impact, requires specific conditions
  - Priority: 2-4 weeks
  - Disclosure: After patch is released

- **Low** - Minor impact, unlikely to be exploited
  - Priority: Next regular release
  - Disclosure: Can be immediate

## Security Best Practices

### For Users

1. **Keep Updated** - Always use the latest stable version
   ```bash
   ppmm --version  # Check your version
   ```

2. **Secure Your Environment**
   - Don't run PPM with unnecessary privileges
   - Protect your `project.toml` files
   - Keep Python and pip updated

3. **Package Sources**
   - PPM only installs from PyPI (https://pypi.org)
   - Verify package authenticity before installing
   - Use specific version pinning for production

### For Developers

1. **Dependency Management**
   - Run `cargo audit` to check for vulnerable dependencies
   - Keep dependencies updated with `cargo update`
   - Review security advisories in `Cargo.toml`

2. **Code Security**
   - Use `cargo clippy` to catch potential issues
   - Validate all user input
   - Handle errors gracefully
   - Avoid unsafe code unless necessary

3. **Testing**
   - Write security-focused tests
   - Test with untrusted input
   - Verify permission handling

## Known Security Considerations

### Current Limitations

1. **Virtual Environment Trust**
   - PPM trusts the Python installation in the virtual environment
   - Ensure the venv directory is only writable by intended users

2. **Package Installation**
   - PPM installs packages from PyPI without cryptographic verification
   - This is consistent with pip's default behavior
   - PyPI provides transport security via HTTPS

3. **Configuration File**
   - `project.toml` may contain sensitive information
   - Always version control with appropriate `.gitignore` rules
   - Avoid storing secrets in project configuration

### Mitigations

- ✅ Input validation on package names
- ✅ Cross-platform path security
- ✅ Error handling to prevent information disclosure
- ✅ No hardcoded credentials or secrets
- ✅ Use of standard, audited dependencies

## Dependency Security

PPM uses these core dependencies (all well-maintained):

| Dependency | Version | Purpose | Status |
| ---------- | ------- | ------- | ------ |
| clap | 3.2.8 | CLI parsing | Maintained |
| reqwest | 0.13 | HTTP client | Maintained |
| toml | 0.9 | Config parsing | Maintained |
| serde | 1.0 | Serialization | Maintained |
| colored | 3.0.0 | Terminal output | Maintained |

**Audit Status:** Dependencies are regularly checked with `cargo audit` for known vulnerabilities.

## Security Roadmap

- [ ] Configuration encryption support
- [ ] PGP signature verification for packages
- [ ] Vulnerability scanning in CI/CD
- [ ] Security audit by third party
- [ ] SBOM (Software Bill of Materials) generation

## Contact

For security concerns:
- 🔐 Private reports: See "Reporting a Vulnerability" section
- 📋 General questions: Open a [Discussion](https://github.com/Sumangal44/python-project-manager/discussions)
- 🐛 Bug reports: Use [Issues](https://github.com/Sumangal44/python-project-manager/issues) for non-security bugs

## Changelog

### Security Patches

- **1.1.0** - Added package name validation, improved error handling
- **1.0.0-alpha** - Initial security review completed, zero critical issues

---

**Last Updated:** January 2026
**Maintained By:** Sumangal44
