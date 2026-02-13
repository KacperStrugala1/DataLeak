from pypdf import PdfReader
from PIL import Image
from PIL.TiffImagePlugin import IFDRational
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
                meta_data = {
                    #gettatr get attribute 'author' form instance meta if not avail return None
                    "Author": getattr(meta, 'author', None),
                    "Creator": getattr(meta, 'creator', None),
                    "Producer": getattr(meta, 'producer', None),
                    "Subject": getattr(meta, 'subject', None),
                    "Title": getattr(meta, 'title', None)
                }
                logging.info(meta_data)
                return meta_data
            
        except Exception as exc:
            logging.info(f"Error occured: {exc}")
            return f"Error occured: {exc}"

class PhotoFile:

    def get_metadata(self, file):
        image = Image.open(file)
        exif_data = image.getexif()
        meta_data = {}

        for tag_id in exif_data:
            
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)

            if isinstance(data, bytes):
                data = data.decode()

        meta_data[f"{tag}"] = data
        logging.info(meta_data)
        return meta_data
    
# class JsonConverter:

#     def get_response(self, meta_data)