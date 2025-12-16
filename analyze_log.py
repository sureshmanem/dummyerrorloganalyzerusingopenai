#!/usr/bin/env python3
"""analyze_log.py

Small utility that reads an error log and asks the OpenAI API to analyze it.
Produces a JSON summary of distinct error types, counts, timestamps, examples, and recommendations.

Usage:
  pip install -r requirements.txt
  export OPENAI_API_KEY="..."
  python analyze_log.py --file dummy_error.log
"""
import os
import re
import json
import argparse
import sys

try:
    from openai import OpenAI
except Exception:
    print("Missing dependency 'openai'. Install with: pip install -r requirements.txt")
    raise
try:
    from dotenv import load_dotenv
except Exception:
    print("Missing dependency 'python-dotenv'. Install with: pip install -r requirements.txt")
    raise

# Load environment variables from .env if present
load_dotenv()


def call_openai_chat(messages, model):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)

    # Instantiate client with the API key (keeps client creation local and avoids undefined variables)
    client = OpenAI(api_key=api_key)

    # Use Chat Completions endpoint from the OpenAI client
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1500,
    )

    # Access response content safely
    try:
        return resp.choices[0].message.content
    except Exception:
        # fallback to dict-like access
        try:
            return resp["choices"][0]["message"]["content"]
        except Exception:
            return str(resp)


def extract_first_json_block(text):
    # Finds the first {...} or [...] block in the string and tries to parse it as JSON.
    m = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    if not m:
        return None
    block = m.group(1)
    try:
        return json.loads(block)
    except Exception:
        return None


def analyze_log_text(log_text, model):
    system = (
        "You are an assistant that analyzes application error logs. "
        "Given a log, identify distinct error types, count occurrences, provide earliest and latest timestamps for each type, "
        "give one or two example messages for each type, estimate severity (low/medium/high), and provide remediation suggestions. "
        "Return a JSON object only. The JSON must include keys: 'errors' (array), 'summary' (string), 'recommendations' (array).")

    user = (
        "Analyze the following log. Output JSON only.\n\nLOG:\n" + log_text
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    resp_text = call_openai_chat(messages, model)
    parsed = extract_first_json_block(resp_text)
    if parsed is not None:
        return parsed

    # Fallback: return raw text if parsing failed
    return {"raw_response": resp_text}


def main():
    parser = argparse.ArgumentParser(description="Analyze an error log using the OpenAI API")
    parser.add_argument("--file", "-f", default="dummy_error.log", help="Path to the log file")
    parser.add_argument("--model", "-m", default="gpt-4o-mini", help="OpenAI model to use (default: gpt-4o-mini)")
    parser.add_argument("--output", "-o", default=None, help="Path to write JSON output (optional)")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: log file '{args.file}' not found.")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as fh:
        log_text = fh.read()

    result = analyze_log_text(log_text, args.model)

    # Pretty-print JSON result
    pretty = json.dumps(result, indent=2, ensure_ascii=False)
    print(pretty)

    if args.output:
        out_path = args.output
        try:
            with open(out_path, "w", encoding="utf-8") as ofh:
                ofh.write(pretty)
            print(f"Wrote analysis JSON to: {out_path}")
        except Exception as exc:
            print(f"Failed to write output file {out_path}: {exc}")


if __name__ == "__main__":
    main()
