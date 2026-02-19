import pytest
from unittest.mock import Mock
from data_leaks.file_type import FileType


@pytest.fixture
def file_type():
    file_type = FileType()
    file_type.pdf_file = Mock()
    file_type.image_file = Mock()
    return file_type

def test_get_handler_pdf(file_type):
    handler = file_type._get_handler("application/pdf")
    assert handler == file_type.pdf_file

def test_get_handler_image(file_type):
    handler = file_type._get_handler("image/png")
    assert handler == file_type.image_file
    
def test_get_handler_fail(file_type):
    handler = file_type._get_handler("")
    assert handler is None


@pytest.mark.parametrize("extension", [
    "application/pdf",
    "image/jpg",
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/bmp",
    "image/tiff",
    "image/ico"
    ])

def test_is_supported_returns_true(file_type, extension):
    assert file_type.is_supported(extension)  

@pytest.mark.parametrize("extension", [
    "",
    "   ",
    "imag",
    "pdf",
    "gif",
    "text/plain",
    ",value",
    None
    ])

def test_is_supported_fail(file_type, extension):
    assert not file_type.is_supported(extension)  
      
    