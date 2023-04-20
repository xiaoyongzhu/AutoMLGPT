"""Code evaluation module."""
from typing import List
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
