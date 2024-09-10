#!/bin/bash

# Check if wget is installed
if ! command -v wget &> /dev/null
then
    echo "wget could not be found, please install it first."
    exit 1
fi

url="https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf"

destination="models/phi-2.Q4_K_M.gguf"

wget -O "$destination" "$url"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "File downloaded successfully to $destination"
else
    echo "Failed to download the file."
    exit 1
fi
