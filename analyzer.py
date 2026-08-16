def detect_tech_stack(languages, tree):
    stack = set()

    for language in languages:
        stack.add(language)

    paths = [item["path"].lower() for item in tree]

    markers = {
        "package.json": "Node.js",
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        "setup.py": "Python",
        "cargo.toml": "Rust",
        "go.mod": "Go",
        "pom.xml": "Java",
        "build.gradle": "Java",
        "dockerfile": "Docker",
    }

    for path in paths:
        filename = path.split("/")[-1]

        if filename in markers:
            stack.add(markers[filename])

        if path.startswith(".github/workflows/"):
            stack.add("GitHub Actions")

    return sorted(stack)


def select_key_files(tree, limit=7):
    priority_files = []
    candidates = []

    excluded_names = {
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "poetry.lock",
        "pipfile.lock",
    }

    excluded_directories = {
        ".git",
        "node_modules",
        "__pycache__",
        "dist",
        "build",
        "vendor",
        ".venv",
        "tests",
        "test",
        "certs",
        "docs",
        "doc",
    }

    excluded_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".ico",
        ".webp",
        ".ai",
        ".psd",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".exe",
        ".dll",
    }

    manifest_files = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "dockerfile",
    }

    entry_points = {
        "main.py",
        "app.py",
        "__main__.py",
        "index.js",
        "index.ts",
        "main.js",
        "main.go",
        "main.rs",
    }

    important_source_files = {
        "__init__.py",
        "api.py",
        "application.py",
        "app.py",
        "client.py",
        "server.py",
        "routes.py",
        "models.py",
        "services.py",
        "database.py",
        "adapters.py",
        "sessions.py",
        "config.py",
    }

    source_extensions = {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".go",
        ".rs",
        ".cpp",
        ".c",
    }

    for item in tree:
        if item["type"] != "blob":
            continue

        path = item["path"]
        parts = path.lower().split("/")
        filename = parts[-1]

        if filename in excluded_names:
            continue

        if any(
            directory in excluded_directories
            for directory in parts[:-1]
        ):
            continue

        if any(filename.endswith(ext) for ext in excluded_extensions):
            continue

        if filename == "readme.md" and len(parts) == 1:
            priority_files.append((0, item))

        elif filename in manifest_files and len(parts) == 1:
            priority_files.append((1, item))

        elif filename in entry_points:
            priority_files.append((2, item))

        elif filename in important_source_files:
            priority_files.append((3, item))

        elif any(filename.endswith(ext) for ext in source_extensions):
            candidates.append(item)

    candidates.sort(
        key=lambda item: item.get("size", 0),
        reverse=True
    )

    priority_files.sort(key=lambda item: item[0])

    selected = [item for _, item in priority_files]
    selected.extend(candidates)

    return selected[:limit]


def group_by_folder(tree):
    groups = {}

    excluded_directories = {
        ".git",
        "node_modules",
        "__pycache__",
        "dist",
        "build",
        "vendor",
        ".venv",
    }

    for item in tree:
        if item["type"] != "blob":
            continue

        parts = item["path"].split("/")

        if any(
            directory.lower() in excluded_directories
            for directory in parts
        ):
            continue

        if len(parts) == 1:
            folder = "root"
        else:
            folder = parts[0]

        groups[folder] = groups.get(folder, 0) + 1

    return groups