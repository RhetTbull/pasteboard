"""Test pasteboard.py module; run with pytest"""

import pathlib

import pytest

from pasteboard import Pasteboard, PNG, TIFF, PasteboardTypeError

TEST_IMAGE_PNG = "test.png"
TEST_IMAGE_TIFF = "test.tiff"


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
    pb.copy_image(TEST_IMAGE_PNG, PNG)
    temp_file = tmp_path / TEST_IMAGE_PNG
    pb.paste_image(str(temp_file), PNG, overwrite=False)
    assert temp_file.exists()
    assert open(TEST_IMAGE_PNG, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.paste_image(str(temp_file), PNG, overwrite=False)

    pb.paste_image(str(temp_file), PNG, overwrite=True)
    assert temp_file.exists()


def test_copy_paste_image_pathlib(tmp_path):
    """Test copy_image() and paste_image() methods with pathlib.Path"""
    pb = Pasteboard()
    pb.copy_image(pathlib.Path(TEST_IMAGE_PNG), PNG)
    temp_file = tmp_path / TEST_IMAGE_PNG
    pb.paste_image(pathlib.Path(temp_file), PNG, overwrite=False)
    assert temp_file.exists()
    assert open(TEST_IMAGE_PNG, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.paste_image(pathlib.Path(temp_file), PNG, overwrite=False)

    pb.paste_image(pathlib.Path(temp_file), PNG, overwrite=True)
    assert temp_file.exists()


def test_get_set_text():
    """Test get_text() and set_text() methods"""
    pb = Pasteboard()
    pb.set_text("Hello World")
    assert pb.get_text() == "Hello World"


def test_get_set_image(tmp_path):
    """Test get_image() and set_image() methods"""
    pb = Pasteboard()
    pb.set_image(TEST_IMAGE_PNG, PNG)
    temp_file = tmp_path / "temp.png"
    pb.get_image(temp_file, PNG, overwrite=False)
    assert open(TEST_IMAGE_PNG, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.get_image(temp_file, PNG, overwrite=False)

    pb.get_image(temp_file, PNG, overwrite=True)
    assert open(TEST_IMAGE_PNG, "rb").read() == open(temp_file, "rb").read()


def test_get_set_image_pathlib(tmp_path):
    """Test get_image() and set_image() methods with pathlib.Path"""
    pb = Pasteboard()
    pb.set_image(pathlib.Path(TEST_IMAGE_PNG), PNG)
    temp_file = tmp_path / "temp.png"
    pb.get_image(temp_file, PNG, overwrite=False)
    assert open(TEST_IMAGE_PNG, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.get_image(temp_file, PNG, overwrite=False)

    pb.get_image(temp_file, PNG, overwrite=True)
    assert open(TEST_IMAGE_PNG, "rb").read() == open(temp_file, "rb").read()


def test_get_set_image_tiff(tmp_path):
    """Test get_image() and set_image() methods for TIFF"""
    pb = Pasteboard()
    pb.set_image(TEST_IMAGE_TIFF, TIFF)
    temp_file = tmp_path / "temp.tiff"
    pb.get_image(temp_file, TIFF, overwrite=False)
    assert open(TEST_IMAGE_TIFF, "rb").read() == open(temp_file, "rb").read()

    with pytest.raises(FileExistsError):
        pb.get_image(temp_file, TIFF, overwrite=False)

    pb.get_image(temp_file, TIFF, overwrite=True)
    assert open(TEST_IMAGE_TIFF, "rb").read() == open(temp_file, "rb").read()

    # TIFF image doesn't have PNG representation
    with pytest.raises(PasteboardTypeError):
        pb.get_image(temp_file, PNG, overwrite=True)


def test_set_text_and_image(tmp_path):
    """Test set_text_and_image() method"""
    pb = Pasteboard()
    pb.set_text_and_image("A photo of a palm tree", TEST_IMAGE_PNG, PNG)
    assert pb.has_text()
    assert pb.has_image()
    assert pb.get_text() == "A photo of a palm tree"
    temp_file = tmp_path / "temp.png"
    pb.get_image(temp_file, PNG, overwrite=False)
    assert open(TEST_IMAGE_PNG, "rb").read() == open(temp_file, "rb").read()


def test_set_text_and_image_pathlib(tmp_path):
    """Test set_text_and_image() method with pathlib.Path input"""
    pb = Pasteboard()
    pb.set_text_and_image("A photo of a palm tree", pathlib.Path(TEST_IMAGE_PNG), PNG)
    assert pb.has_text()
    assert pb.has_image()
    assert pb.get_text() == "A photo of a palm tree"
    temp_file = tmp_path / "temp.png"
    pb.get_image(temp_file, PNG, overwrite=False)
    assert open(TEST_IMAGE_PNG, "rb").read() == open(temp_file, "rb").read()


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
    pb.copy_image(TEST_IMAGE_PNG, PNG)
    assert pb.has_image() is True
    assert pb.has_image(PNG) is True
    assert pb.has_image(TIFF) is True
    pb.copy_image(TEST_IMAGE_TIFF, TIFF)
    assert pb.has_image() is True
    assert pb.has_image(PNG) is False
    assert pb.has_image(TIFF) is True
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


def test_invalid_format(tmp_path):
    """Test invalid format specifier raises PasteboardTypeError"""
    pb = Pasteboard()
    with pytest.raises(PasteboardTypeError):
        pb.copy_image(TEST_IMAGE_PNG, "invalid")

    pb.copy_image(TEST_IMAGE_PNG, PNG)
    temp_file = tmp_path / "temp.png"
    with pytest.raises(PasteboardTypeError):
        pb.get_image(temp_file, "invalid")

    with pytest.raises(PasteboardTypeError):
        pb.get_image_data("invalid")

    with pytest.raises(PasteboardTypeError):
        pb.has_image("invalid")
