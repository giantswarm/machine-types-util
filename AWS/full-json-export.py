import json
import subprocess
import sys

import boto3
import botocore.exceptions

# These are the two regions we query for instance types,
# as experiments showed that together they have all of them.
REGIONS = ["us-east-1", "us-east-2"]


def get_credentials_from_cli(profile="default"):
    """Use 'aws configure export-credentials' to get credentials from an aws login session."""
    try:
        result = subprocess.run(
            ["aws", "configure", "export-credentials", "--profile", profile],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def get_session():
    """Create a boto3 session, prompting for a profile if needed."""
    profiles = boto3.Session().available_profiles

    if len(profiles) > 1:
        print("Available AWS profiles:", file=sys.stderr)
        for i, profile in enumerate(profiles, 1):
            print(f"  {i}. {profile}", file=sys.stderr)

        choice = input(f"Select a profile [1-{len(profiles)}]: ").strip()
        try:
            profile_name = profiles[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection.", file=sys.stderr)
            sys.exit(1)
    else:
        profile_name = "default"

    # First try creating a session with the profile directly (works for
    # standard credentials and SSO).
    session = boto3.Session(profile_name=profile_name)
    credentials = session.get_credentials()
    if credentials:
        try:
            credentials.get_frozen_credentials()
            return session
        except Exception:
            pass

    # Fall back to exporting credentials via the AWS CLI, which supports
    # 'aws login' sessions that boto3 doesn't understand natively.
    print(f"Resolving credentials for profile '{profile_name}' via AWS CLI...", file=sys.stderr)
    creds = get_credentials_from_cli(profile_name)
    if creds:
        return boto3.Session(
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds.get("SessionToken"),
        )

    print("No AWS credentials found. Please run 'aws login' to authenticate.", file=sys.stderr)
    sys.exit(1)


def main():
    session = get_session()

    instance_types = {}
    for region in REGIONS:
        ec2 = session.client('ec2', region_name=region)

        try:
            results = ec2.get_paginator("describe_instance_types").paginate().build_full_result()
        except botocore.exceptions.NoCredentialsError:
            print("No AWS credentials found. Please run 'aws login' to authenticate.", file=sys.stderr)
            sys.exit(1)
        except botocore.exceptions.ClientError as e:
            if "ExpiredToken" in str(e) or "InvalidClientTokenId" in str(e):
                print("AWS credentials have expired. Please run 'aws login' to re-authenticate.", file=sys.stderr)
                sys.exit(1)
            print(f"Failed to get instance types for {region}: {e}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"Failed to get instance types for {region}: {e}", file=sys.stderr)
            continue

        new_types = 0
        for instance_type in results["InstanceTypes"]:
            name = instance_type.pop("InstanceType")
            if name not in instance_types:
                instance_types[name] = instance_type
                new_types += 1

        print(f"Processed {region}, found {new_types} new types, {len(instance_types)} total", file=sys.stderr)

    sorted_types = dict(sorted(instance_types.items()))

    output_file = "instance_types.json"
    with open(output_file, "w") as f:
        json.dump(sorted_types, f, indent=2, default=str, sort_keys=True)
        f.write("\n")
    print(f"Wrote {len(sorted_types)} instance types to {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
