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
