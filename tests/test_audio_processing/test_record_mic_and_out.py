import pytest
import threading
from unittest.mock import call, Mock, patch

from app.audio_processing import record, record_mic_and_out
from app.audio_processing import MIC_DEVICE_INDEX, OUT_DEVICE_INDEX


@pytest.fixture
def mock_sounddevice():
    """Mocks the sounddevice module to prevent actual recording."""
    with patch("sounddevice.rec") as mock_rec, patch("sounddevice.wait") as mock_wait:
        yield mock_rec, mock_wait


@pytest.fixture
def mock_wavfile():
    """Mocks the scipy.io.wavfile module."""
    with patch("scipy.io.wavfile.write") as mock_wav_write:
        yield mock_wav_write


def test_record_mic_and_out_calls_record_function(
    tmp_path, mock_sounddevice, mock_wavfile
):
    """
    Tests that the 'record' function is called for both microphone and output.
    """
    mic_filename = str(tmp_path / "mic_audio.wav")
    out_filename = str(tmp_path / "system_audio.wav")

    with patch("app.audio_processing.record") as mock_record:
        record_mic_and_out(mic_filename, out_filename, 1, 2)
        mock_record.assert_any_call(mic_filename, 1)
        mock_record.assert_any_call(out_filename, 2)
        assert mock_record.call_count == 2


def test_record_mic_and_out_uses_default_device_indices(
    tmp_path, mock_sounddevice, mock_wavfile
):
    """
    Tests that default device indices are used if not provided.
    """
    mic_filename = str(tmp_path / "mic_audio.wav")
    out_filename = str(tmp_path / "system_audio.wav")

    with patch("app.audio_processing.record") as mock_record:
        record_mic_and_out(mic_filename, out_filename)
        mock_record.assert_any_call(mic_filename, MIC_DEVICE_INDEX)
        mock_record.assert_any_call(out_filename, OUT_DEVICE_INDEX)
        assert mock_record.call_count == 2


def test_record_mic_and_out_creates_threads(tmp_path, mock_sounddevice, mock_wavfile):
    """
    Tests that two threads are created and started.
    """
    mic_filename = str(tmp_path / "mic_audio.wav")
    out_filename = str(tmp_path / "system_audio.wav")

    with patch("threading.Thread") as MockThread:
        record_mic_and_out(mic_filename, out_filename)
        assert MockThread.call_count == 2
        calls = [
            call(target=record, args=(mic_filename, MIC_DEVICE_INDEX)),
            call(target=record, args=(out_filename, OUT_DEVICE_INDEX)),
        ]
        MockThread.assert_has_calls(calls, any_order=True)
        mock_threads = [
            call_obj.return_value
            for call_obj in MockThread.mock_calls
            if call_obj.method == "()"
        ]
        for mock_thread in mock_threads:
            assert mock_thread.start.called


def test_record_mic_and_out_waits_for_threads(tmp_path, mock_sounddevice, mock_wavfile):
    """
    Tests that the main thread waits for both recording threads to complete.
    """
    mic_filename = str(tmp_path / "mic_audio.wav")
    out_filename = str(tmp_path / "system_audio.wav")

    mock_mic_thread = Mock(spec=threading.Thread)
    mock_out_thread = Mock(spec=threading.Thread)

    with patch("threading.Thread", side_effect=[mock_mic_thread, mock_out_thread]):
        record_mic_and_out(mic_filename, out_filename)
        mock_mic_thread.start.assert_called_once()
        mock_out_thread.start.assert_called_once()
        mock_mic_thread.join.assert_called_once()
        mock_out_thread.join.assert_called_once()


def test_record_mic_and_out_with_os_pathlike(tmp_path, mock_sounddevice, mock_wavfile):
    """
    Tests that the function works correctly with os.PathLike objects.
    """
    mic_filename = tmp_path / "mic_audio.wav"
    out_filename = tmp_path / "system_audio.wav"

    with patch("app.audio_processing.record"):
        record_mic_and_out(mic_filename, out_filename)
        # We don't need to assert much here, as the 'record' function is mocked
        # The fact that the function runs without error is a basic check.
        pass
