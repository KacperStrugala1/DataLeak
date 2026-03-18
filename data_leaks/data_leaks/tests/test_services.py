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

