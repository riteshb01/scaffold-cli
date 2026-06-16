import argparse
import sys
import os

from scaffold_cli.scaffolder import TEMPLATES, Scaffolder


def cmd_new(args: argparse.Namespace) -> None:
    print(f"\n Scaffolding '{args.name}' ({args.type})...")
    try:
        s = Scaffolder(
            project_name=args.name,
            template_key=args.type,
            output_dir=args.output or ".",
        )
        s.run(open_vscode=args.code)
        path = os.path.join(args.output or ".", args.name)
        print(f"Project created at: {os.path.abspath(path)}")
        print(f"\n   cd {args.name}")
        _print_next_steps(args.type)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list(_args: argparse.Namespace) -> None:
    print("\nAvailable templates:\n")
    for key, cls in TEMPLATES.items():
        print(f"  {key:<14} {cls.label}")
    print()


def _print_next_steps(template_key: str) -> None:
    steps = {
        "flask": "pip install -r requirements.txt\npython run.py",
        "nextjs": "npm install\nnpm run dev",
        "python-cli": "pip install -e .\n<your-project-name> --help",
        "django": "pip install -r requirements.txt\npython manage.py migrate\npython manage.py runserver",
    }
    if template_key in steps:
        print("\n   Next steps:")
        for line in steps[template_key].split("\n"):
            print(f"   {line}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="scaffold",
        description="Scaffold new dev projects instantly.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # scaffold new
    new_parser = subparsers.add_parser("new", help="Create a new project")
    new_parser.add_argument("name", help="Project name")
    new_parser.add_argument(
        "--type",
        required=True,
        choices=list(TEMPLATES.keys()),
        metavar="TYPE",
        help=f"Template type: {', '.join(TEMPLATES.keys())}",
    )
    new_parser.add_argument(
        "--output",
        "-o",
        default=".",
        metavar="DIR",
        help="Output directory (default: current directory)",
    )
    new_parser.add_argument(
        "--code",
        action="store_true",
        help="Open project in VS Code after creation",
    )
    new_parser.set_defaults(func=cmd_new)

    # scaffold list
    list_parser = subparsers.add_parser("list", help="List available templates")
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
