# scaffold-cli

A minimal command-line tool that spins up new dev projects in one command — folders, boilerplate, and an initial git commit, all done.

```bash
scaffold new my-api --type flask
scaffold new my-app --type nextjs
scaffold new my-tool --type python-cli
scaffold new my-site --type django
```

---

## Why

Setting up a new project is always the same five minutes of busywork: create the folder, `git init`, copy a `.gitignore`, write a `README`, wire up the entry point. This tool does all of that in one shot so you can skip straight to building.

---

## Install

```bash
pip install scaffold-cli
```

Or install from source:

```bash
git clone https://github.com/yourusername/scaffold-cli.git
cd scaffold-cli
pip install -e .
```

Requires Python 3.10+.

---

## Usage

### Create a new project

```bash
scaffold new <project-name> --type <template>
```

**Options**

| Flag | Description |
|------|-------------|
| `--type` | Template to use (required) |
| `--output`, `-o` | Directory to create project in (default: `.`) |
| `--code` | Open the project in VS Code after creation |

**Examples**

```bash
# Flask API
scaffold new my-api --type flask

# Next.js app, open in VS Code immediately
scaffold new my-frontend --type nextjs --code

# Python CLI tool, placed in a specific folder
scaffold new my-tool --type python-cli --output ~/projects
```

### List available templates

```bash
scaffold list
```

```
Available templates:

  flask          Flask (Python web app)
  nextjs         Next.js (React frontend)
  python-cli     Python CLI tool
  django         Django (Python full-stack)
```

---

## What gets created

### `flask`
```
my-api/
├── app/
│   ├── __init__.py    # app factory
│   └── routes.py
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### `nextjs`
```
my-app/
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   └── globals.css
├── package.json
├── tsconfig.json
├── .gitignore
└── README.md
```

### `python-cli`
```
my-tool/
├── my-tool/
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── README.md
```

### `django`
```
my-site/
├── my-site/
│   ├── __init__.py
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

Every project gets `git init` + an initial commit automatically.

---

## Adding a custom template

Subclass `ProjectTemplate` in `scaffold_cli/scaffolder.py` and add it to the `TEMPLATES` dict:

```python
class MyTemplate(ProjectTemplate):
    label = "My custom template"

    def get_structure(self) -> dict:
        return {
            "main.py": "# entry point\n",
            ".gitignore": "*.pyc\n",
            "README.md": f"# {self.name}\n",
        }

TEMPLATES["my-template"] = MyTemplate
```

Then use it like any other:

```bash
scaffold new my-project --type my-template
```

---

## License

MIT
