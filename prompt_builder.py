def build_prompt(
    metadata,
    tech_stack,
    folder_groups,
    tree,
    key_file_contents
):
    prompt = f"""
You are an expert software engineer analyzing a public GitHub repository.

Your task is to explain the repository clearly to a developer who has
never seen the project before.

REPOSITORY METADATA

Name: {metadata["name"]}
Description: {metadata["description"]}
Stars: {metadata["stars"]}
Default branch: {metadata["default_branch"]}
Topics: {", ".join(metadata["topics"]) if metadata["topics"] else "None"}
License: {metadata["license"] or "Not specified"}


TECH STACK

{format_list(tech_stack)}


FOLDER STRUCTURE

{format_folder_groups(folder_groups)}


COMPLETE FILE TREE

{format_file_tree(tree)}


KEY FILE CONTENTS

{format_key_files(key_file_contents)}


INSTRUCTIONS

Generate a concise but useful technical explanation of this repository.

SOURCE BOUNDARIES

You have two levels of repository information:

1. FILE TREE
   The file tree tells you which files and folders exist.
   It does NOT provide the contents or implementation of those files.

2. KEY FILE CONTENTS
   These are the files whose actual contents have been provided.
   You may make detailed implementation claims only when they are
   supported by these contents.

If a file appears in the file tree but its contents were not provided,
you may mention that the file exists, but do not describe its internal
implementation as fact.

When describing repository behavior, prioritize:
- information directly supported by provided file contents
- repository metadata
- detected technology information
- structural observations from the file tree

Do not invent:
- files
- classes
- functions
- dependencies
- features
- implementation details
- bugs

If something cannot be determined from the provided information,
say so or clearly indicate the uncertainty.

Your response MUST contain exactly these five Markdown sections:

# Overview

Explain what the project does, who it is for, and its main purpose.

# Tech Stack

Explain the important technologies used and what role each one appears
to play in the project.

# Repository Structure

Explain the important folders and how the project is organized.
Base implementation details on provided file contents only.

# Key Files

Choose the three most important files from the provided key files.

For each one:
- Give its path.
- Explain what it does.
- Explain why a developer should read it.

Only describe implementation details that are supported by the
provided contents of that file.

# Suggested Improvement

Suggest exactly one practical improvement to the repository.

The suggestion must be based on something supported by the provided
repository information or file contents.

Do not invent problems that are not supported by the repository.

IMPORTANT OUTPUT RULES

- Return only the Markdown report.
- Do not add an introduction before # Overview.
- Do not add a conclusion after # Suggested Improvement.
- Do not create additional top-level sections.
- Keep the report technically accurate.
- Clearly indicate uncertainty when necessary.
"""

    return prompt


def format_list(items):
    if not items:
        return "- None detected"

    return "\n".join(f"- {item}" for item in items)


def format_folder_groups(groups):
    if not groups:
        return "No folders detected."

    return "\n".join(
        f"- {folder}: {count} files"
        for folder, count in groups.items()
    )


def format_file_tree(tree):
    files = []

    for item in tree:
        if item["type"] == "blob":
            files.append(item["path"])

    if not files:
        return "No files detected."

    return "\n".join(files)


def format_key_files(key_file_contents):
    if not key_file_contents:
        return "No key file contents available."

    sections = []

    for path, content in key_file_contents.items():
        sections.append(
            f"--- {path} ---\n\n{content}"
        )

    return "\n\n".join(sections)