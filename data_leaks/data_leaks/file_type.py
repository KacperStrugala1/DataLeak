from .utils.services import PdfFile, PhotoFile

class FileType:
    def __init__(self):
        self.pdf_file = PdfFile()
        self.image_file = PhotoFile()
        self.image_extensions = ["image/jpg", "image/jpeg", "image/png", "image/gif", "image/bmp", "image/tiff", "image/ico"]  
        #pdf_extension = ".pdf"

    def check_file_format(self, file):
        content_type = file.content_type

        if content_type == "application/pdf":
            return self.pdf_file.get_metadata(file)
        elif content_type in self.image_extensions:
            return self.image_file.get_metadata(file)
        else:
            return "Unsupported file type"
    
    def delete_file(self, file):
        content_type = file.content_type

        if content_type == "application/pdf":
            return self.pdf_file.delete_metadata(file)
        elif content_type in self.image_extensions:
            return self.image_file.delete_metadata(file)
        else:
            return "Unsupported file type"