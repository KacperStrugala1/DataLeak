from .services import PdfFile, PhotoFile
from PIL import Image

import logging

class FileType:
    def __init__(self):
        self.pdf_file = PdfFile()
        self.image_file = PhotoFile()
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ico"}  
        pdf_extension = ".pdf"

    def check_file_format(self, file):
        content_type = file.content_type

        if content_type == "application/pdf":
            self.pdf_file.get_metadata(file)
        elif content_type in ["image/jpeg", "image/png"]:
            self.image_file.get_metadata(file)
        else:
            logging.error("Unsupported file type")