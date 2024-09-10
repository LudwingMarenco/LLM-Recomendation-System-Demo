import argparse
from modules.movie_recommender_api import RecommenderAPI
from utils.movie_utils import get_config

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser()

    # Add a command-line argument for the config file
    parser.add_argument("--config_file", type=str, dest="config", required=True)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the configuration from the specified config file
    config = get_config(args.config)

    # Run LLM API
    recommender_api = RecommenderAPI(config)
    recommender_api.run()
