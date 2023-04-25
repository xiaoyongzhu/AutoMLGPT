"""Code evaluation module."""
from __future__ import annotations

from autogpt.llm_utils import call_ai_function


def analyze_code(code: str, error_message: str) -> list[str]:
    """
    A function that takes in a string and returns a response from create chat
      completion api call.

    Parameters:
        code (str): Code to be evaluated.
        error_message (str): Optional error message from previous run
    Returns:
        A result string from create chat completion. A list of suggestions to
            improve the code.
    """

    function_string = "def analyze_code(code: str, error_message: Optional[str]) -> List[str]:"
    args = [code, error_message]
    description_string = (
        "Analyzes the given code and optinall error message from previous run, "
        "and returns a list of suggestions for improvements."
    )

    return call_ai_function(function_string, args, description_string)
