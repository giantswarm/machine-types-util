# Google Cloud Platform (GCP)

## Prerequisites

- Personal access to a GCP project
- Google Compute API enabled in that GCP project. See [here](https://console.developers.google.com/apis/api/compute).

## Usage

1. Install the `gcloud` CLI as explained in the [documentation](https://cloud.google.com/sdk/docs/install-sdk).
2. Run `gcloud auth application-default login`
3. Switch into the `GCP/` folder.
4. Create a virtual python environment using `python3 -m venv venv` here in the GCP folder.
5. Activate the venv using `source ./venv/bin/activate`
6. Install dependencies using `pip install -r requirements.txt`
7. Execute `python main.py`.

As a result, a YAML representation of the machine types data will be printed to standard output. This output can then be used in the giantswarm/config repository.
