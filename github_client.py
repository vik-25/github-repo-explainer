import requests
from urllib.parse import urlparse


BASE_URL = "https://api.github.com"


def parse_repo_url(url):
    parsed = urlparse(url)

    if parsed.netloc != "github.com":
        raise ValueError("Please provide a valid GitHub repository URL.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repo = parts[1].removesuffix(".git")

    return owner, repo


def github_get(url):
    response = requests.get(url,timeout=10)

    if response.status_code == 404:
        raise RuntimeError("Repository not found or private.")

    if response.status_code == 403:
        remaining = response.headers.get("X-RateLimit-Remaining")

        if remaining == "0":
            raise RuntimeError("GitHub API rate limit reached.\nPlease wait before trying again.")

        raise RuntimeError("GitHub request was forbidden.")

    response.raise_for_status()

    return response.json()


def get_repo_metadata(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}"

    data = github_get(url)

    return {
        "name": data["name"],
        "description": data["description"],
        "stars": data["stargazers_count"],
        "default_branch": data["default_branch"],
        "topics": data.get("topics", []),
        "license": data["license"]["name"] if data["license"] else None,
    }


def get_languages(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}/languages"

    return github_get(url)


def get_file_tree(owner, repo, branch):
    url = f"{BASE_URL}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    data = github_get(url)

    if data.get("truncated"):
        print(
            "Warning: GitHub returned a truncated file tree. "
            "The repository analysis may be incomplete."
        )

    return data["tree"]


def get_file_content(owner, repo, path, branch):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        raise RuntimeError(f"File not found: {path}")

    response.raise_for_status()

    return response.text