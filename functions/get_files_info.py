import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_directory = validate_directory(working_directory, directory)
        files = []
        for file in os.listdir(target_directory):
            files.append(
                f"- {file}: file_size={os.path.getsize(os.path.join(target_directory, file))}, is_dir={os.path.isdir(os.path.join(target_directory, file))}\n"
            )

        return "".join(files)
    except Exception as e:
        return f"{str(e)}"


def validate_directory(working_directory: str, directory: str = ".") -> str:
    absolute_working_directory: str = os.path.abspath(working_directory)
    target_directory: str = os.path.normpath(
        os.path.join(absolute_working_directory, directory)
    )

    is_valid_target_directory: bool = (
        os.path.commonpath([absolute_working_directory, target_directory])
        == absolute_working_directory
    )

    if not is_valid_target_directory:
        raise ValueError(
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        )

    if not os.path.isdir(target_directory):
        raise ValueError(f'Error: "{directory}" is not a directory')

    return target_directory
