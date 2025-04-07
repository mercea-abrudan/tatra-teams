import os
from audio.functions import record
from helper_functions import get_next_filename

audio_folder = "./audio/data"
file_name = get_next_filename(audio_folder)
file_path = os.path.join(audio_folder, file_name)


def main():
    record(duration=10, sample_rate=44100, output_file_name=file_path)


if __name__ == "__main__":
    main()
