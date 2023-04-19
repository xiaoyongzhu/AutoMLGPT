from __future__ import annotations

import json

from autogpt.llm_utils import call_ai_function


def generate_features_from_schema(input_dataframe_name: str, schema: str, target: str) -> str:
    """
    A function that takes in data schema, and return code that generates features.

    Parameters:
        schema: data schema in the format of string
    Returns:
        string of python code that produces features in pandas dataframe.
    """

    function_string = (
        "def generate_features_from_schema(input_dataframe_name: str, schema: str, target: str) -> str:"
    )
    args = [input_dataframe_name, schema, target]
    description_string = (
        "Given the variable name of the input dataframe, the schema of the dataframe and an ML target,"
        " generate python code that produce ML features that can achieve the target."
        " The produced features should be stored in a dataframe."
        " Return only the generated python code in a string."
    )

    return call_ai_function(function_string, args, description_string)
