from typing import Any
import copy

def json_to_typing_basic(schema: dict):

    # Copy so we don't start popping keys from the main description
    working_schema = copy.deepcopy(schema)

    # Get basic type (will be recursive for objects/arrays)
    json_type = working_schema.pop("type", "any")
    python_type = Any

    description = {}

    if json_type == "boolean":
        python_type = bool
    elif json_type == "integer":
        python_type = int
    elif json_type == "number":
        python_type = float
    elif json_type == "null":
        python_type = NoneType
    elif json_type == "string":
        python_type = str
    elif json_type == "object":
        python_type = dict
        description["properties"] = {k: json_to_typing_basic(v) for k, v in working_schema.pop("properties", {}).items()}
    elif json_type == "array":
        python_type = list
        description["items"] = json_to_typing_basic(working_schema.pop("items",{}))

    description["type"] = python_type

    # Add in extra unused parameters
    description.update(working_schema)

    return description