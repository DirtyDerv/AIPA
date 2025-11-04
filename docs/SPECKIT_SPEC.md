# Feature Specification: Speckit / GitHub Spec Kit Integration

**Feature Branch**: `speckit/integration`  
**Created**: 2025-11-04  
**Status**: Draft  
**Input**: Enable use of the repo's `.specify` and `.github/prompts` kit to generate and maintain specs, plans and checklists automatically.

## Summary

This spec describes how to onboard the Speckit/GitHub Spec Kit included in `.specify/` and `.github/prompts/` to produce reproducible feature specifications, plans and checklists for the AIPA project. Outputs are generated spec markdown files placed in `docs/` and optionally committed to a `speckit-generated` branch by a GitHub Action.

Goals:
- Make it easy to generate consistent feature specs using the included templates and prompts.
- Automate spec generation (optional) with a GitHub Action that runs the prompts and commits results to a branch for review.
- Keep secrets and credentials out of generated outputs and repository history.

## User Scenarios & Testing (mandatory)

### User Story 1 - Generate a feature spec from templates (Priority: P1)

As a developer, I want to use the `.specify/templates/` and `.specify/memory/constitution.md` to generate a filled feature spec so I can create a consistent plan for a new feature.

Why this priority: Core developer workflow - specs drive development, tests and acceptance criteria.

Independent Test: Run the generator script or copy templates and produce a `docs/<feature>-spec.md` file containing the required sections.

Acceptance Scenarios:
1. Given a feature name and description, when the generate command runs, then a spec file is created in `docs/` with populated sections.
2. Given templates exist, when a developer edits `docs/<feature>-spec.md`, then changes are retained and the generator does not overwrite without explicit flag.

---

### User Story 2 - Commit generated specs to a review branch (Priority: P2)

As a maintainer, I want an automated workflow to run speckit prompts and commit generated specs to a branch so reviewers can see proposals as pull requests.

Why this priority: Streamlines review and makes specs visible to collaborators.

Independent Test: Run the GH Action locally (or simulate) to verify a new branch `speckit-generated/<date>` is created and new files are committed.

Acceptance Scenarios:
1. Given a successful generation run, when the GH Action completes, then a branch with generated files exists and a PR can be opened manually.

---

### User Story 3 - Safe generation with secret-scan guard (Priority: P2)

As a security-conscious owner, I want the generator to skip or redact any file content that contains credentials so no secrets are accidentally committed.

Why this priority: Prevent accidental leakage of credentials discovered earlier in this repository.

Independent Test: Run the generator on current repo; ensure that any content matching known secret patterns is replaced with `<REDACTED>` and that the output contains no secret-like strings.

Acceptance Scenarios:
1. Given repository files that contain tokens, when generator runs, then generated spec does not include tokens and marks redacted sections.

---

### Edge Cases

- Templates missing required placeholders — generator should fail with a helpful error and not produce incomplete output.
- Multiple developers running the action simultaneously — generated branches should be timestamped or include a unique id to avoid conflicts.
- Large or binary files referenced in templates — generator should ignore non-text content.

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: The generator MUST read templates from `.specify/templates/` and `constitution.md` from `.specify/memory/`.
- **FR-002**: The generator MUST produce a markdown spec file under `docs/` named `<feature>-spec.md`.
- **FR-003**: The generator MUST support a CLI mode: `tools/speckit_generate.py --feature "Feature Name" --output docs/` (or PowerShell script provided in `.specify/scripts/powershell/`).
- **FR-004**: The generator MUST redact strings that match a configurable set of secret patterns before writing output (token regex, private keys, emails with certain patterns).
- **FR-005**: The GitHub Action (optional) MUST run the generator in a container or environment with no access to service_role keys, and must create a branch `speckit-generated/<timestamp>` and commit generated files.
- **FR-006**: Generated files MUST include a header comment with creation timestamp and generator version.

### Non-Functional Requirements

- **NFR-001**: Generation runtime MUST be under 30 seconds for plain text templates.
- **NFR-002**: The process MUST produce deterministic output given the same inputs.
- **NFR-003**: The generator MUST fail safely — not modify the repo unless an explicit `--commit` flag is passed.

### Key Entities

- **Template**: A markdown file under `.specify/templates/` containing placeholders to be replaced.
- **Constitution**: A repository-level context doc in `.specify/memory/constitution.md` that provides project principles used to populate specs.
- **Spec Output**: The generated markdown file in `docs/`.

## Success Criteria (mandatory)

### Measurable Outcomes

- **SC-001**: A generated spec file appears in `docs/` within 30s when the generator is run locally.
- **SC-002**: The GitHub Action (if enabled) creates a branch and commits generated files with no secrets present (verified via a local scan).
- **SC-003**: 0 incidents of secret leakage in generated files across 3 runs using a test dataset with seeded fake tokens.

## Implementation Plan & Tasks

This section contains a minimal plan to implement the generator and optional GH Action. Each item is independently testable.

1. Create a generator script (Python or PowerShell) that loads templates and replaces placeholders.
   - Owner: repo maintainer
   - Deliverable: `tools/speckit_generate.py` or `.specify/scripts/powershell/setup-plan.ps1` invocation

2. Implement a redaction routine supporting a configurable `secrets.json` of regex patterns.
   - Owner: security owner

3. Add a GitHub Actions workflow (optional): `.github/workflows/speckit-generate.yml` which runs on manual dispatch and schedules.
   - Action behaviour: checkout repo, run generator, run a local secret-scan, commit to `speckit-generated/<timestamp>` if no secrets found.

4. Create a short `docs/SPECKIT_README.md` documenting usage and safety checks.

5. Run tests: seed a test repo with fake tokens and verify redaction.

## Checklist (pre-merge)

- [ ] Generator script added to `tools/` and tested locally.
- [ ] Redaction patterns configured and tested.
- [ ] GitHub Action added (optional) and run manually once.
- [ ] `docs/SPECKIT_README.md` created and linked from `README.md`.
- [ ] No secret strings remain in generated output (run `git grep` on generated files).

## Notes & Constraints

- This spec prioritises safety: never commit secrets. The repo currently had a detected Discord token; generation MUST avoid including raw copies of that data.
- If you want, I can implement `tools/speckit_generate.py` and a GH Action — say the word and I'll create them and run local tests.

---

*Spec generated automatically from `.specify/templates/spec-template.md` and repo constitution on 2025-11-04.*
