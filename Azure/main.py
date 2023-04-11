SUBSCRIPTION_ID = "PLACEHOLDER"

LOCATION = "westeurope"

MINIMUM_CPUS = 2

# Keys should match the value of the Azure Resource SKU "family" key.
VM_FAMILIES = {
    "standardDSv3Family": {
        "name": "DSv3-series",
        "type": "general purpose",
    },
    "standardDv5Family": {
        "name": "Dv5-series",
        "type": "general purpose"
    },
    "standardDSv5Family": {
        "name": "Dsv5-series",
        "type": "general purpose"
    },
    "standardNCSv3Family": {
        "name": "NCv3-series",
        "type": "GPU - accelerated compute"
    },
    "Standard NCASv3_T4 Family": {
        "name": "NCasT4_v3-series",
        "type": "GPU - accelerated compute"
    },
}

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

def main():
    client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID,
        )

    capabilities = {}

    vms = client.resource_skus.list(filter=f"location eq '{LOCATION}'")
    for vm in vms:
        if vm.resource_type == "virtualMachines" and vm.family in VM_FAMILIES.keys():
            vm_info = {
                "description": f"{VM_FAMILIES[vm.family]['name']}, {VM_FAMILIES[vm.family]['type']}"
            }
            capabilities[vm.name] = vm_info


    vms = client.virtual_machine_sizes.list(location=LOCATION)

    for vm in vms:
        if vm.name in capabilities and vm.number_of_cores >= MINIMUM_CPUS:
            vm_info = {
                **capabilities[vm.name],
                'additionalProperties': vm.additional_properties,
                'maxDataDiskCount': vm.max_data_disk_count,
                'memoryInMb': vm.memory_in_mb,
                'name': vm.name,
                'numberOfCores': vm.number_of_cores,
                'osDiskSizeInMb': vm.os_disk_size_in_mb,
                'resourceDiskSizeInMb': vm.resource_disk_size_in_mb
            }
            capabilities[vm.name] = vm_info

    capabilities = dict(sorted(capabilities.items(), key=lambda x: x[0]))

    result = {
        "vm": {
            "default": "Standard_D2s_v3",
            "allowed": [k for k in capabilities.keys()],
            "capabilities": capabilities,
        }
    }

    output = dump(result, Dumper=Dumper)

    print("# YAML representation of Azure machine types:\n")
    print(output)


if __name__ == "__main__":
    main()