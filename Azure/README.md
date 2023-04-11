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
7. Replace `SUBSCRIPTION_ID` in `main.py` with a valid Azure subscription ID.
8. Execute `python main.py`.

As a result, a YAML representation of the machine types data will be printed to standard output. This output can then be used in the giantswarm/config repository.
