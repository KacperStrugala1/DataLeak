from data_leaks.utils.services import PdfFile, PhotoFile
from unittest.mock import MagicMock, patch
import pytest
import datetime
import PIL

#PDF FILE tests
@pytest.fixture
def pdf_file():
    pdf_file = PdfFile()
    return pdf_file

def test_get_metadata(pdf_file):
    mock_meta = MagicMock()
    mock_meta.title = "Title"
    mock_meta.author = "Author"
    mock_meta.creator = "Creator"
    mock_meta.producer = "Producer"
    mock_meta.subject = "Subject"
    mock_meta.creation_date = datetime.datetime(2024, 1, 1, 10, 0, 0)
    mock_meta.keywords = "pdf,test"

    mock_reader = MagicMock()
    mock_reader.metadata = mock_meta

    with patch("pdf_file.PdfReader", return_value=mock_reader):
        result = pdf_file.get_metadata("fake.pdf")

    assert result["Title"] == "Title"
    assert result["Created"] == "2024-01-01 10:00:00"


