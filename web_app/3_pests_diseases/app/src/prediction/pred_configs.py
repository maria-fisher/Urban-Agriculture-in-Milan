import yaml
from src.constants import PREDICTION_CONFIG_PATH

def save_crop_configs(data_dict : dict, key:str, filename = PREDICTION_CONFIG_PATH):
  
    """
    Saves a dictionary to a YAML file with the specified key.

    Args:
        data_dict (dict): The dictionary to be saved.
        filename (str): The filename of the YAML file.
        key (str): The key under which the data will be stored in the YAML file.
    """

    # Load existing data (or create an empty dictionary if file doesn't exist)
    try:
        with open(filename, 'r') as f:
            existing_data = yaml.safe_load(f)
    except FileNotFoundError:
        existing_data = {}

    # Overwrite or append data under the specified key (configurable)
    # Option 1: Overwrite (default)
    existing_data[key] = data_dict

    # Option 2: Append (if desired)
    # existing_data.setdefault(key, []).append(data_dict)

    # Write the updated data to the YAML file
    with open(filename, 'w') as f:
        yaml.dump(existing_data, f, default_flow_style=False) 


def get_crop_configs(key :str, filename = PREDICTION_CONFIG_PATH):
    """
    Loads data from a YAML file with the specified key.

    Args:
        filename (str): The filename of the YAML file.
        key (str): The key under which the data is stored in the YAML file.

    Returns:
        dict or None: The data associated with the key, or None if the key is not found.
    """

    # Try loading data from the YAML file
    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return None  # Return None if file doesn't exist

    # Return data associated with the key (or None if not found)
    return data.get(key)

def read_yaml(file_path):
    """
    Reads a YAML file and returns its contents as a dictionary.

    Parameters:
    file_path (str): The path to the YAML file.

    Returns:
    dict: The contents of the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except yaml.YAMLError as exc:
        print(f"Error in YAML file: {exc}")
