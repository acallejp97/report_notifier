import os

import pytest
from services.save_file_service import SaveService


def test_save_and_read(temp_working_dir):
    filename = "testfile.txt"
    service = SaveService(filename)
    lines = ["line1\n", "line2\n"]
    service.save(lines)
    content = service.read()
    assert content == "line1\nline2\n"


def test_delete(temp_working_dir):
    filename = "testfile.txt"
    service = SaveService(filename)
    service.save(["line\n"])
    service.delete()
    assert not os.path.exists(service.filename)


def test_update_filename(temp_working_dir):
    service = SaveService()
    new_filename = "newfile.txt"
    service.update_filename(new_filename)
    assert new_filename in service.filename


def test_check_filename_error():
    service = SaveService()
    service.filename = "mock_file"
    with pytest.raises(ValueError):
        service._check_filename()


def test_read_nonexistent_file(temp_working_dir):
    """Test reading a file that doesn't exist returns None"""
    filename = "nonexistent.txt"
    service = SaveService(filename)
    content = service.read()
    assert content is None
