#!/bin/bash

venv_name=contentenv


if grep -q "$venv_name/" .gitignore; then
    :
else
    echo "$venv_name/" >> .gitignore
fi

if ! command -v pip &> /dev/null; then
    apt update && apt install --no-install-recommends --no-install-suggests --yes apt-transport-https ca-certificates curl gnupg lsb-release git python3-dev python3-pip python3-virtualenv
fi

if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

if [ -f "$HOME/.local/bin/env" ]; then
    source "$HOME/.local/bin/env"
else
    export PATH="$HOME/.local/bin:$PATH"
fi


if [ -f "$venv_name/bin/activate" ]; then
    echo "Virtual environment already exists. Activating $venv_name"
    source $venv_name/bin/activate
    if [ ! "$VIRTUAL_ENV" == "$(pwd)/$venv_name" ]; then
        echo "Invalid virtual environment $venv_name."
        deactivate 2>/dev/null || true
        echo "Removing invalid virtual environment $venv_name"
        rm -fr $venv_name || true
        echo "Creating a new virtual environment $venv_name"
        uv venv --python 3.10.11 $venv_name
        source $venv_name/bin/activate
    fi
else
    echo "Creating virtual environment $venv_name"
    rm -fr $venv_name || true
    uv venv --python 3.10.11 $venv_name
    source $venv_name/bin/activate
fi

# Validating virtual environment and Installing dependencies
if [ "$VIRTUAL_ENV" == "$(pwd)/$venv_name" ]; then
    echo "Virtual environment $venv_name is active. Installing project dependencies"
    uv pip install -r requirements.txt
else
    echo "Failed to activate virtual environment $venv_name."
    exit 1
fi