# Contributing to PPMM (Python Project Manager)

Thank you for your interest in contributing to PPM! We welcome contributions from everyone. This guide will help you get started.

## Code of Conduct

Be respectful and constructive in all interactions. We're building an inclusive community.

## Getting Started

### Prerequisites

- **Rust 1.60+** - [Install Rust](https://rustup.rs/)
- **Python 3.7+** - For testing and development
- **Git** - Version control
- **Cargo** - Rust package manager (comes with Rust)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Sumangal44/python-project-manager.git
cd python-project-manager

# Build the project
cargo build

# Run tests
cargo test

# Check code quality
cargo clippy -- -D warnings
cargo fmt --check
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write clean, idiomatic Rust code
- Follow the existing code style
- Add comments for complex logic
- Keep functions focused and small

### 3. Testing

Write tests for new functionality:

```bash
# Run all tests
cargo test

# Run specific test
cargo test test_name

# Run with output
cargo test -- --nocapture
```

### 4. Code Quality Checks

Before committing, ensure code quality:

```bash
# Format code
cargo fmt

# Check formatting
cargo fmt --check

# Run clippy (linter)
cargo clippy -- -D warnings

# Check documentation
cargo doc --no-deps
```

### 5. Commit & Push

```bash
# Commit with descriptive message
git commit -m "feat: add feature description"
# or
git commit -m "fix: resolve issue description"
# or
git commit -m "docs: update documentation"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Open a Pull Request

1. Go to the repository on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template:
   - **Title:** Clear, concise description
   - **Description:** What changes? Why? How?
   - **Fixes:** Reference any related issues (#123)
   - **Testing:** How was this tested?

## Commit Message Conventions

Use conventional commits:

```
type(scope): short description

Optional longer description explaining the changes in detail.

Optional footer with references to issues.
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style (formatting, missing semicolons)
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Test additions/changes
- `chore` - Build, dependencies, CI/CD

**Examples:**
```
feat(cli): add interactive mode for project creation
fix(venv): resolve path issue on Windows
docs(readme): add configuration examples
refactor(core): simplify package manager logic
```

## Code Style Guidelines

### Rust Style

- Use `cargo fmt` for formatting (enforced)
- Follow [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- Write descriptive variable and function names
- Add doc comments for public APIs:

```rust
/// Creates a new Python project with scaffolding.
///
/// # Arguments
/// * `name` - The project name
/// * `version` - Initial version number
///
/// # Returns
/// Result indicating success or error
pub fn create_project(name: &str, version: &str) -> Result<(), String> {
    // Implementation
}
```

### Error Handling

- Prefer `Result<T, String>` for error handling
- Provide clear, actionable error messages
- Use `.map_err()` to add context to errors

```rust
fs::create_dir(path)
    .map_err(|e| format!("Failed to create directory: {}", e))?
```

## Project Structure

```
src/
├── main.rs              # CLI entry point
├── project_managers.rs  # Project creation logic
├── ppm_functions.rs     # Core functionality
├── settings.rs          # Configuration handling
└── utils.rs             # Utility functions
```

## Key Modules

### `main.rs`
- CLI argument parsing with Clap
- Command routing
- Entry point

### `project_managers.rs`
- Project creation and initialization
- Package management (add/remove)
- Virtual environment setup

### `ppm_functions.rs`
- Project information display
- Requirements generation
- Script execution

### `settings.rs`
- TOML configuration handling
- Settings serialization/deserialization

### `utils.rs`
- Cross-platform path helpers
- File operations
- Process management

## Testing Guidelines

### Unit Tests

Add tests in the same file:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_package_name() {
        assert!(validate_package_name("requests").is_ok());
        assert!(validate_package_name("my-package").is_ok());
    }
}
```

### Integration Tests

Place in `tests/` directory:

```bash
tests/
└── integration_test.rs
```

## Documentation

### Code Documentation

- Document public functions and types
- Include examples in doc comments
- Use `///` for doc comments

### Updating README

When adding features:
1. Update `README.md` with usage examples
2. Add to appropriate section
3. Keep examples clear and runnable

## Pull Request Review Process

PRs should:
1. ✅ Pass all CI checks
2. ✅ Have clear commit history
3. ✅ Include relevant tests
4. ✅ Follow code style guidelines
5. ✅ Update documentation if needed

**Reviewers will:**
- Check code quality and style
- Verify tests are comprehensive
- Ensure no breaking changes
- Provide constructive feedback

## Reporting Issues

### Bug Reports

Include:
- Clear title describing the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- System information (OS, Rust version, PPM version)
- Error messages/logs

### Feature Requests

Include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if any)
- Examples of similar tools

## Areas for Contribution

### High Priority
- [ ] Dependency resolution
- [ ] Lock file support
- [ ] Dev dependencies
- [ ] Improved error messages
- [ ] Performance optimizations

### Medium Priority
- [ ] Python version management
- [ ] Project templates
- [ ] Installation progress bar
- [ ] Package conflict detection
- [ ] Caching for PyPI responses

### Low Priority
- [ ] Additional documentation
- [ ] Example projects
- [ ] Tutorial videos
- [ ] Blog posts

## Questions?

- Check [Discussions](https://github.com/Sumangal44/python-project-manager/discussions)
- Open an [Issue](https://github.com/Sumangal44/python-project-manager/issues)
- Read the [Wiki](https://github.com/Sumangal44/python-project-manager/wiki)

Thank you for contributing! 🚀
