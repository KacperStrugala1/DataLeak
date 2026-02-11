from .utils.services import PdfFile, PhotoFile

class FileType:
    def __init__(self):
        self.pdf_file = PdfFile()
        self.image_file = PhotoFile()
        #image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ico"]  
        #pdf_extension = ".pdf"

    def check_file_format(self, file):
        content_type = file.content_type

        if content_type == "application/pdf":
            return self.pdf_file.get_metadata(file)
        elif content_type in ["image/jpeg", "image/png"]:
            return self.image_file.get_metadata(file)
        else:
            return "Unsupported file type"