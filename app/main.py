import logging
import os
from audio_processing import record_mic_and_out
from utils import get_next_filename

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

audio_folder = "../data/recordings"
mic_file_name = get_next_filename(audio_folder, "mic")
out_file_name = get_next_filename(audio_folder, "out")
mic_file_path = os.path.join(audio_folder, mic_file_name)
out_file_path = os.path.join(audio_folder, out_file_name)


def main():
    logger.info("Application started.")
    record_mic_and_out(mic_file_path, out_file_path, 1, 2)
    logger.info("Application finished.")


if __name__ == "__main__":
    main()
