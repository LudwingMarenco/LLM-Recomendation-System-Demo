#!/bin/bash

venv_name=movieenv

# Remove venv folder git tracking
if grep -q "$venv_name/" .gitignore; then
    :
else
    echo "$venv_name/" >> .gitignore
fi

# TODO: create check for url packages
# Create venv
if [[ "$VIRTUAL_ENV" != "" ]]
then
    echo "Virtual enviroment already create, please run movie_activate_venv.sh" 
else
    python3 -m venv $venv_name
    echo "export PYTHONPATH=$PWD" >> $venv_name/bin/activate
    source ./$venv_name/bin/activate
    pip3 install --upgrade pip setuptools wheel
    # pip3 install dvc[ssh]
    # pip install dvclive
    # pip3 install mlem
    pip3 install --no-cache-dir -r requirements.txt
    
fi
