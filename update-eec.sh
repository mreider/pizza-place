#!/bin/bash

# Default file path
file="k8s/dynakube.yaml"

# Check if file exists
if [ ! -f "$file" ]; then
    echo "Error: File '$file' does not exist."
    exit 1
fi

# Prompt user for the new tag
read -p "Enter the new EEC tag: " new_tag

# Validate input
if [[ -z "$new_tag" ]]; then
    echo "Error: New tag cannot be empty."
    exit 1
fi

# Update the tag
sed -i '/extensionExecutionController:/,/tag:/s/\(tag: \).*/\1'"$new_tag"'/' "$file"

# Confirmation message
echo "Tag updated to '$new_tag' in file '$file'"