from __future__ import annotations

import json
import subprocess
from autogpt.llm_utils import call_ai_function, generate_single_function_based_on_description


def generate_features_from_schema(input_source: str, target: str) -> str:
    """
    A function that takes in data schema, and return code that generates features.

    Parameters:
        schema: data schema in the format of string
    Returns:
        string of python code that produces features in pandas dataframe.
    """

    function_name = "generate_features_from_schema"
    args = [input_source, target]
    description_string = (
       f"""
       You have data source which is {input_source}. 
        "Given the variable name of the input dataframe, the schema of the dataframe and an ML target,"
        " generate python code that produce ML features that can achieve the target."
        " The produced features should be stored in a dataframe.
        Return the result in a single python code block
        """
    )

    code_path = generate_single_function_based_on_description(function_name, args, description_string)
    if code_path:
        # Run the other script
        return subprocess.run(["python", code_path], capture_output=True, text=True)
    else:
        raise RuntimeError("something is wrong, code is not generated, need human input")

    # function_string = (
    #     "def generate_features_from_schema(input_dataframe_name: str, schema: str, target: str) -> str:"
    # )
    # args = [input_dataframe_name, schema, target]
    # description_string = (
    #     "Given the variable name of the input dataframe, the schema of the dataframe and an ML target,"
    #     " generate python code that produce ML features that can achieve the target."
    #     " The produced features should be stored in a dataframe."
    #     " Return only the generated python code in a string."
    # )

    # return call_ai_function(function_string, args, description_string)
