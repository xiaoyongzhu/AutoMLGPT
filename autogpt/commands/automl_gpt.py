"""Code evaluation module."""
from typing import List

from autogpt.llm_utils import call_ai_function, extract_code
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

    function_string = "def read_scan_understand_data_source(code: str) -> List[str]:"
    args = [source]
    description_string = (
        "You have a data source like this. generate whole python code to scan and analyze the data, including name, shape, dtypes, sample, distribution, missing values, unique values, and other info that may help on the data analytics of the dataset. save the analyzed result in a file called /tmp/analyze.txt and return the content of /tmp/analyze.txt"
    )

    res = call_ai_function(function_string, args, description_string)
    print("res", call_ai_function(function_string, args, description_string))
    code = extract_code(res)
    print("extract code",code)
    write_to_file("/tmp/read_scan_understand_data_source_generated.py", code)
    execute_python_file("/tmp/read_scan_understand_data_source_generated.py")
    return "success"



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
