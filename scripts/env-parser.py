#!/usr/bin/env python3

from pathlib import Path

from dotenv import dotenv_values


def parse_env_file(env_file_path: str | None = None) -> None:
    # If no path provided, use default '../.env' relative to script location
    if env_file_path is None:
        script_dir = Path(__file__).parent
        env_file_path = script_dir.parent / ".env"

    # Read the .env file
    env_config = dotenv_values(env_file_path)

    # Filter out specific keys and create formatted string
    excluded_keys = ["GOOGLE_APPLICATION_CREDENTIALS"]
    formatted_vars = ",".join(f"{key}={value}" for key, value in env_config.items() if key not in excluded_keys)

    # Print the formatted string (for shell to capture)
    print(formatted_vars)


if __name__ == "__main__":
    parse_env_file()
