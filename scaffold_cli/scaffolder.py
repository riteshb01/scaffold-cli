import os
import subprocess
from abc import ABC, abstractmethod


class ProjectTemplate(ABC):
    """Base class for all project templates."""

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    @abstractmethod
    def get_structure(self) -> dict:
        """Return a dict of {relative_path: file_content}."""
        pass

    @property
    @abstractmethod
    def label(self) -> str:
        pass


class FlaskTemplate(ProjectTemplate):
    label = "Flask (Python web app)"

    def get_structure(self) -> dict:
        return {
            "app/__init__.py": (
                "from flask import Flask\n\n"
                "def create_app():\n"
                "    app = Flask(__name__)\n\n"
                "    @app.route('/')\n"
                "    def index():\n"
                "        return 'Hello from Flask!'\n\n"
                "    return app\n"
            ),
            "app/routes.py": (
                "from flask import Blueprint\n\n"
                "main = Blueprint('main', __name__)\n\n"
                "@main.route('/health')\n"
                "def health():\n"
                "    return {'status': 'ok'}\n"
            ),
            "run.py": (
                "from app import create_app\n\n"
                "app = create_app()\n\n"
                "if __name__ == '__main__':\n"
                "    app.run(debug=True)\n"
            ),
            "requirements.txt": "flask>=3.0.0\npython-dotenv>=1.0.0\n",
            ".env.example": "FLASK_ENV=development\nSECRET_KEY=change-me\n",
            ".gitignore": _python_gitignore(),
            "README.md": _readme(self.name, "Flask"),
        }


class NextJSTemplate(ProjectTemplate):
    label = "Next.js (React frontend)"

    def get_structure(self) -> dict:
        return {
            "app/page.tsx": (
                "export default function Home() {\n"
                "  return (\n"
                "    <main>\n"
                "      <h1>Welcome to {self.name}</h1>\n"
                "    </main>\n"
                "  );\n"
                "}\n"
            ).replace("{self.name}", self.name),
            "app/layout.tsx": (
                "export const metadata = { title: '"
                + self.name
                + "' };\n\n"
                "export default function RootLayout({ children }: { children: React.ReactNode }) {\n"
                "  return (\n"
                "    <html lang='en'>\n"
                "      <body>{children}</body>\n"
                "    </html>\n"
                "  );\n"
                "}\n"
            ),
            "app/globals.css": "* { box-sizing: border-box; margin: 0; padding: 0; }\n",
            "package.json": (
                "{\n"
                f'  "name": "{self.name}",\n'
                '  "version": "0.1.0",\n'
                '  "private": true,\n'
                '  "scripts": {\n'
                '    "dev": "next dev",\n'
                '    "build": "next build",\n'
                '    "start": "next start"\n'
                "  },\n"
                '  "dependencies": {\n'
                '    "next": "^14.0.0",\n'
                '    "react": "^18.0.0",\n'
                '    "react-dom": "^18.0.0"\n'
                "  },\n"
                '  "devDependencies": {\n'
                '    "typescript": "^5.0.0",\n'
                '    "@types/react": "^18.0.0",\n'
                '    "@types/node": "^20.0.0"\n'
                "  }\n"
                "}\n"
            ),
            "tsconfig.json": (
                '{\n  "compilerOptions": {\n'
                '    "target": "es5",\n'
                '    "lib": ["dom", "dom.iterable", "esnext"],\n'
                '    "allowJs": true,\n'
                '    "skipLibCheck": true,\n'
                '    "strict": true,\n'
                '    "noEmit": true,\n'
                '    "esModuleInterop": true,\n'
                '    "module": "esnext",\n'
                '    "moduleResolution": "bundler",\n'
                '    "resolveJsonModule": true,\n'
                '    "isolatedModules": true,\n'
                '    "jsx": "preserve",\n'
                '    "incremental": true,\n'
                '    "plugins": [{ "name": "next" }]\n'
                "  },\n"
                '  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],\n'
                '  "exclude": ["node_modules"]\n'
                "}\n"
            ),
            ".gitignore": _nextjs_gitignore(),
            "README.md": _readme(self.name, "Next.js"),
        }


class PythonCLITemplate(ProjectTemplate):
    label = "Python CLI tool"

    def get_structure(self) -> dict:
        return {
            f"{self.name}/__init__.py": f"# {self.name}\n",
            f"{self.name}/main.py": (
                "import argparse\n\n\n"
                "def main():\n"
                "    parser = argparse.ArgumentParser(description='"
                + self.name
                + " CLI')\n"
                "    parser.add_argument('command', help='Command to run')\n"
                "    args = parser.parse_args()\n"
                "    print(f'Running: {args.command}')\n\n\n"
                "if __name__ == '__main__':\n"
                "    main()\n"
            ),
            "pyproject.toml": (
                "[build-system]\n"
                'requires = ["setuptools>=68"]\n'
                'build-backend = "setuptools.backends.legacy:build"\n\n'
                "[project]\n"
                f'name = "{self.name}"\n'
                'version = "0.1.0"\n'
                'requires-python = ">=3.10"\n\n'
                "[project.scripts]\n"
                f'{self.name} = "{self.name}.main:main"\n'
            ),
            "requirements.txt": "# add dependencies here\n",
            ".gitignore": _python_gitignore(),
            "README.md": _readme(self.name, "Python CLI"),
        }


class DjangoTemplate(ProjectTemplate):
    label = "Django (Python full-stack)"

    def get_structure(self) -> dict:
        return {
            # ── entry point ──────────────────────────────────────────────────
            "manage.py": (
                "#!/usr/bin/env python\n"
                "import os, sys\n\n"
                "def main():\n"
                "    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '"
                + self.name
                + ".settings')\n"
                "    from django.core.management import execute_from_command_line\n"
                "    execute_from_command_line(sys.argv)\n\n"
                "if __name__ == '__main__':\n"
                "    main()\n"
            ),
            # ── project package ──────────────────────────────────────────────
            f"{self.name}/__init__.py": "",
            f"{self.name}/settings.py": (
                "from pathlib import Path\n"
                "from dotenv import load_dotenv\n"
                "import os\n\n"
                "load_dotenv()\n\n"
                "BASE_DIR = Path(__file__).resolve().parent.parent\n\n"
                "SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')\n"
                "DEBUG = os.environ.get('DEBUG', 'True') == 'True'\n"
                "ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')\n\n"
                "INSTALLED_APPS = [\n"
                "    'django.contrib.admin',\n"
                "    'django.contrib.auth',\n"
                "    'django.contrib.contenttypes',\n"
                "    'django.contrib.sessions',\n"
                "    'django.contrib.messages',\n"
                "    'django.contrib.staticfiles',\n"
                "    'core',\n"
                "]\n\n"
                "MIDDLEWARE = [\n"
                "    'django.middleware.security.SecurityMiddleware',\n"
                "    'django.contrib.sessions.middleware.SessionMiddleware',\n"
                "    'django.middleware.common.CommonMiddleware',\n"
                "    'django.middleware.csrf.CsrfViewMiddleware',\n"
                "    'django.contrib.auth.middleware.AuthenticationMiddleware',\n"
                "    'django.contrib.messages.middleware.MessageMiddleware',\n"
                "    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n"
                "]\n\n"
                f"ROOT_URLCONF = '{self.name}.urls'\n\n"
                "TEMPLATES = [\n"
                "    {\n"
                "        'BACKEND': 'django.template.backends.django.DjangoTemplates',\n"
                "        'DIRS': [BASE_DIR / 'templates'],\n"
                "        'APP_DIRS': True,\n"
                "        'OPTIONS': {\n"
                "            'context_processors': [\n"
                "                'django.template.context_processors.debug',\n"
                "                'django.template.context_processors.request',\n"
                "                'django.contrib.auth.context_processors.auth',\n"
                "                'django.contrib.messages.context_processors.messages',\n"
                "            ],\n"
                "        },\n"
                "    },\n"
                "]\n\n"
                f"WSGI_APPLICATION = '{self.name}.wsgi.application'\n\n"
                "DATABASES = {\n"
                "    'default': {\n"
                "        'ENGINE': 'django.db.backends.sqlite3',\n"
                "        'NAME': BASE_DIR / 'db.sqlite3',\n"
                "    }\n"
                "}\n\n"
                "AUTH_PASSWORD_VALIDATORS = [\n"
                "    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},\n"
                "    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},\n"
                "    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},\n"
                "    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},\n"
                "]\n\n"
                "LANGUAGE_CODE = 'en-us'\n"
                "TIME_ZONE = 'UTC'\n"
                "USE_I18N = True\n"
                "USE_TZ = True\n\n"
                "STATIC_URL = '/static/'\n"
                "STATICFILES_DIRS = [BASE_DIR / 'static']\n"
                "STATIC_ROOT = BASE_DIR / 'staticfiles'\n\n"
                "MEDIA_URL = '/media/'\n"
                "MEDIA_ROOT = BASE_DIR / 'media'\n\n"
                "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'\n"
                "LOGIN_REDIRECT_URL = '/'\n"
                "LOGOUT_REDIRECT_URL = '/'\n"
            ),
            f"{self.name}/urls.py": (
                "from django.contrib import admin\n"
                "from django.urls import path, include\n"
                "from django.conf import settings\n"
                "from django.conf.urls.static import static\n\n"
                "urlpatterns = [\n"
                "    path('admin/', admin.site.urls),\n"
                "    path('', include('core.urls')),\n"
                "] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n"
            ),
            f"{self.name}/wsgi.py": (
                "import os\n"
                "from django.core.wsgi import get_wsgi_application\n\n"
                f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.name}.settings')\n"
                "application = get_wsgi_application()\n"
            ),
            f"{self.name}/asgi.py": (
                "import os\n"
                "from django.core.asgi import get_asgi_application\n\n"
                f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{self.name}.settings')\n"
                "application = get_asgi_application()\n"
            ),
            # ── core app ─────────────────────────────────────────────────────
            "core/__init__.py": "",
            "core/apps.py": (
                "from django.apps import AppConfig\n\n\n"
                "class CoreConfig(AppConfig):\n"
                "    default_auto_field = 'django.db.models.BigAutoField'\n"
                "    name = 'core'\n"
            ),
            "core/models.py": (
                "from django.db import models\n\n"
                "# Create your models here.\n"
            ),
            "core/views.py": (
                "from django.shortcuts import render\n\n\n"
                "def index(request):\n"
                "    context = {'project_name': '" + self.name + "'}\n"
                "    return render(request, 'core/index.html', context)\n"
            ),
            "core/urls.py": (
                "from django.urls import path\n"
                "from . import views\n\n"
                "app_name = 'core'\n\n"
                "urlpatterns = [\n"
                "    path('', views.index, name='index'),\n"
                "]\n"
            ),
            "core/admin.py": (
                "from django.contrib import admin\n\n"
                "# Register your models here.\n"
            ),
            "core/tests.py": (
                "from django.test import TestCase, Client\n"
                "from django.urls import reverse\n\n\n"
                "class IndexViewTest(TestCase):\n"
                "    def setUp(self):\n"
                "        self.client = Client()\n\n"
                "    def test_index_status_code(self):\n"
                "        response = self.client.get(reverse('core:index'))\n"
                "        self.assertEqual(response.status_code, 200)\n"
            ),
            # ── templates ────────────────────────────────────────────────────
            "templates/base.html": (
                "<!DOCTYPE html>\n"
                '<html lang="en">\n'
                "<head>\n"
                '    <meta charset="UTF-8">\n'
                '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                "    <title>{% block title %}" + self.name + "{% endblock %}</title>\n"
                "    {% load static %}\n"
                "    <link rel=\"stylesheet\" href=\"{% static 'css/main.css' %}\">\n"
                "</head>\n"
                "<body>\n"
                "    <nav>\n"
                '        <a href="/">' + self.name + "</a>\n"
                "    </nav>\n"
                "    <main>\n"
                "        {% if messages %}\n"
                "            {% for message in messages %}\n"
                '                <div class="message {{ message.tags }}">{{ message }}</div>\n'
                "            {% endfor %}\n"
                "        {% endif %}\n"
                "        {% block content %}{% endblock %}\n"
                "    </main>\n"
                "    <script src=\"{% static 'js/main.js' %}\"></script>\n"
                "</body>\n"
                "</html>\n"
            ),
            "templates/core/index.html": (
                "{% extends 'base.html' %}\n\n"
                "{% block title %}Home — {{ project_name }}{% endblock %}\n\n"
                "{% block content %}\n"
                "<h1>Welcome to {{ project_name }}</h1>\n"
                "<p>Your Django project is up and running. "
                "<a href='/admin/'>Admin</a></p>\n"
                "{% endblock %}\n"
            ),
            # ── static files ─────────────────────────────────────────────────
            "static/css/main.css": (
                "*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }\n\n"
                "body {\n"
                "    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;\n"
                "    line-height: 1.6;\n"
                "    color: #333;\n"
                "}\n\n"
                "nav {\n"
                "    padding: 1rem 2rem;\n"
                "    background: #0d6efd;\n"
                "    color: white;\n"
                "    font-weight: 600;\n"
                "}\n\n"
                "nav a { color: white; text-decoration: none; }\n\n"
                "main { max-width: 960px; margin: 2rem auto; padding: 0 1rem; }\n\n"
                ".message { padding: 0.75rem 1rem; margin-bottom: 1rem; border-radius: 4px; }\n"
                ".message.success { background: #d1e7dd; color: #0f5132; }\n"
                ".message.error   { background: #f8d7da; color: #842029; }\n"
            ),
            "static/js/main.js": (
                "// Main JS entry point\n"
                "console.log('Django app loaded');\n"
            ),
            # ── infra ────────────────────────────────────────────────────────
            "requirements.txt": "django>=5.0\npython-dotenv>=1.0.0\n",
            ".env.example": (
                "SECRET_KEY=change-me-use-a-long-random-string\n"
                "DEBUG=True\n"
                "ALLOWED_HOSTS=localhost,127.0.0.1\n"
            ),
            ".gitignore": _python_gitignore() + "db.sqlite3\nmedia/\nstaticfiles/\n",
            "README.md": _readme(self.name, "Django"),
        }


TEMPLATES: dict[str, type[ProjectTemplate]] = {
    "flask": FlaskTemplate,
    "nextjs": NextJSTemplate,
    "python-cli": PythonCLITemplate,
    "django": DjangoTemplate,
}


def _python_gitignore() -> str:
    return (
        "__pycache__/\n*.py[cod]\n*.egg-info/\ndist/\nbuild/\n"
        ".env\n.venv/\nvenv/\n.DS_Store\n*.log\n"
    )


def _nextjs_gitignore() -> str:
    return (
        "node_modules/\n.next/\nout/\nbuild/\n.env\n.env.local\n"
        ".DS_Store\n*.log\nnpm-debug.log*\n"
    )


def _readme(name: str, template_type: str) -> str:
    return (
        f"# {name}\n\n"
        f"A {template_type} project scaffolded with [scaffold-cli](https://github.com/yourusername/scaffold-cli).\n\n"
        "## Getting Started\n\n"
        "```bash\n# install dependencies\n# run the project\n```\n\n"
        "## License\n\nMIT\n"
    )


class Scaffolder:
    """Orchestrates project creation."""

    def __init__(self, project_name: str, template_key: str, output_dir: str = "."):
        if template_key not in TEMPLATES:
            raise ValueError(
                f"Unknown template '{template_key}'. "
                f"Choose from: {', '.join(TEMPLATES)}"
            )
        self.project_name = project_name
        self.root = os.path.join(output_dir, project_name)
        template_cls = TEMPLATES[template_key]
        self.template: ProjectTemplate = template_cls(project_name, self.root)

    def run(self, open_vscode: bool = False) -> None:
        self._create_directories()
        self._write_files()
        self._git_init()
        if open_vscode:
            self._open_vscode()

    def _create_directories(self) -> None:
        structure = self.template.get_structure()
        dirs = set()
        for rel_path in structure:
            d = os.path.dirname(os.path.join(self.root, rel_path))
            if d:
                dirs.add(d)
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        os.makedirs(self.root, exist_ok=True)

    def _write_files(self) -> None:
        for rel_path, content in self.template.get_structure().items():
            full_path = os.path.join(self.root, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)

    def _git_init(self) -> None:
        subprocess.run(["git", "init"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            ["git", "add", "."], cwd=self.root, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "initial commit via scaffold-cli"],
            cwd=self.root,
            check=True,
            capture_output=True,
        )

    def _open_vscode(self) -> None:
        subprocess.run(["code", self.root])
