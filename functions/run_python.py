import os
import sys
import subprocess

def run_python_file(working_directory, file_path):
    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_path.startswith(base_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            # Use unittest for test files
            if "test" in os.path.basename(file_path).lower():
                # Run as a unittest module
                cmd = [sys.executable, "-m", "unittest", file_path]
            else:
                # Run as a normal Python script
                cmd = [sys.executable, file_path, "main.py"]

            result = subprocess.run(
                cmd,
                timeout=30,
                cwd=base_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return f'STDOUT: {result.stdout} STDERR: {result.stderr}'

        except subprocess.TimeoutExpired:
            return f'Error: Execution timed out after 30 seconds'
        except Exception as q:
            return f'Error: {str(q)}'

    except Exception as e:
        return f'Error: {str(e)}'
