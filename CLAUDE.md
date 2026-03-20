# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo contains Python scripts that fetch VM/instance type data from cloud providers (AWS, Azure) and output YAML for use in the `giantswarm/config` repository. Each provider has its own independent directory with a `main.py`, `requirements.txt`, and `README.md`.

## Architecture

Two independent scripts, one per cloud provider, with no shared code:

- **AWS/** - Uses `boto3` to query EC2 instance types from `us-east-1` and `us-east-2`. Outputs `capabilities` keyed by instance type name.
- **Azure/** - Uses `azure-mgmt-compute` SDK. Requires a subscription ID set in `main.py` (`SUBSCRIPTION_ID`). Filters to specific VM families defined in `VM_FAMILIES` dict. Requires `az login`.

All scripts output YAML to stdout using PyYAML (with CDumper when available).

## Running a Script

Each provider follows the same pattern (run from within the provider directory):

```sh
cd <Provider>/
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```

Each requires active cloud credentials for its respective provider before execution.
