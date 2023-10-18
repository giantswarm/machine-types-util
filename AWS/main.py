
BYTES_IN_ONE_MIB = 1048576

# Minimal number of (v)CPUs required.
MINIMUM_CPUS = 2

# Minimal amount of RAM required, in MB.
MINIMUM_RAM_MB = 4000

import os
import boto3
import sys

from pprint import pprint

from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


client = boto3.client('account')

# These are the two regions we query for instance types,
# as experiments showed that together they have all of them.
regions = ["us-east-1", "us-east-2"]

# Collect instance types
capabilities = {}
for region in regions:
    ec2 = boto3.client('ec2', region_name=region)

    try:
        results = ec2.get_paginator("describe_instance_types").paginate().build_full_result()
    except Exception as e:
        print(f"Failed to get instance types for {region}: {e}")
        continue

    new_types = 0

    for instance_type in results["InstanceTypes"]:
        if instance_type["InstanceType"] in capabilities:
            continue
        
        record = {
            "cpu_cores": instance_type["VCpuInfo"]["DefaultVCpus"],
            "memory_size_gb": 0,
            "storage_size_gb": 0,
        }

        mem = instance_type["MemoryInfo"]["SizeInMiB"] * BYTES_IN_ONE_MIB / 1000.0 / 1000.0 / 1000.0
        mem_str = f"{mem:.2f}"
        record["memory_size_gb"] = float(mem_str)

        # Skip instance types with too few CPUs or RAM
        if record["cpu_cores"] < MINIMUM_CPUS or record["memory_size_gb"] < (MINIMUM_RAM_MB / 1000.0):
            continue

        try:
            record["storage_size_gb"] = instance_type["InstanceStorageInfo"]["TotalSizeInGB"]
        except KeyError:
            pass

        capabilities[instance_type["InstanceType"]] = record
        new_types += 1
    
    print(f"Processed {region}, found {new_types} new types, {len(capabilities.keys())} instance types total")

output = dump({"capabilities": capabilities}, Dumper=Dumper)
print("# YAML representation of EC2 instance types:\n")
print(output)
