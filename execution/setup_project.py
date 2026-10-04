"""Prepare the three-layer workspace without overwriting existing settings."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ("directives", "execution", ".tmp")
IGNORE_ENTRIES = (
    ".tmp/",
    ".env",
    "credentials.json",
    "token.json",
    "__pycache__/",
    "*.py[cod]",
)


def main():
    for name in DIRECTORIES:
        (ROOT / name).mkdir(exist_ok=True)

    # Exclusive creation preserves any existing environment settings.
    try:
        with (ROOT / ".env").open("x", encoding="utf-8") as env_file:
            env_file.write("# Add environment variables and API keys when required.\n")
    except FileExistsError:
        pass

    ignore_file = ROOT / ".gitignore"
    existing = ignore_file.read_text(encoding="utf-8-sig") if ignore_file.exists() else ""
    missing = [entry for entry in IGNORE_ENTRIES if entry not in existing.splitlines()]
    if missing:
        with ignore_file.open("a", encoding="utf-8") as output:
            if existing and not existing.endswith("\n"):
                output.write("\n")
            output.write("\n".join(missing) + "\n")

    for name in (*DIRECTORIES, ".env", ".gitignore"):
        print(f"OK: {name}")
    for name in ("credentials.json", "token.json"):
        status = "present; authorization not checked" if (ROOT / name).is_file() else "not configured"
        print(f"Google OAuth {name}: {status}")


if __name__ == "__main__":
    main()
