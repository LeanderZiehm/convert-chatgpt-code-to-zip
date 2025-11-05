# chatgpt-code-zip

This project provides a FastAPI web interface that extracts code blocks from a structured Markdown document and packages them into a downloadable ZIP archive. Each section in the Markdown that begins with a header referencing a valid filename (for example `# src/app.py`) will be parsed, and the code block beneath it will be written to the corresponding file inside the generated ZIP.

### Purpose

Developers frequently use Markdown to describe full project structures, especially when collaborating or sharing code in chat-based environments. The goal of this tool is to streamline the process of converting those Markdown excerpts into real files, enabling rapid bootstrapping of projects from documentation or AI-generated code specifications.

### Features

* Parses file paths from Markdown headers
* Extracts fenced code blocks and writes them to files
* Produces a ZIP archive dynamically in memory
* Provides a simple browser UI
* FastAPI backend for clean API access

---

## Running Locally Without Docker

### Requirements

* Python 3.12+
* Recommended: virtual environment

### Installation

```bash
git clone <repo-url>
cd chatgpt-code-zip
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then navigate to:

```
http://localhost:8000
```

---

## Running With Docker

### Build and Run

```bash
docker compose up --build
```

Or run the image manually:

```bash
docker build -t md-zipper .
docker run -p 8000:8000 --env-file .env md-zipper
```

Visit:

```
http://localhost:8000
```

---

## Environment Variables

The `.env` file controls the external port exposed by Docker:

```env
APP_PORT=8000
```

---

## Usage Workflow

1. Paste your Markdown that defines files with code blocks
2. Click the convert button
3. Download the generated ZIP containing the file tree represented in the Markdown

Example Markdown structure:

```markdown
# app/main.py
```

```python
print("Hello world")
```

---

## Notes

* File extraction logic only processes Markdown headers with valid filenames.
* Secrets should never appear in the Markdown; load them from environment files in your projects.
* This repository is designed to be safe to commit because sensitive values are externalized.


uvicorn main:app --port 5014 --reload
