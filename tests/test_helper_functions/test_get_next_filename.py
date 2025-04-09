import os
import pytest
from unittest.mock import patch
from helper_functions import get_next_filename


@pytest.fixture
def test_folder(tmp_path):
    """Fixture to create and clean up a temporary test folder."""
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()
    yield str(folder_path)
    # pytest handles the cleanup of tmp_path automatically


def test_different_arguments(test_folder):
    assert get_next_filename(test_folder, "game", "exe") == "game_000.exe"
    assert get_next_filename(test_folder, "image", "jpg") == "image_000.jpg"
    assert get_next_filename(test_folder, "movie", "mp4") == "movie_000.mp4"


def test_no_files(test_folder):
    assert get_next_filename(test_folder) == "recording_000.wav"


def test_single_file(test_folder):
    open(os.path.join(test_folder, "recording_000.wav"), "a").close()
    assert get_next_filename(test_folder) == "recording_001.wav"


def test_multiple_files(test_folder):
    open(os.path.join(test_folder, "recording_000.wav"), "a").close()
    open(os.path.join(test_folder, "recording_001.wav"), "a").close()
    open(os.path.join(test_folder, "recording_002.wav"), "a").close()
    assert get_next_filename(test_folder) == "recording_003.wav"


def test_gap_in_numbers(test_folder):
    open(os.path.join(test_folder, "recording_000.wav"), "a").close()
    open(os.path.join(test_folder, "recording_005.wav"), "a").close()
    assert get_next_filename(test_folder) == "recording_006.wav"


def test_different_base_filename(test_folder):
    open(os.path.join(test_folder, "image_002.jpg"), "a").close()
    assert get_next_filename(test_folder, "image", "jpg") == "image_003.jpg"


def test_non_matching_files(test_folder):
    open(os.path.join(test_folder, "another_file.txt"), "a").close()
    open(os.path.join(test_folder, "recording_000.wav"), "a").close()
    assert get_next_filename(test_folder) == "recording_001.wav"


def test_folder_not_found():
    assert get_next_filename("./non_existent_folder") == "recording_000.wav"


def test_exception_handling(test_folder, capsys):
    with patch("os.listdir", side_effect=Exception("Test Exception")):
        result = get_next_filename(test_folder)
        captured = capsys.readouterr()
        assert "An Exception occured: Test Exception" in captured.out
        assert result is None
