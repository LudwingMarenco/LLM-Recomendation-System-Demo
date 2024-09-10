import yaml

def get_config(config_file: str):
    """
    Load and parse a YAML configuration file.

    Parameters:
    - config_file (str): The path to the YAML configuration file.

    Returns:
    - dict: The parsed configuration as a dictionary.
    """
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config