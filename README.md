# GitHub Repository Explainer

A lightweight Python CLI tool that analyzes a public GitHub repository
and generates a concise Markdown explanation using Gemini.

## What it does

The tool takes a public GitHub repository URL and:

1. Fetches repository metadata.
2. Fetches the repository language breakdown.
3. Retrieves the complete file tree.
4. Detects the likely technology stack.
5. Groups files by folder.
6. Selects a small set of important files.
7. Fetches the contents of those files.
8. Builds a structured prompt.
9. Sends the prompt to Gemini.
10. Saves the generated explanation as a Markdown file.

The tool intentionally does not send the entire repository to the LLM.
It gives the model the complete file structure while providing the
contents of only selected key files.

## Requirements

- Python 3.9 or newer
- A Gemini API key
- Internet connection
- Access to public GitHub repositories

## Installation

Clone the repository:

```bash
git clone https://github.com/vik-25/github-repo-explainer.git
cd github-repo-explainer
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is intentionally excluded from Git using `.gitignore`.

Do not share or commit your API key.

## Usage

Run the tool with a GitHub repository URL:

```bash
python main.py https://github.com/owner/repository
```

The generated report will be saved as:

```text
report.md
```

### Specify an output file

You can provide a custom output filename:

```bash
python main.py https://github.com/owner/repository --output my-report.md
```

For example:

```bash
python main.py https://github.com/psf/requests --output requests.md
```

## Project Structure

```text
github-repo-explainer/
├── main.py
├── github_client.py
├── analyzer.py
├── prompt_builder.py
├── llm.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── examples/
    └── sample_report.md
```

### `main.py`

CLI entry point and application orchestration.

### `github_client.py`

Handles GitHub network requests, including repository metadata,
language information, the recursive file tree, and selected file
contents.

### `analyzer.py`

Contains deterministic repository-analysis heuristics for detecting
the technology stack, selecting key files, and grouping files by
folder.

### `prompt_builder.py`

Combines the repository information and selected file contents into
the structured prompt sent to the LLM.

### `llm.py`

Handles communication with Gemini and returns the generated Markdown
report.

## Example

A sample report generated from the
[Requests](https://github.com/psf/requests) repository is available at:

```text
examples/sample_report.md
```

The example demonstrates the format and level of detail produced by
the tool.

## How the pipeline works

```text
GitHub Repository URL
        │
        ▼
github_client.py
        │
        ▼
Repository Metadata + Languages + File Tree
        │
        ▼
analyzer.py
        │
        ├── Technology Stack
        ├── Key Files
        └── Folder Groups
        │
        ▼
Selected File Contents
        │
        ▼
prompt_builder.py
        │
        ▼
Structured AI Prompt
        │
        ▼
llm.py
        │
        ▼
Gemini
        │
        ▼
Markdown Report
```

## Limitations

- Only public GitHub repositories are supported.
- GitHub's unauthenticated API rate limits apply.
- Very large repositories may have a truncated file tree.
- The analysis is based on repository metadata, file structure, and
  selected key files.
- The generated report is AI-assisted and should be reviewed when
  implementation-level accuracy is important.

## License

Add your preferred license here.
