from pypdf import PdfReader
from PIL import Image
from PIL.ExifTags import TAGS
import logging


class PdfFile:
    def get_metadata(self, file):
        try:
            reader = PdfReader(file)
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

    def get_metadata(self, file):
        image = Image.open(file)
        exif_data = image.getexif()
        meta_data = {}

        for tag_id, value in exif_data.items():
            tagname = TAGS.get(tag_id, tag_id)

            if isinstance(value, bytes):
                max_len = 50
                if len(value) > max_len:
                    value = value[:max_len].hex() + "..."
                else:
                    value = value.hex()

            meta_data[f"{tagname:25}"] = value

        return meta_data
    
# class JsonConverter:

#     def get_response(self, meta_data)