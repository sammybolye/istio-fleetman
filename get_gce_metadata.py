#!/usr/bin/env python3

import os
import requests

# GCE Metadata Server URL
METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/instance/attributes/"
HEADERS = {"Metadata-Flavor": "Google"}

# Output file to store environment variables
PROFILE_SCRIPT = os.path.expanduser("~/.gce_metadata_env")

def fetch_metadata():
    """Fetches instance metadata attributes from the GCE metadata server."""
    try:
        response = requests.get(METADATA_URL, headers=HEADERS, timeout=5)
        response.raise_for_status()
        keys = response.text.strip().split("\n")

        metadata = {}
        for key in keys:
            value_response = requests.get(METADATA_URL + key, headers=HEADERS, timeout=5)
            value_response.raise_for_status()
            metadata[key] = value_response.text.strip()
        
        return metadata
    except requests.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return {}

def save_metadata(metadata):
    """Saves metadata as environment variables to a script for persistent use."""
    with open(PROFILE_SCRIPT, "w") as f:
        f.write("#!/bin/bash\n")
        for key, value in metadata.items():
            env_key = key.upper().replace("-", "_")  # Convert to uppercase, replace hyphens
            f.write(f'export {env_key}="{value}"\n')

    # Ensure the script is readable
    os.chmod(PROFILE_SCRIPT, 0o644)

    # Add sourcing to .bashrc if not already added
    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, "a") as bashrc:
        if f"source {PROFILE_SCRIPT}" not in open(bashrc_path).read():
            bashrc.write(f"\nsource {PROFILE_SCRIPT}\n")

    print(f"Metadata environment variables saved to {PROFILE_SCRIPT} and sourced in ~/.bashrc")

def main():
    metadata = fetch_metadata()
    if metadata:
        save_metadata(metadata)
        # Load metadata immediately using bash explicitly
        os.system(f"bash -c 'source {PROFILE_SCRIPT}'")
    else:
        print("No metadata retrieved.")

if __name__ == "__main__":
    main()
