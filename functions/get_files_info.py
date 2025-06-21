import os, time


def get_files_info(working_directory, directory=None):
    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, directory or "."))

        # Guard: is the target_path within working_directory?
        if not target_path.startswith(base_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Guard: is it a directory?
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        # List contents
        entries = []
        for item in os.listdir(target_path):
            item_path = os.path.join(target_path, item)
            try:
                size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                entries.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')
            except Exception as e:
                entries.append(f'Error: Could not access "{item}": {str(e)}')

        return "\n".join(entries)

    except Exception as e:
        return f'Error: {str(e)}'
    
def get_file_content(working_directory, file_path):
    #try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_path.startswith(base_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        try:
            limit = 10000
            Arr = []
            with open(f'{target_path}', 'r') as f:
                readf = f.read()
                for i in readf:
                    if len(readf) >= limit:
                        Arr.append(readf)
                        return Arr, f'...File "{file_path}" truncated at 10000 characters'
                    else:
                        return readf, len(readf)
                
        except Exception as e:
            return f'Error: File not found or is not a regular file: "{file_path}"'
   

def write_file(working_directory, file_path, content):
    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not target_path.startswith(base_path):
            return f'Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"'

        # Create parent directories if they don't exist
        parent_dir = os.path.dirname(target_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # Write to the file
        with open(target_path, 'w') as f:
            f.write(content)

        return f'Successfully wrote to \"{file_path}\" ({len(content)} characters written)"'

    except Exception as e:
        return f'Error: {str(e)}'






    