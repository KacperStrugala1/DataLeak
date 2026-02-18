from .utils.services import PdfFile, PhotoFile


class FileType:
    def __init__(self):
        self.pdf_file = PdfFile()
        self.image_file = PhotoFile()
        self.image_extensions = [
            "image/jpg",
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/bmp",
            "image/tiff",
            "image/ico",
        ]
        self.pdf_extension = ["application/pdf"]

    #handler will return instance of our file object (pdf or image) 
    def _get_handler(self, content_type):
        if content_type in self.pdf_extension:
            return self.pdf_file
        elif content_type in self.image_extensions:
            return self.image_file
        else:
            return None


    def is_supported(self, extension):
        if extension in self.pdf_extension or self.image_extensions:
            return True
        else:
            return False


    def check_file_meta(self, file):
        handler = self._get_handler(file.content_type)
        if handler:
            return handler.get_metadata(file)
        return None


    def delete_file_meta(self, file):
        handler = self._get_handler(file.content_type)
        if handler:
            return handler.delete_metadata(file)
        return None
