
from autogpt.llm_utils import call_ai_function
from typing import List

def deduce(context: str, question: str) -> str:
    """
    A magic function that deduce answer from context

    Parameters:
        context (str): The current information
        question (str): The question to answer
    Returns:
        Answer to the question deduced from the context.
    """

    function_string = "deduce(context: str, question: str) -> str:"
    args = [context, question]
    description_string = (
        "Based on the input context, try to deduce the answer to the question. Return the answer in a string."
    )

    return call_ai_function(function_string, args, description_string)
