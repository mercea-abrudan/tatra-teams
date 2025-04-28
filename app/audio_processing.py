import logging
import os
import threading
import scipy.io.wavfile as wav
import sounddevice as sd

logger = logging.getLogger(__name__)

SAMPLE_RATE = 44100  # kiloHertz
DURATION = 10  # seconds
MIC_DEVICE_INDEX = 1
OUT_DEVICE_INDEX = 2


def record(output_file_name: str | os.PathLike, device_index: int, duration: int = DURATION, sample_rate: int = SAMPLE_RATE):
    """
    Records audio from a specified device and saves it to a WAV file.

    This function uses the `sounddevice` library to record audio from the
    audio input device identified by `device_index`. The recording runs
    for a specified `duration` at a given `sample_rate` and saves the
    captured audio data as a single-channel WAV file using `scipy.io.wavfile`.

    Parameters:
        output_file_name (str | os.PathLike): The file path where the recorded
            audio will be saved in WAV format.
        device_index (int): The index of the audio input device to record from.
            You can find available device indices using `sd.query_devices()`.
        duration (int, optional): The duration of the recording in seconds.
            Defaults to the global `DURATION` constant.
        sample_rate (int, optional): The sampling rate (frames per second) for
            the audio recording. Defaults to the global `SAMPLE_RATE` constant.

    Returns:
        None

    Notes:
        - Ensure that the `device_index` is valid for your system.
        - The recording is saved as a single-channel (mono), 16-bit PCM WAV file.
        - This function blocks until the recording is complete.

    Example:
        >>> record("microphone_recording.wav", 1, duration=10, sample_rate=48000)
    """
    logger.info(f"Recording from device: {device_index} started.")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, device=device_index)
    sd.wait()
    logger.info(f"Recording from device: {device_index} finished.")
    wav.write(output_file_name, sample_rate, recording)


def record_mic_and_out(
        mic_filename: str | os.PathLike,
        out_filename: str | os.PathLike,
        mic_device_index: int = MIC_DEVICE_INDEX,
        out_device_index: int = OUT_DEVICE_INDEX,
    ):
    """
    Record audio from the microphone and system output simultaneously using threads.

    This function starts recording audio from two different audio devices:
    one designated as the microphone input and the other as the system audio output.
    The recordings are executed in parallel using threads and saved to separate files.

    Parameters:
        mic_filename (str | os.PathLike): The file path where the microphone audio 
            will be saved in WAV format.
        out_filename (str | os.PathLike): The file path where the system audio 
            output will be saved in WAV format.
        mic_device_index (int, optional): The index of the microphone input device. 
            Defaults to MIC_DEVICE_INDEX.
        out_device_index (int, optional): The index of the system output audio device. 
            Defaults to OUT_DEVICE_INDEX.

    Returns:
        None

    Notes:
        - Ensure the device indices provided are valid and correspond to the 
          desired audio devices on your system.
        - Device indeces can be found by listing sd.query_devices()
        - This function blocks execution until both recordings are complete.
        - The audio files are saved in 16-bit PCM format with a single channel 
          (mono) audio stream by default.

    Example:
        >>> record_mic_and_out(
        ...     mic_filename="mic_audio.wav",
        ...     out_filename="sys_audio.wav",
        ...     mic_device_index=1,
        ...     out_device_index=2,
        ... )
    """
    logger.info("Recording started.")

    # Use threads to record from both devices simultaneously
    mic_thread = threading.Thread(target=record, args=(mic_filename, mic_device_index))
    out_thread = threading.Thread(target=record, args=(out_filename, out_device_index))

    # Start recording
    mic_thread.start()
    out_thread.start()

    # Wait for both recordings to complete
    mic_thread.join()
    out_thread.join()
    logger.info("Recording complete.")
