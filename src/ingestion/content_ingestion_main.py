import argparse
from src.utils.content_utils import get_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type=str, dest="config", required=True)
    args = parser.parse_args()

    
    config = get_config(args.config)

    print(config)
    print("ok")