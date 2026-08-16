import argparse

from github_client import (
    parse_repo_url,
    get_repo_metadata,
    get_languages,
    get_file_tree,
    get_file_content,
)

from analyzer import (
    detect_tech_stack,
    select_key_files,
    group_by_folder,
)

from prompt_builder import build_prompt
from llm import generate_report


def main():
    parser = argparse.ArgumentParser(
        description="Explain a public GitHub repository using AI."
    )

    parser.add_argument(
        "url",
        help="GitHub repository URL"
    )

    parser.add_argument(
        "--output",
        default="report.md",
        help="Output Markdown file"
    )

    args = parser.parse_args()

    try:
        owner, repo = parse_repo_url(args.url)

        print(f"\nRepository: {owner}/{repo}")

        print("\nFetching repository metadata...")
        metadata = get_repo_metadata(owner, repo)

        print("Fetching language breakdown...")
        languages = get_languages(owner, repo)

        print("Fetching file tree...")
        tree = get_file_tree(
            owner,
            repo,
            metadata["default_branch"]
        )

        print("Analyzing repository...")

        tech_stack = detect_tech_stack(languages, tree)
        key_files = select_key_files(tree)
        folder_groups = group_by_folder(tree)

        print("Fetching key file contents...")

        key_file_contents = {}

        for file in key_files:
            path = file["path"]

            print(f"  Fetching: {path}")

            content = get_file_content(
                owner,
                repo,
                path,
                metadata["default_branch"]
            )

            key_file_contents[path] = content

        print("Building AI prompt...")

        prompt = build_prompt(
            metadata,
            tech_stack,
            folder_groups,
            tree,
            key_file_contents,
        )

        print("Sending repository to Gemini...")

        report = generate_report(prompt)

        with open(
            args.output,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(report)

        print(f"\nReport successfully saved to: {args.output}")

    except (ValueError, RuntimeError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()