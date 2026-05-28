#!/bin/bash

venv_name=contentenv

if [ -f "$venv_name/Scripts/activate" ]; then 
   source $venv_name/Scripts/activate 
elif [ -f "$venv_name/bin/activate" ]; then  
    source $venv_name/bin/activate 
else    
   echo "Activation script not found in expected locations (tupyenv/Scripts or tupyenv/bin)."
fi
source $venv_name/bin/activate