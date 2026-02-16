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

    # REFACTOR THAT pls

    def get_file_extension(self, file):
        content_type = file.content_type

        if content_type in self.pdf_extension:
            return "pdf"
        elif content_type in self.image_extensions:
            return "image"
        else:
            return None

    def check_file_format(self, file):
        content_type = file.content_type

        if content_type in self.pdf_extension:
            return self.pdf_file.get_metadata(file)
        elif content_type in self.image_extensions:
            return self.image_file.get_metadata(file)
        else:
            return None

    def delete_file(self, file):
        content_type = file.content_type

        if content_type in self.pdf_extension:
            return self.pdf_file.delete_metadata(file)
        elif content_type in self.image_extensions:
            return self.image_file.delete_metadata(file)
        else:
            return None
