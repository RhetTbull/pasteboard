"""Test pasteboard.py module; run with pytest"""

import pathlib

import pytest

from pasteboard import Pasteboard

TEST_IMAGE = "test.png"


def test_copy_paste():
    """Test copy() and paste() methods"""
    pb = Pasteboard()
    pb.copy("Hello World")
    assert pb.paste() == "Hello World"


def test_append():
    """Test append() method"""
    pb = Pasteboard()
    pb.copy("Hello")
    pb.append(" World")
    assert pb.paste() == "Hello World"


def test_clear():
    """Test clear() method"""
    pb = Pasteboard()
    pb.copy("Hello World")
    assert pb.paste() == "Hello World"
    pb.clear()
    assert pb.paste() == ""


def test_copy_paste_image(tmp_path):
    """Test copy_image() and paste_image() methods"""
    pb = Pasteboard()
    pb.copy_image(TEST_IMAGE)
    temp_file = tmp_path / TEST_IMAGE
    pb.paste_image(str(temp_file), overwrite=False)
    assert temp_file.exists()
    assert open(TEST_IMAGE, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.paste_image(str(temp_file), overwrite=False)

    pb.paste_image(str(temp_file), overwrite=True)
    assert temp_file.exists()


def test_copy_paste_image_pathlib(tmp_path):
    """Test copy_image() and paste_image() methods with pathlib.Path"""
    pb = Pasteboard()
    pb.copy_image(pathlib.Path(TEST_IMAGE))
    temp_file = tmp_path / TEST_IMAGE
    pb.paste_image(pathlib.Path(temp_file), overwrite=False)
    assert temp_file.exists()
    assert open(TEST_IMAGE, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.paste_image(pathlib.Path(temp_file), overwrite=False)

    pb.paste_image(pathlib.Path(temp_file), overwrite=True)
    assert temp_file.exists()


def test_get_set_text():
    """Test get_text() and set_text() methods"""
    pb = Pasteboard()
    pb.set_text("Hello World")
    assert pb.get_text() == "Hello World"


def test_get_set_image(tmp_path):
    """Test get_image() and set_image() methods"""
    pb = Pasteboard()
    pb.set_image(TEST_IMAGE)
    temp_file = tmp_path / "temp.png"
    pb.get_image(temp_file, overwrite=False)
    assert open(TEST_IMAGE, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.get_image(temp_file, overwrite=False)

    pb.get_image(temp_file, overwrite=True)
    assert open(TEST_IMAGE, "rb").read() == open(temp_file, "rb").read()


def test_get_set_image_pathlib(tmp_path):
    """Test get_image() and set_image() methods with pathlib.Path"""
    pb = Pasteboard()
    pb.set_image(pathlib.Path(TEST_IMAGE))
    temp_file = tmp_path / "temp.png"
    pb.get_image(temp_file, overwrite=False)
    assert open(TEST_IMAGE, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.get_image(temp_file, overwrite=False)

    pb.get_image(temp_file, overwrite=True)
    assert open(TEST_IMAGE, "rb").read() == open(temp_file, "rb").read()


def test_has_text():
    """Test has_text() method"""
    pb = Pasteboard()
    pb.copy("Hello World")
    assert pb.has_text() is True
    pb.clear()
    assert pb.has_text() is False


def test_has_image():
    """Test has_image() method"""
    pb = Pasteboard()
    pb.copy("Hello World")
    assert pb.has_image() is False
    pb.copy_image(TEST_IMAGE)
    assert pb.has_image() is True
    pb.clear()
    assert pb.has_image() is False


def test_has_changed():
    """Test has_changed() method"""
    pb = Pasteboard()
    pb.copy("Hello World")
    assert pb.has_changed() is False
    pb2 = Pasteboard()
    pb2.copy("Hello World 2")
    assert pb.has_changed() is True
