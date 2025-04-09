import os
import re


def get_next_filename(
    folder_path="./audio/data", base_filename="recording", extension="wav"
):
    """
    Finds the largest number in filenames matching "base_filename_XXX.extension",
    increments it by 1, and returns the new filename.

    Args:
        folder_path (str): The path to the folder.
        base_filename (str): The base filename (e.g., "file_name").
        extension (str): The extension (e.g., "wav")

    Returns:
        str: The incremented filename (e.g., "file_name_003.wav").
    """
    highest_number = -1
    pattern = re.compile(rf"{base_filename}_(\d+).{extension}")

    try:
        for filename in os.listdir(folder_path):
            match = pattern.match(filename)
            if match:
                number = int(match.group(1))
                highest_number = max(highest_number, number)

        new_number = highest_number + 1
        return f"{base_filename}_{new_number:03d}.{extension}"

    except FileNotFoundError:
        return f"{base_filename}_000.{extension}"

    except Exception as e:
        print(f"An Exception occured: {e}")
        return None
