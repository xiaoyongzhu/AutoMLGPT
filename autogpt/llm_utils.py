from __future__ import annotations

import time
import re
from ast import List
import os
import openai
from colorama import Fore, Style
from openai.error import APIError, RateLimitError
from autogpt.workspace import path_in_workspace
import time
from autogpt.config import Config
from autogpt.logs import logger

CFG = Config()

openai.api_key = CFG.openai_api_key


def call_ai_function(
    function: str, args: list, description: str, model: str | None = None
) -> str:
    """Call an AI function

    This is a magic function that can do anything with no-code. See
    https://github.com/Torantulino/AI-Functions for more info.

    Args:
        function (str): The function to call
        args (list): The arguments to pass to the function
        description (str): The description of the function
        model (str, optional): The model to use. Defaults to None.

    Returns:
        str: The response from the function
    """
    if model is None:
        model = CFG.smart_llm_model
    # For each arg, if any are None, convert to "None":
    args = [str(arg) if arg is not None else "None" for arg in args]
    # parse args to comma separated string
    args = ", ".join(args)
    messages = [
        {
            "role": "system",
            "content": f"You are now the following python function: ```# {description}"
            f"\n{function}```\n\nOnly respond with your `return` value.",
        },
        {"role": "user", "content": args},
    ]

    return create_chat_completion(model=model, messages=messages, temperature=0)



def generate_file_based_on_input(
    function: str, args: List, description: str, model: Optional[str] = None
) -> str:
    """Call an AI function

    This is a magic function that can do anything with no-code. See
    https://github.com/Torantulino/AI-Functions for more info.

    Args:
        function (str): The function to call
        args (list): The arguments to pass to the function
        description (str): The description of the function
        model (str, optional): The model to use. Defaults to None.

    Returns:
        str: The response from the function
    """
    if model is None:
        model = CFG.smart_llm_model
    # For each arg, if any are None, convert to "None":
    args = [str(arg) if arg is not None else "None" for arg in args]
    # parse args to comma separated string
    args = ", ".join(args)
    messages = [
        {
            "role": "system",
            "content": f"You are now the following python function: ```# {description}"
            f"\n{function}```\n\nOnly respond with your `return` value.",
        },
        {"role": "user", "content": args},
    ]

    return create_chat_completion(model=model, messages=messages, temperature=0)


def generate_single_function_based_on_description(
    function: str, args: List, description: str, model: Optional[str] = None
) -> str:
    """Call an AI function

    This is a magic function that can do anything with no-code. See
    https://github.com/Torantulino/AI-Functions for more info.

    Args:
        function (str): The function to call
        args (list): The arguments to pass to the function
        description (str): The description of the function
        model (str, optional): The model to use. Defaults to None.

    Returns:
        str: The response from the function
    """
    if model is None:
        model = CFG.smart_llm_model
    # For each arg, if any are None, convert to "None":
    # parse args to comma separated string
    system_prompt = """
    You are a helpful code assistant.

    """
    misc_requirements = """    
    - if asked to do feature engineering, Don't just use the original columns. Always use some sort of combination of the columns, or transformation/aggregation of the columns. Use pandas to do all the work
    - if asked to do feature engineering,  Make sure the original columns exist when you generate all the features.
    - if asked to do feature engineering,  If using divisions, make sure there's no zeros in the Divisor
    - If asked to generate a distribution graph, the x axis max should be the 99.5% percentile of the data and the min should be 0.5% percentile of the data in case of outliers
    - make sure import all the packages that are needed such as numpy
    """
    user_input = f"Write a python function, the function name should be called {function}, the input would be {args}, and the description is {description}"
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": user_input + misc_requirements},
    ]

    response = create_chat_completion(model=model, messages=messages, temperature=0)
    # Get the current time and seconds
    current_time = time.localtime()
    current_time_str = time.strftime("%Y%m%d_%H%M%S", current_time)
    with open(path_in_workspace(f"result_{current_time_str}.txt"), 'w') as file:
        file.write(response)

    # if the function is returned without being put into a code block
    if response.startswith(f"def {function}"):
        generated_code = response
    else:
        generated_code = extract_code(
            response)["python"] or extract_code(response)["sql"]
    # Create the filename with the current time and seconds

    file_name = path_in_workspace(f"generated_{function}_{current_time_str}.py")
    with open(file_name, 'w') as file:
        file.write(generated_code)
    return file_name if generated_code else  ""


def extract_code(input_string):
    # import re
    # Initialize a dictionary to store the code blocks for each language
    code_blocks = {
        'python': [],
        'sql': []
    }

    # Define regular expression patterns for Python and SQL code blocks
    pattern_python = r"```python(.*?)```"
    pattern_sql = r"```sql(.*?)```"

    # Extract Python code blocks using the regular expression pattern
    matches = re.findall(pattern_python, input_string, re.DOTALL)
    for match in matches:
        # Remove leading/trailing whitespaces and append the match to the list
        code_blocks['python'].append(match.strip())

    # Extract SQL code blocks using the regular expression pattern
    matches = re.findall(pattern_sql, input_string, re.DOTALL)
    for match in matches:
        # Remove leading/trailing whitespaces and append the match to the list
        code_blocks['sql'].append(match.strip())

    # Combine code blocks into single strings using newline as separator
    code_blocks['python'] = '\n'.join(code_blocks['python'])
    code_blocks['sql'] = '\n'.join(code_blocks['sql'])

    # Return the dictionary containing the code blocks for both languages
    return code_blocks

# Overly simple abstraction until we create something better
# simple retry mechanism when getting a rate error or a bad gateway
def create_chat_completion(
    messages: list,  # type: ignore
    model: str | None = None,
    temperature: float = CFG.temperature,
    max_tokens: int | None = None,
) -> str:
    """Create a chat completion using the OpenAI API

    Args:
        messages (list[dict[str, str]]): The messages to send to the chat completion
        model (str, optional): The model to use. Defaults to None.
        temperature (float, optional): The temperature to use. Defaults to 0.9.
        max_tokens (int, optional): The max tokens to use. Defaults to None.

    Returns:
        str: The response from the chat completion
    """
    response = None
    num_retries = 10
    warned_user = False
    if CFG.debug_mode:
        print(
            Fore.GREEN
            + f"Creating chat completion with model {model}, temperature {temperature},"
            f" max_tokens {max_tokens}" + Fore.RESET
        )
    for attempt in range(num_retries):
        backoff = 2 ** (attempt + 2)
        try:
            if CFG.use_azure:
                response = openai.ChatCompletion.create(
                    deployment_id=CFG.get_azure_deployment_id_for_model(model),
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            else:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            break
        except RateLimitError:
            if CFG.debug_mode:
                print(
                    Fore.RED + "Error: ",
                    f"Reached rate limit, passing..." + Fore.RESET,
                )
            if not warned_user:
                logger.double_check(
                    f"Please double check that you have setup a {Fore.CYAN + Style.BRIGHT}PAID{Style.RESET_ALL} OpenAI API Account. "
                    + f"You can read more here: {Fore.CYAN}https://github.com/Significant-Gravitas/Auto-GPT#openai-api-keys-configuration{Fore.RESET}"
                )
                warned_user = True
        except APIError as e:
            if e.http_status == 502:
                pass
            else:
                raise
            if attempt == num_retries - 1:
                raise
            if CFG.debug_mode:
                print(e)
        if CFG.debug_mode:
            print(
                Fore.RED + "Error: ",
                f"API Bad gateway... Waiting {backoff} seconds..." + Fore.RESET,
            )
        time.sleep(backoff)
    if response is None:
        logger.typewriter_log(
            "FAILED TO GET RESPONSE FROM OPENAI",
            Fore.RED,
            "Auto-GPT has failed to get a response from OpenAI's services. "
            + f"Try running Auto-GPT again, and if the problem the persists try running it with `{Fore.CYAN}--debug{Fore.RESET}`.",
        )
        logger.double_check()
        if CFG.debug_mode:
            raise RuntimeError(f"Failed to get response after {num_retries} retries")
        else:
            quit(1)

    return response.choices[0].message["content"]


def create_embedding_with_ada(text) -> list:
    """Create an embedding with text-ada-002 using the OpenAI SDK"""
    num_retries = 10
    for attempt in range(num_retries):
        backoff = 2 ** (attempt + 2)
        try:
            if CFG.use_azure:
                return openai.Embedding.create(
                    input=[text],
                    engine=CFG.get_azure_deployment_id_for_model(
                        "text-embedding-ada-002"
                    ),
                )["data"][0]["embedding"]
            else:
                return openai.Embedding.create(
                    input=[text], model="text-embedding-ada-002"
                )["data"][0]["embedding"]
        except RateLimitError:
            pass
        except APIError as e:
            if e.http_status == 502:
                pass
            else:
                raise
            if attempt == num_retries - 1:
                raise
        if CFG.debug_mode:
            print(
                Fore.RED + "Error: ",
                f"API Bad gateway.. Waiting {backoff} seconds..." + Fore.RESET,
            )
        time.sleep(backoff)
