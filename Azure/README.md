# Azure (CAPZ)

## Prerequisites

- Access to an Azure subscription.

## Usage

1. Install Azure CLI as explained in the [documentation](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
2. Run `az login`
3. Switch into the `Azure/` folder.
4. Create a virtual python environment using `python3 -m venv venv` here in the Azure folder.
5. Activate the venv using `source ./venv/bin/activate`
6. Install dependencies using `pip install -r requirements.txt`
7. Execute `python full-json-export.py`.

As a result, a JSON file with machine types data will be created in `vm_types.json`.
