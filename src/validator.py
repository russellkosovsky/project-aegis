# src/validator.py

from jsonschema import validate
from jsonschema.exceptions import ValidationError

# This schema defines the rules for a valid network_config.yml file.
# It uses the standard JSON Schema format.
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        },
        "links": {
            "type": "array",
            "items": {
                "type": "array",
                # --- MODIFIED: Use prefixItems for tuple-like validation ---
                "prefixItems": [
                    {"type": "string"}, # From Node
                    {"type": "string"}, # To Node
                    {"type": "number"}  # Latency
                ],
                # --- Ensure no more than 3 items are in the array ---
                "minItems": 3,
                "maxItems": 3
            }
        }
    },
    "required": ["nodes", "links"]
}


def validate_config(config_data):
    """
    Validates a loaded YAML configuration against the defined schema.
    
    Args:
        config_data: The dictionary loaded from the YAML file.
        
    Returns:
        bool: True if validation is successful, False otherwise.
    """
    try:
        validate(instance=config_data, schema=CONFIG_SCHEMA)
        print("Configuration file format is valid.")
        return True
    except ValidationError as e:
        print("--- CONFIGURATION ERROR ---")
        print(f"Your network_config.yml file has a formatting error.")
        print(f"Error details: {e.message}")
        print(f"Please check the part of your config related to: {list(e.path)}")
        print("---------------------------")
        return False
    except Exception as e:
        # Catch other potential errors, like SchemaError during development
        print(f"--- VALIDATION SCHEMA ERROR ---")
        print(f"There is an issue with the validator.py schema itself: {e}")
        print("-------------------------------")
        return False
