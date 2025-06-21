# AI Coding Agent

This project provides an AI coding agent that can interact with the file system, execute Python files, and write new files based on user prompts.

## Features

- List files and directories.
- Read file contents.
- Execute Python files.
- Write or overwrite files.

## Usage

Provide a user prompt as the first argument to the script. For example:

```bash
python main.py "List all files in the current directory."
```

You can also use the `--verbose` flag to get more detailed output:

```bash
python main.py "Read the contents of main.py." --verbose
```

## API Key

Make sure to set the `GEMINI_API_KEY` environment variable with your Gemini API key.

## Credits

BloodLordSoth 2025 - [https://github.com/BloodLordSoth](https://github.com/BloodLordSoth)