# Contributing to scaffold-cli

First off — **thank you for taking the time to contribute!** 🎉

scaffold-cli is an open-source project and contributions of all kinds are welcome: new templates, bug fixes, documentation improvements, ideas, and more.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Adding a New Template](#adding-a-new-template)
  - [Submitting a Pull Request](#submitting-a-pull-request)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Project Structure](#project-structure)
- [Contributors](#contributors)

---

## Code of Conduct

This project follows a simple rule: **be kind**. Treat everyone with respect. Harassment, discrimination, or toxic behaviour of any kind will not be tolerated.

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/scaffold-cli.git
   cd scaffold-cli
   ```
3. **Create a branch** for your work:
   ```bash
   git checkout -b feat/my-new-template
   ```
4. Make your changes, commit, and push to your fork
5. Open a **Pull Request** against `main`

---

## How to Contribute

### Reporting Bugs

If you find a bug, please [open an issue](https://github.com/riteshb01/scaffold-cli/issues) with:

- A clear title and description
- Steps to reproduce
- Expected vs actual behaviour
- Your Python version and OS

### Suggesting Features

Open an issue with the `enhancement` label. Describe:
- What problem it solves
- How you'd expect it to work
- Any alternatives you've considered

### Adding a New Template

This is the most impactful contribution you can make! To add a template:

1. Open `scaffold_cli/scaffolder.py`
2. Subclass `ProjectTemplate`:

```python
class MyTemplate(ProjectTemplate):
    label = "My Framework (description)"

    def get_structure(self) -> dict:
        return {
            "main.py": "# entry point\n",
            ".gitignore": "*.pyc\n",
            "README.md": _readme(self.name, "My Framework"),
        }
```

3. Register it in the `TEMPLATES` dict:

```python
TEMPLATES["my-template"] = MyTemplate
```

4. Add the next-steps hint in `scaffold_cli/cli.py` inside `_print_next_steps()`:

```python
"my-template": "npm install\nnpm run dev",
```

5. Document the file structure it creates in `README.md`

**Template checklist:**
- [ ] Always include a `.gitignore`
- [ ] Always include a `README.md` (use the `_readme()` helper)
- [ ] Use sensible, minimal boilerplate — no unnecessary bloat
- [ ] Test it end-to-end: `scaffold new test-project --type my-template`

### Submitting a Pull Request

- Keep PRs focused — one feature or fix per PR
- Write a clear PR description explaining *what* and *why*
- Make sure the tool runs without errors after your change
- Update `README.md` if you added a template or changed behaviour

---

## Development Setup

**Requirements:** Python 3.10+

```bash
# Install in editable mode
pip install -e .

# Verify the CLI works
scaffold --help
scaffold list

# Test your template
scaffold new my-test --type flask
```

No additional dependencies are required for development.

---

## Code Style

- Follow standard Python conventions (PEP 8)
- Use type hints for all function signatures
- Keep functions small and focused
- Prefer clarity over cleverness

---

## Project Structure

```
scaffold-cli/
├── scaffold_cli/
│   ├── __init__.py
│   ├── cli.py          # argument parsing & CLI commands
│   └── scaffolder.py   # template classes & Scaffolder orchestrator
├── pyproject.toml      # package metadata & entry point
├── README.md
├── CONTRIBUTING.md     # ← you are here
└── LICENSE
```

---

## Contributors

A huge thanks to everyone who has contributed to this project:

| Name | GitHub | Contribution |
|------|--------|--------------|
| Ritesh Bastola | [@riteshb01](https://github.com/riteshb01) | Creator & maintainer |

> **Want your name here?** Submit a PR and you'll be added! 🙌

---

*scaffold-cli is MIT licensed. By contributing, you agree that your contributions will be licensed under the same MIT License.*
