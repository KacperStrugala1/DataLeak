from pypdf import PdfReader
from PIL import Image
from PIL.TiffImagePlugin import IFDRational
from PIL.ExifTags import TAGS
import logging
import datetime


class PdfFile:
    def get_metadata(self, file):
        try:
            reader = PdfReader(file)
            meta = reader.metadata
            
            if not meta:
                return "Cannot fetch metadata or blank file"
            else:
                meta_data = {
                    "Title": getattr(meta, 'title', None),
                    "Author": getattr(meta, 'author', None),
                    "Creator": getattr(meta, 'creator', None),
                    "Producer": getattr(meta, 'producer', None),
                    "Subject": getattr(meta, 'subject', None),
                    #added time serialization to get pass to json
                    "Created": getattr(meta, 'creation_date', None).strftime("%Y-%m-%d %H:%M:%S"),
                    "Keywords": getattr(meta, 'keywords', None)
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
        return meta_data
    
