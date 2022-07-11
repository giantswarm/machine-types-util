# Configuration

# Set this to a GCP project name that has the Compute API enabled.
GCP_PROJECT = 'testing-cluster-api'

# Set this to the zone you want to retrieve types for.
GCP_ZONE = 'europe-west1-b'

# Minimal number of CPUs required.
MINIMUM_CPUS = 4

# Minimal amount of RAM required, in MB.
MINIMUM_RAM_MB = 4000

# End of configuration

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


# Requesting the data from Google Cloud API

credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)
filter = f'guestCpus>={MINIMUM_CPUS} memoryMb>={MINIMUM_RAM_MB}'
request = service.machineTypes().list(project=GCP_PROJECT, zone=GCP_ZONE, filter=filter)

machine_types = []

while request is not None:
    response = request.execute()

    for machine_type in response['items']:
        machine_types.append({
            'description': machine_type['description'],
            'guestCpus': machine_type['guestCpus'],
            'name': machine_type['name'],
            'memoryMb': machine_type['memoryMb'],
        })

    request = service.machineTypes().list_next(previous_request=request, previous_response=response)

# Finally massaging the data into the format we need

# Sorting first by machine type family, then CPU, then RAM.
machine_types = sorted(machine_types, key=lambda k: (k['name'].split('-')[0], k['guestCpus'], k['memoryMb']))

keys = []
capabilities = {}
for item in machine_types:
    keys.append(item['name'])
    capabilities[item['name']] = {
        'description': item['description'],
        'guestCpus': item['guestCpus'],
        'memoryMb': item['memoryMb'],
    }

result = {
    'GCP': {
        'MachineTypes': {
            'Allowed': keys,
            'Capabilities': capabilities,
        }
    }
}

output = dump(result, Dumper=Dumper)

print('# YAML representation of GCP machine types:\n')
print(output)

