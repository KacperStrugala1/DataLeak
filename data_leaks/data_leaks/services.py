from pypdf import PdfReader
from PIL import Image
from PIL.ExifTags import TAGS
import logging


class PdfFile:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def get_metadata(self):
        try:
            reader = PdfReader(f"{self.pdf_file}")
            meta = reader.metadata
            
            if not meta:
                return "Cannot fetch metadata or blank file"
            else:
                return {
                    #gettatr get attribute 'author' form instance meta if not avail return None
                    "Author": getattr(meta, 'author', None),
                    "Creator": getattr(meta, 'creator', None),
                    "Producer": getattr(meta, 'producer', None),
                    "Subject": getattr(meta, 'subject', None),
                    "Title": getattr(meta, 'title', None)
                }
        except Exception as exc:
            logging.info(f"Error occured: {exc}")
            return f"Error occured: {exc}"

class PhotoFile:
    def __init__(self, photo_file):
        self.photo_file = photo_file

    def get_metadata(self):
        image = Image(f"{self.photo_file}")
        exif_data = image.getexif()

        for tag_id in exif_data:
            meta_data = {}
            tagname = TAGS.get(tag_id, tag_id)
            value = exif_data.get(tag_id)
            meta_data[f"{tagname:25}"] = value
            return meta_data
