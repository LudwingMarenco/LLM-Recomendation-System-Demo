#!/bin/bash

model_folder="models"
mkdir -p $model_folder

if [ -d "$model_folder" ]; then
    if ls "$model_folder"/*.gguf 1> /dev/null 2>&1; then
        echo "Model already exist in the $model_folder."
    else
        ./get_model.sh
    fi
else
    echo "model_folder $model_folder does not exist."
    exit 1
fi

python3 src/movie_recommender/movie_recommender_main.py --config_file src/movie_recommender/config/movie_recommender.yaml