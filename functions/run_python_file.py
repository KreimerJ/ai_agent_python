import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file in the specified directory, optionally with arguments. Use this whenever you are told to run something in Python.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of arguments to pass to the Python file",
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_working_dir, absolute_file_path = verify_python_file(
            working_directory, file_path
        )
        command: list[str] = ["python", absolute_file_path]
        if args:
            command.extend(args)

        subprocess_result = subprocess.run(
            command, text=True, timeout=30, capture_output=True
        )
        stdout = subprocess_result.stdout
        stderr = subprocess_result.stderr

        complete_process: list[str] = []

        if subprocess_result.returncode == 0:
            complete_process.append("Process exited with code 0")
        if not stdout and not stderr:
            complete_process.insert(0, "No output produced")
        else:
            complete_process.insert(0, f"STDOUT: {stdout}")
            complete_process.insert(1, f"STDERR: {stderr}")

        return "\n".join(complete_process)

    except Exception as e:
        return f"Error: executing Python file: {e}"


def verify_python_file(working_directory: str, file_path: str) -> tuple[str, str]:
    absolute_working_dir: str = os.path.abspath(os.path.normpath(working_directory))
    target_file: str = os.path.abspath(
        os.path.normpath(os.path.join(absolute_working_dir, file_path))
    )

    is_inside_working_dir: bool = (
        os.path.commonpath([absolute_working_dir, target_file]) == absolute_working_dir
    )

    if not is_inside_working_dir:
        raise ValueError(
            f'Cannot execute "{file_path}" as it is outside the permitted working directory'
        )

    if not os.path.isfile(target_file):
        raise ValueError(f'"{file_path}" does not exist or is not a regular file')

    if not target_file.endswith("py"):
        raise ValueError(f'"{file_path}" is not a Python file')

    return absolute_working_dir, target_file
