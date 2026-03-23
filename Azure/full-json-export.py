import json
import subprocess
import sys

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

LOCATION = "westeurope"


def get_subscription_id():
    """Get the Azure subscription ID from the CLI."""
    try:
        result = subprocess.run(
            ["az", "account", "show", "--query", "id", "-o", "tsv"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except FileNotFoundError:
        pass

    print("Could not determine Azure subscription ID.", file=sys.stderr)
    print("Please run 'az login' to authenticate.", file=sys.stderr)
    sys.exit(1)


def main():
    subscription_id = get_subscription_id()
    print(f"Using subscription {subscription_id}", file=sys.stderr)

    client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
    )

    vm_types = {}

    print(f"Fetching resource SKUs for location '{LOCATION}'...", file=sys.stderr)
    skus = client.resource_skus.list(filter=f"location eq '{LOCATION}'")
    for sku in skus:
        if sku.resource_type != "virtualMachines":
            continue

        entry = sku.as_dict()
        name = entry.pop("name")
        vm_types[name] = entry

    sorted_types = dict(sorted(vm_types.items()))

    output_file = "vm_types.json"
    with open(output_file, "w") as f:
        json.dump(sorted_types, f, indent=2, default=str, sort_keys=True)
        f.write("\n")
    print(f"Wrote {len(sorted_types)} VM types to {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
