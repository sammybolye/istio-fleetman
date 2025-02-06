#!/bin/bash

# URL to fetch instance metadata
METADATA_URL="http://metadata.google.internal/computeMetadata/v1/instance/attributes/"
HEADER="Metadata-Flavor: Google"

# File where persistent environment variables will be stored
PROFILE_SCRIPT="/etc/profile.d/gce_metadata.sh"

# Clear the file to prevent duplicate entries
sudo bash -c "echo '#!/bin/bash' > $PROFILE_SCRIPT"

# Fetch the list of metadata keys
KEYS=$(curl -s -H "$HEADER" $METADATA_URL)

# Loop through each key and fetch its value
for KEY in $KEYS; do
  # Fetch value for the metadata key
  VALUE=$(curl -s -H "$HEADER" "${METADATA_URL}${KEY}")

  # Convert key to uppercase and replace hyphens with underscores
  ENV_KEY=$(echo "$KEY" | tr '[:lower:]' '[:upper:]' | tr '-' '_')

  # Export as an environment variable (current session)
  export "$ENV_KEY"="$VALUE"

  # Append to /etc/profile.d/gce_metadata.sh for persistence
  echo "export $ENV_KEY=\"$VALUE\"" | sudo tee -a $PROFILE_SCRIPT > /dev/null
done

# Ensure script is executable
sudo chmod +x $PROFILE_SCRIPT

echo "Metadata variables have been set and will persist across reboots."
