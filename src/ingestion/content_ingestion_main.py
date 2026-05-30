import argparse
from src.utils.content_utils import get_config
from src.ingestion.modules.content_ingest_module import ingest_text_dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type=str, dest="config", required=True)
    args = parser.parse_args()
    config = get_config(args.config)

    ingest_text_dataset(config=config)