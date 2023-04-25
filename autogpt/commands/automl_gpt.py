"""Code evaluation module."""
from typing import List, Optional, Tuple
import subprocess
from autogpt.workspace import path_in_workspace
from autogpt.llm_utils import call_ai_function, generate_single_function_based_on_description
from autogpt.commands.file_operations import write_to_file
from autogpt.commands.execute_code import execute_python_file

def read_scan_understand_data_source(source: str) -> List[str]:
    """
    A function that takes in a string and returns a response from create chat
      completion api call.

    Parameters:
        code (str): Code to be evaluated.
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """

    function_name = "read_scan_understand_data_source"
    args = [source]
    description_string = (
       f"You have data source which is {source}. generate whole python code to scan and analyze the data, including name, shape, sample, distribution of the dataset. save the analyzed result in a file called {path_in_workspace('analyze_result.txt')} and return its content."
    )

    code_path = generate_single_function_based_on_description(function_name, args, description_string)
    if code_path:
        # Run the other script
        return subprocess.run(["python", code_path], capture_output=True, text=True)
    else:
        return "something is wrong, code is not generated, need human input"



def generate_models(input_source: str, target: str, suggestion: Optional[str]) -> str:
    """
    A function that takes in data schema, and return code that generates features.

    Parameters:
        schema: data schema in the format of string
    Returns:
        string of python code that produces features in pandas dataframe.
    """

    function_name = "generate_models"
    args = [input_source, target, suggestion]
    description_string = (
       f"""
       You have data source which is {input_source}. 
        "Given the variable name of the input dataframe, the schema of the dataframe and an ML target,"
        " generate python code that produce ML features and machine learning code  to predict {target} that maximize the accuracy."
        Return the result in a single python code block.
        """
    )

    description_string += f"Use these suggestions if applicable when generating code: {suggestion}" if suggestion else ""

    code_path = generate_single_function_based_on_description(function_name, args, description_string)
    if code_path:
        # Run the other script
        return subprocess.run(["python", code_path], capture_output=True, text=True)
    else:
        raise RuntimeError("something is wrong, code is not generated, need human input")


"""Code evaluation module."""
from typing import List

from autogpt.llm_utils import call_ai_function


def generate_features(source: str) -> List[str]:
    """
    A function that takes in a string and returns a response from create chat
      completion api call.

    Parameters:
        code (str): Code to be evaluated.
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """

    function_string = "def generate_features(source: str) -> List[str]:"
    args = [source]
    description_string = (
        "You have a data source like this. There is also a file called /tmp/analyze.txt which contains the stats describing this dataset. Now based on your understanding of the data (you can leverage external sources such as google to understand them a bit more). Based on your understanding and learning, generate features based on requirements."
    )

    return call_ai_function(function_string, args, description_string)



"""Code evaluation module."""
from typing import List

from autogpt.llm_utils import call_ai_function


def visualize_data(source: str) -> List[str]:
    """
    A function that takes in a string and returns a response from create chat
      completion api call.

    Parameters:
        code (str): Code to be evaluated.
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """

    function_string = "def visualize_data(source: str) -> List[str]:"
    args = [source]
    description_string = (
        "You have a data source like this. There is also a file called /tmp/analyze.txt which contains the stats describing this dataset. Now based on your understanding of the data (you can leverage external sources such as google to understand them a bit more). Based on your understanding and learning, visualize the data based on requirements"
    )

    return call_ai_function(function_string, args, description_string)



def improve_code_file(file_path: str, error_message: str) -> Tuple[str, str]:

    with open(file_path, 'r+') as file:
        # read from file
        code = file.read()

        function_string = (
            "def generate_improved_code(code: str, error_message: str) -> str:"
        )
        
        # use magic func to improve code.
        args = [code, error_message]
        description_string = (
            "Fix the provided code based on the error messages"
            " provided, making no other changes."
        )

        improved_code = call_ai_function(function_string, args, description_string)

        # write back to file
        file.seek(0)
        file.write(improved_code)

    return (file_path, improved_code)
