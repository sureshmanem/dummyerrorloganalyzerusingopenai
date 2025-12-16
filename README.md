# Dummy Error Log Analyzer using OpenAI API

About

This small project demonstrates how to use the OpenAI API to analyze application error logs and produce a concise JSON summary useful for triage. It is a lightweight example and developer utility, not a production monitoring system.

Key features:

- Read timestamped log files and send them to an LLM for analysis.
- Extract structured JSON containing detected error types, counts, example messages, timestamps, severity, and recommended remediations.
- Save analysis output to a file with `--output`.
- Simple `.env` support for `OPENAI_API_KEY` and an included `dummy_error.log` for quick testing.

Primary files:

- `analyze_log.py`: main script that reads a log and calls the OpenAI ChatCompletion API.
- `dummy_error.log`: example log for testing.
- `requirements.txt`: Python dependencies.
- `.env.example`: example environment file (do not commit real keys).
- `.gitignore`: ignores secrets, venvs, logs, and build artifacts.

Intended audience and use-cases:

- Developers learning how to integrate LLMs for lightweight observability tasks.
- Quick triage of small logs during debugging or post-mortem investigation.
- Educational demos and prototypes.

A minimal example showing how to analyze a small error log using the OpenAI API.

Prerequisites

- Python 3.8+
- An OpenAI API key in the `OPENAI_API_KEY` environment variable.

Setup


Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Environment

Create a `.env` file in the project root (or export env vars directly). A sample `.env` has been added; fill your key:

```text
OPENAI_API_KEY=sk-...
```

Then run the script as below.

Storing your API key

Create a `.env` file from `.env.example` and set your OpenAI API key directly. This project expects the plain API key available via the `OPENAI_API_KEY` environment variable (loaded from `.env` by `python-dotenv`), or exported in your shell. Do NOT commit `.env` to source control — keep it local and ignored.

Saving analysis output

Use `--output` (or `-o`) to write the analysis JSON to a file:

```bash
python analyze_log.py --file dummy_error.log --output analysis.json
```

Git / Security

- Do NOT commit your real secrets. This repository includes a `.env.example` with placeholder values; copy it to `.env` and fill your real key locally.
- The project provides a `.gitignore` that excludes `.env`, virtualenv directories, build artifacts, logs, and common editor files. Keep secrets out of source control.
- Example workflow:

```bash
# keep a copy of .env locally only
cp .env.example .env
# edit .env to add your key (this file is ignored by git)
# do NOT commit .env
```


Usage

```bash
export OPENAI_API_KEY="sk-..."
python analyze_log.py --file dummy_error.log
```

Options:

- `--file` / `-f`: path to the log file (default: `dummy_error.log`)
- `--model` / `-m`: model name to use (default: `gpt-4o-mini`)

What the script does

- Reads the provided log file.
- Sends the content to the OpenAI Chat Completion API with instructions to analyze and return a JSON summary containing detected error types, counts, example messages, and remediation suggestions.

Notes

- The script expects the `openai` Python package. The `requirements.txt` references `openai`.
- The model you select may affect response format. The script attempts to extract the first JSON block from the model response.

Step-by-step execution (recommended)

1) Create and activate a virtual environment (recommended):

```bash
# macOS / zsh
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3) Create your `.env` from the example and fill your real API key (DO NOT commit):

```bash
cp .env.example .env
# then edit .env and set OPENAI_API_KEY
```

4) (Optional) Keep your `.env` local and ignored; encryption tools are not required for this workflow.

5) Run the analyzer and print JSON to stdout:

```bash
python analyze_log.py --file dummy_error.log
```

6) Run the analyzer and save JSON to a file:

```bash
python analyze_log.py --file dummy_error.log --output analysis.json
```

7) (Optional) Use a different model or input file:

```bash
python analyze_log.py --file path/to/log.log --model gpt-4o-mini --output result.json
```

Troubleshooting

- If you see "Missing dependency", ensure you installed `requirements.txt` in the same Python environment.
- If the script prints an error asking for `OPENAI_API_KEY`, confirm the `.env` is present and contains your key or export it manually:

```bash
export OPENAI_API_KEY="sk-..."
```

- If the model response is not valid JSON, the script will return the raw model response under `raw_response` — try changing the `--model` or increasing `max_tokens` in `analyze_log.py`.

Security reminder

- Never commit real `OPENAI_API_KEY` values. Use `.gitignore` and `.env.example` as a template.
- Store encrypted `.env.enc` copies securely and manage passwords separately.

Quick start (one-liner)

Create a venv, install deps and run the analyzer in one line:

```bash
python -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt && cp .env.example .env && echo "OPENAI_API_KEY=sk-..." >> .env && python analyze_log.py --file dummy_error.log --output analysis.json
```

Example analyzer output

Below is a short example of the JSON the analyzer aims to produce (actual fields may vary):

```json
{
	"summary": "Detected 4 error types across 11 log lines.",
	"errors": [
		{
			"type": "db_connection_timeout",
			"count": 3,
			"earliest": "2025-12-14T09:14:10.001",
			"latest": "2025-12-14T09:25:00.001",
			"examples": ["Could not acquire connection from pool - timeout"],
			"severity": "high",
			"recommendation": "Investigate DB pool size and connectivity to 127.0.0.1:5432; add retry/backoff."
		},
		{
			"type": "auth_failure",
			"count": 3,
			"earliest": "2025-12-14T09:12:03.123",
			"latest": "2025-12-14T09:22:30.000",
			"examples": ["Failed to authenticate user 'alice' - invalid credentials"],
			"severity": "medium",
			"recommendation": "Check identity provider availability and token signing keys."
		}
	],
	"recommendations": ["Add DB connection monitoring", "Harden auth token validation"]
}
```

