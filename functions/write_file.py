import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write the content into a file, warning: this will override the previous info in that file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "content to write into the file",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target_file_path: str = verify_file(working_directory, file_path)

        with open(target_file_path, "w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"{str(e)}"


def verify_file(working_directory: str, file_path: str) -> str:
    absolute_working_dir: str = os.path.abspath(working_directory)
    target_file_path: str = os.path.normpath(
        os.path.abspath(os.path.join(absolute_working_dir, file_path))
    )
    is_inside_working_dir: bool = (
        os.path.commonpath([absolute_working_dir, target_file_path])
        == absolute_working_dir
    )

    if not is_inside_working_dir:
        raise ValueError(
            f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        )

    if os.path.isdir(target_file_path):
        raise ValueError(f'Error: Cannot write to "{file_path}" as it is a directory')

    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    return target_file_path
