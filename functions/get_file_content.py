import os

from config import MAX_FILE_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "read the contents of the selected file, must be used when prompted to read the contents of any file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_file = verify_get_file_content(working_directory, file_path)

        with open(target_file, "r") as file:
            file_content = file.read(MAX_FILE_CHARS)
            extra_character = file.read(1)

            if extra_character:
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
                )

        return file_content

    except Exception as e:
        return f"Error: {str(e)}"


def verify_get_file_content(working_directory: str, file_path: str) -> str:
    absolute_working_dir: str = os.path.abspath(working_directory)
    absolute_target_path: str = os.path.normpath(
        os.path.abspath(os.path.join(absolute_working_dir, file_path))
    )
    is_inside_working_dir: bool = (
        os.path.commonpath([absolute_working_dir, absolute_target_path])
        == absolute_working_dir
    )
    is_file: bool = os.path.isfile(absolute_target_path)
    if not is_inside_working_dir:
        raise ValueError(
            f'Cannot read "{file_path}" as it is outside the permitted working directory'
        )

    if not is_file:
        raise ValueError(f' File not found or is not a regular file: "{file_path}"')

    return absolute_target_path
