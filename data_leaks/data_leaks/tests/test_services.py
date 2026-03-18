from data_leaks.utils.services import PdfFile, PhotoFile
from unittest.mock import MagicMock, patch
from pypdf import PdfReader, PdfWriter
import pytest
from datetime import datetime
import PIL


@pytest.fixture
def pdf_file():
    return PdfFile()


@pytest.fixture
def photo_file():
    return PhotoFile()


@pytest.fixture
def metadata_pdf():
    meta_data = MagicMock()
    meta_data.title = "Test Title"
    meta_data.creation_date = datetime(2024, 1, 1, 12, 0, 0)
    meta_data.keywords = "pdf,test"
    return meta_data


@pytest.fixture
def metadata_pdf():
    meta_data = MagicMock()
    meta_data.title = "Test Title"
    meta_data.creation_date = datetime(2026, 1, 1, 12, 0, 0)
    meta_data.keywords = "pdf,test"
    return meta_data


@patch("data_leaks.utils.services.PdfReader")
def test_get_metadata_create_date(mock_reader, pdf_file, metadata_pdf):

    mock_reader.return_value.metadata = metadata_pdf
    result = pdf_file.get_metadata("file.pdf")

    assert result["Created"] == "2026-01-01 12:00:00"


@patch("data_leaks.utils.services.PdfReader")
def test_get_metadata_fail(mock_reader, pdf_file):

    mock_reader.return_value.metadata = None
    result = pdf_file.get_metadata("file.pdf")

    assert result == "Cannot fetch metadata or blank file"


@patch("data_leaks.utils.services.PdfReader")
def test_get_metadata_without_date(mock_reader, pdf_file):
    meta_data = MagicMock()
    meta_data.creation_date = None
    mock_reader.return_value.metadata = meta_data
    result = pdf_file.get_metadata("file.pdf")

    assert result["Created"] == "None"
