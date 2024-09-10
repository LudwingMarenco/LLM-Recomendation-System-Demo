#!/bin/bash

# Check if wget is installed
if ! command -v wget &> /dev/null
then
    echo "wget could not be found, please install it first."
    exit 1
fi
mkdir -p models

url="https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q2_K.gguf"

destination="models/phi-2.Q2_K.gguf"

wget -O "$destination" "$url"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "File downloaded successfully to $destination"
else
    echo "Failed to download the file."
    exit 1
fi
