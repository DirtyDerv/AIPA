<!-- Local copy / summary of https://github.com/github/spec-kit README (imported 2025-11-04) -->
# Spec Kit (summary)

Spec Kit is an open-source toolkit from GitHub that enables Spec-Driven Development: writing executable, high-quality specifications that drive implementation and testing. It provides templates, prompts, CLI tooling (`specify`), and integrations for AI-assisted workflows.

Key points:
- Purpose: Focus product scenarios and predictable outcomes rather than ad-hoc coding.
- Core deliverables: templates for specs, plans, checklists, tasks, and a project constitution (principles).
- CLI: `specify` (install via `uv tool` or use one-time execution). Key commands: `specify init`, `specify check`, and slash-like commands available via AI integration (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`, `/speckit.clarify`, `/speckit.analyze`, `/speckit.checklist`).
- Philosophy: Intent-first, test-first, iterative refinement, and AI-assistance for spec creation and execution.
- Safety: The toolkit emphasizes redaction and secret-safety; generated outputs should not contain credentials.
- Supported environments: Linux, macOS, Windows; Python 3.11+, git, and optional `uv` tool.

Recommended usage in this repo:
- Use local `.specify/templates/` and `.specify/memory/constitution.md` as the primary sources for generating specs.
- Run the PowerShell helper scripts under `.specify/scripts/powershell/` if on Windows (or convert to Python/bash as needed).
- Before committing generated files, run a local secret-scan and redact matches (the repo previously had a detected Discord token — be cautious).

References:
- Upstream project: https://github.com/github/spec-kit
- Documentation site: https://github.github.io/spec-kit/

Imported on: 2025-11-04
