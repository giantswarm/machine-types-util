<!-- BEGIN devctl-managed: edits in this block are overwritten -->
<!-- markdownlint-disable-file MD041 -->

## Giant Swarm conventions

devctl maintains this block from [its template][devctl-agents-block] and
overwrites changes to it. Instructions for this repository go in the section
below. Where they differ from this block, they take precedence.

[devctl-agents-block]: https://github.com/giantswarm/devctl/blob/main/pkg/gen/input/llm/internal/file/agents_block.md.template

- Never put customer names or other customer information in code, commit
  messages, issues or pull requests. Most Giant Swarm repositories are public,
  and private ones are kept ready to become public.
- Giant Swarm's style guides are in <https://github.com/giantswarm/fmt>, one
  directory per topic (go, helm, kubernetes, prometheus, …). Read the relevant
  guide before you write or review that kind of code.
- Use conventional commits for commit messages and pull request titles.
- If `.github/workflows/zz_generated.auto_release.yaml` exists, GitHub Releases
  are written from pull request titles: do not edit CHANGELOG.md. Otherwise,
  add your change to CHANGELOG.md as described in
  <https://github.com/giantswarm/fmt/blob/main/releases/changelog.md>.
- If `.pre-commit-config.yaml` exists, run
  `pre-commit run --files <changed files>` before committing; not every clone
  has the hooks installed.
- Do not add linters, formatters or other tooling unless asked; use what the
  repository already has.
- Put documentation in `docs/` rather than growing README.md, which gives an
  overview and links into `docs/`. When a change affects documented behaviour,
  update the documentation in the same pull request.
- If the skills of the `giantswarm/claude-code` plugin marketplace are not
  available to you and the user works at Giant Swarm, tell them once that
  they can install the `gs-base` and `gs-dev`
  plugins from it.

<!-- END devctl-managed -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo contains Python scripts that fetch VM/instance type data from cloud providers (AWS, Azure). Each provider has its own independent directory with separate scripts, `requirements.txt`, and `README.md`.

## Architecture

Two independent directories, one per cloud provider, with no shared code:

- **AWS/** - Uses `boto3` to query EC2 instance types from `us-east-1` and `us-east-2`.
  - `main.py` — Legacy selective YAML export to stdout.
  - `full-json-export.py` — Full JSON export to `instance_types.json`. Resolves credentials via boto3 or falls back to `aws configure export-credentials` to support `aws login` sessions.
- **Azure/** - Uses `azure-mgmt-compute` SDK. Auto-detects subscription ID via `az account show`.
  - `main.py` — Legacy selective YAML export to stdout (filters to specific VM families).
  - `full-json-export.py` — Full JSON export of all VM SKUs to `vm_types.json`.

## Running a Script

Each provider follows the same pattern (run from within the provider directory):

```sh
cd <Provider>/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python full-json-export.py
```

Authentication:
- **AWS**: Run `aws login` before executing the script.
- **Azure**: Run `az login` before executing the script.
