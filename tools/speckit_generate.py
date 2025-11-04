#!/usr/bin/env python3
"""Speckit spec generator

Usage:
  python tools/speckit_generate.py --feature "Feature Name" [--template spec-template.md] [--output docs/] [--commit]

This script reads templates from `.specify/templates/` and constitution from `.specify/memory/constitution.md`, replaces placeholders,
redacts secrets using configurable regex patterns, and writes the resulting markdown to the output directory.
It is safe by default and does not commit changes unless --commit is passed.
"""
import argparse
import os
import re
import sys
from datetime import datetime

# Add project root to the Python path to allow sibling imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from tools.lms_adapter import generate as generate_local
except ImportError:
    generate_local = None


DEFAULT_TEMPLATE = "spec-template.md"
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", ".specify", "templates")
CONSTITUTION_PATH = os.path.join(os.path.dirname(__file__), "..", ".specify", "memory", "constitution.md")


def load_template(template_name: str) -> str:
    path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_constitution() -> str:
    if not os.path.exists(CONSTITUTION_PATH):
        return ""
    with open(CONSTITUTION_PATH, "r", encoding="utf-8") as f:
        return f.read()


def redact_text(text: str, patterns) -> tuple:
    """Redact any occurrences of regex patterns. Returns (redacted_text, found_flag)."""
    found = False
    for patt in patterns:
        new_text, count = re.subn(patt, "<REDACTED>", text, flags=re.IGNORECASE)
        if count:
            found = True
        text = new_text
    return text, found


def default_patterns():
    # A conservative set of regex patterns to catch common secrets. These avoid overly-broad matches.
    return [
        # Discord bot token pattern (classic form)
        r"[MN][A-Za-z0-9_-]{23}\\.[A-Za-z0-9_-]{6}\\.[A-Za-z0-9_-]{27}",
        # Possible bot token without dots
        r"bot_[A-Za-z0-9-_]{20,}",
        # GitHub token patterns
        r"ghp_[A-Za-z0-9_]{36}",
        r"gho_[A-Za-z0-9_]{36}",
        # AWS Access Key ID
        r"AKIA[0-9A-Z]{16}",
        # Generic base64-like private key block (BEGIN PRIVATE KEY)
        r"-----BEGIN ([A-Z ]+ )?PRIVATE KEY-----[\s\S]+?-----END ([A-Z ]+ )?PRIVATE KEY-----",
        # Generic-looking long hex or base64 tokens
        r"[A-Za-z0-9_-]{40,}",
    ]


def replace_placeholders(template: str, context: dict) -> str:
    # Very simple placeholder replacements: [FEATURE NAME], [DATE], $ARGUMENTS etc.
    out = template
    out = out.replace("[FEATURE NAME]", context.get("feature_name", "<feature>"))
    out = out.replace("[DATE]", context.get("date", ""))
    out = out.replace("$ARGUMENTS", context.get("arguments", ""))
    # Add constitution inline if placeholder exists
    if "[CONSTITUTION]" in out:
        out = out.replace("[CONSTITUTION]", context.get("constitution", ""))
    return out


def generate_spec_body_local(feature_name: str, constitution: str) -> str:
    """Generate the spec body using the local LLM."""
    if not generate_local:
        return f"Could not import local LLM adapter. Please check `tools/lms_adapter.py`."

    prompt = f"""
You are a senior software engineer writing a technical specification document.
Your task is to generate the content for a spec about the feature: "{feature_name}".

Follow these rules from the project constitution:
---
{constitution}
---

Based on the feature name and the constitution, please generate a detailed specification.
Include sections for:
- **Overview**: A brief summary of the feature.
- **Requirements**: A list of functional and non-functional requirements.
- **Technical Design**: High-level technical implementation details.
- **Open Questions**: Any points that need further clarification.

Generate the full markdown content for the spec body.
"""
    print("Generating spec body with local LLM... (this may take a moment)")
    return generate_local(prompt)


def main(argv):
    parser = argparse.ArgumentParser(description="Speckit spec generator")
    parser.add_argument("--feature", required=True, help="Feature name/title")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE, help="Template filename (from .specify/templates)")
    parser.add_argument("--output", default="docs", help="Output directory")
    parser.add_argument("--commit", action="store_true", help="Commit generated files (use with caution)")
    parser.add_argument("--secrets-file", help="Optional file containing newline-separated regex patterns to redact")
    parser.add_argument("--use-local-llm", action="store_true", help="Use local LLM to generate spec body content")
    args = parser.parse_args(argv)

    template_text = load_template(args.template)
    constitution = load_constitution()

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:00 UTC")
    context = {
        "feature_name": args.feature,
        "date": now,
        "arguments": args.feature,
        "constitution": constitution,
    }

    if args.use_local_llm:
        # If using local LLM, we generate the body and inject it into the template
        spec_body = generate_spec_body_local(args.feature, constitution)
        context["feature_name"] = f"{args.feature} (AI Generated)"
        # A simple way to inject: assume template has a marker like [SPEC BODY]
        if "[SPEC BODY]" in template_text:
            output_text = template_text.replace("[SPEC BODY]", spec_body)
            output_text = replace_placeholders(output_text, context)
        else:
            # Fallback: just append to the template content
            output_text = replace_placeholders(template_text, context) + "\n\n---\n\n" + spec_body
    else:
        output_text = replace_placeholders(template_text, context)

    # Load extra patterns
    patterns = default_patterns()
    if args.secrets_file and os.path.exists(args.secrets_file):
        with open(args.secrets_file, "r", encoding="utf-8") as sf:
            custom = [line.strip() for line in sf if line.strip() and not line.startswith("#")]
            patterns = custom + patterns

    redacted_text, found = redact_text(output_text, patterns)

    os.makedirs(args.output, exist_ok=True)
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "-", args.feature).strip("-")[:80]
    out_path = os.path.join(args.output, f"{safe_name}-spec.md")
    with open(out_path, "w", encoding="utf-8") as out:
        header = f"<!-- Generated by speckit_generate.py on {now} -->\n\n"
        out.write(header)
        out.write(redacted_text)

    print(f"Wrote: {out_path}")
    if found:
        print("WARNING: Potential secrets redacted in output. Review <REDACTED> markers.")
    else:
        print("OK: No secret patterns found in generated output.")

    if args.commit:
        print("Commit requested, but this script will not perform commits in this environment.")


if __name__ == "__main__":
    main(sys.argv[1:])
