# LLM Recomendation System Demo

## Overview

This repository contains python implementation which OpenCV framework for detecting and recognizing faces using models from model zoo.

## Features

- **Multiple Face Detection**: Capable of detecting multiple faces simultaneously.
- **Constrained Face Recognition**: Recognition process is limited to using a single photo per person.
- **Real-time Face Database Update**: Ability to update the face database in real-time. New face photos can be added, and the module updates dynamically while running.

## How to use it?

### Running locally

1. **Set Up Virtual Environment**: Create a virtual environment to manage dependencies cleanly by running

    ```bash
    ./scripts/movie_create_venv.sh
    ```

2. **Activate virtual envinroment**: Activate your virtual environment. You can do this by running:

    ```bash
     source scripts/movie_activate_venv.sh
    ```

3. **Run the LLM Recomendation System Demo**: Execute the following command within your virtual environment to start the LLM Recomendation System Demo:

    ```bash
    ./main.sh
    ```

4. **Run Mesop UI based interface**: Execute the following command within your virtual environment in another terminal to deploy UI interfce for direclty interact with the LLM Recomendation System Demo

    ```bash
    ./run_mesop.sh
    ```

### Running in container

1. **Build image**: Build and execute the images within a container by running:

    ```bash
    docker compose up --build
    ```
