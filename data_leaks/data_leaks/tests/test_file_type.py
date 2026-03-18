import pytest
from unittest.mock import Mock
from types import SimpleNamespace
from data_leaks.file_type import FileType


@pytest.fixture
def file_type():
    file_type = FileType()
    file_type.pdf_file = Mock()
    file_type.image_file = Mock()
    return file_type

pdf_extension = SimpleNamespace(content_type="application/pdf")
image_extension = SimpleNamespace(content_type= "image/jpeg")
invalid_extension = SimpleNamespace(content_type="video/mp4")

def test_get_handler_pdf(file_type):
    handler = file_type._get_handler("application/pdf")
    assert handler == file_type.pdf_file


def test_get_handler_image(file_type):
    handler = file_type._get_handler("image/png")
    assert handler == file_type.image_file


def test_get_handler_fail(file_type):
    handler = file_type._get_handler("")
    assert handler is None


@pytest.mark.parametrize(
    "extension",
    [
        "application/pdf",
        "image/jpg",
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/bmp",
        "image/tiff",
        "image/ico",
    ],
)
def test_is_supported_returns_true(file_type, extension):
    assert file_type.is_supported(extension)


@pytest.mark.parametrize(
    "extension", ["", "   ", "imag", "pdf", "gif", "text/plain", ",value", None]
)
def test_is_supported_fail(file_type, extension):
    assert not file_type.is_supported(extension)  



def test_check_file_meta_pdf(file_type):
    
    file_type.pdf_file.get_metadata.return_value = {"Creator": "User1"}

    
    metadata = file_type.check_file_meta(pdf_extension)
    file_type.pdf_file.get_metadata.assert_called_once_with(pdf_extension)

    assert metadata == {"Creator": "User1"}

def test_check_file_meta_photo(file_type):
    
    file_type.image_file.get_metadata.return_value = {"Device": "Iphone 17"}

    metadata = file_type.check_file_meta(image_extension)
    file_type.image_file.get_metadata.assert_called_once_with(image_extension)

    assert metadata == {"Device": "Iphone 17"}


def test_check_file_meta_fail(file_type):
    
    metadata = file_type.check_file_meta(invalid_extension)

    assert metadata is None

def test_delete_file_meta_pdf(file_type):
    pass

def test_delete_file_meta_pdf(file_type):
    pass

def test_delete_file_meta_pdf(file_type):
    pass
