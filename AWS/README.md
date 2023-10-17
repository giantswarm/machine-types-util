# AWS (CAPZ)

Fetches AWS EC2 instance type information to populate our capabilities information, mainly needed for Happa.

## Prerequisites

- Access to an AWS account
- The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed
- AWS session credentials in `~/.aws/credentials`

Ideally, check [our docs](https://intranet.giantswarm.io/docs/support-and-ops/ops-recipes/aws-cli-with-mfa/) on logging in with the AWS CLI and multi-factor authentication (MFA).

Execute `aws iam get-user` to verify that you are authenticated.

## Usage

1. Switch into the `AWS/` folder (the folder containing this README file) in the terminal.
2. Create a virtual python environment using `python3 -m venv venv` here in the AWS folder.
3. Activate the virtual environmnent using `source ./venv/bin/activate`
4. Install dependencies using `pip install -r requirements.txt`
5. Execute `python main.py`.

As a result, a YAML representation of the instance types data will be printed to standard output. This output can then be used in the giantswarm/config repository.
