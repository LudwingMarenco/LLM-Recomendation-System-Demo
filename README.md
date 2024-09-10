# LLM Recomendation System Demo

## Overview

This repository provides a Python implementation of an LLM-based recommendation system using the LangChain pipeline. While the current pipeline is designed to recommend movies, it can be easily extended to other domains such as books.

## Features

- **Local LLM Deployment**: Run a lightweight LLM model locally.
- **API Integration**: Test the LLM recommendation system in real-time with API integration.
- **UI Interface Mesop Based**: Rapid deployment of a UI interface for direct interaction with the prompt engineering tasks.

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

3. **Run the LLM Recomendation System Demo**: Start the LLM Recommendation System Demo by executing:

    ```bash
    ./main.sh
    ```

4. **Run Mesop UI based interface**: In a separate terminal, deploy the UI interface for direct interaction with the LLM Recommendation System Demo by running:

    ```bash
    ./run_mesop.sh
    ```

### Running in container

1. **Build image**: Build and execute the images within a container by running:

    ```bash
    docker compose up --build
    ```
