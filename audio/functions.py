import os
import scipy.io.wavfile as wav
import sounddevice as sd

sample_rate = 44100  # kiloHertz
duration = 60  # seconds


def record(duration: int, sample_rate: int, output_file_name: str | os.PathLike):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    print("Recording finished.")
    wav.write(output_file_name, sample_rate, recording)
