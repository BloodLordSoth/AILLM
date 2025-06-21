import os
import sys
import subprocess
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_file_content, write_file, get_files_info
from functions.run_python import run_python_file

# Load API key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# CLI input handling
contentvalue = sys.argv[1] if len(sys.argv) > 1 else ""
verb = sys.argv[2] if len(sys.argv) > 2 else ""

if not contentvalue:
    print("Error: You must provide a user prompt as the first argument.")
    sys.exit(1)

# Gemini client setup
client = genai.Client(api_key=api_key)

# Define function schemas
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads specified file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we wish to read from.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes given content to specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we wish to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The message content that is being written."
            )
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the .py python file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file we are running.",
            ),
        },
    ),
)

# Tool list
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

# System prompt
system_prompt = """
You are a helpful AI coding agent.
You can:
- List files and directories
- Read file contents
- Execute Python files
- Write or overwrite files
Paths are relative and auto-secured to the working directory.
"""

# Call handler
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args or {}

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    args["working_directory"] = "./"

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

# Message history initialization
messages = [
    types.Content(role="user", parts=[types.Part(text=contentvalue)]),
]

# Main iteration loop
for i in range(20):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    print(f"\nIteration {i + 1}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Total tokens: {response.usage_metadata.total_token_count}")

    # Append all candidates to conversation
    function_called = False
    for candidate in response.candidates:
        messages.append(candidate.content)
        for part in candidate.content.parts:
            if part.function_call:
                function_called = True
                result = call_function(part.function_call, verbose=(verb == "--verbose"))
                messages.append(result)
                if verb == "--verbose":
                    print(f"-> {result.parts[0].function_response.response}")

    if not function_called:
        print("\nFinal response:")
        print(response.text)
        break
