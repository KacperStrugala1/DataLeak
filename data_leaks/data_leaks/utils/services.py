from pypdf import PdfReader, PdfWriter
from PIL import Image
from io import BytesIO
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
                if getattr(meta, 'creation_date') != None:
                    meta_data = {
                        "Title": getattr(meta, 'title', None),
                        "Author": getattr(meta, 'author', None),
                        "Creator": getattr(meta, 'creator', None),
                        "Producer": getattr(meta, 'producer', None),
                        "Subject": getattr(meta, 'subject', None),
                        #added time serialization to get pass to json
                        "Created": getattr(meta, 'creation_date').strftime("%Y-%m-%d %H:%M:%S"),
                        "Keywords": getattr(meta, 'keywords', None)
                    }
                else:
                    meta_data = {
                        "Title": getattr(meta, 'title', None),
                        "Author": getattr(meta, 'author', None),
                        "Creator": getattr(meta, 'creator', None),
                        "Producer": getattr(meta, 'producer', None),
                        "Subject": getattr(meta, 'subject', None),
                        #added time serialization to get pass to json
                        "Created": "None",
                        "Keywords": getattr(meta, 'keywords', None)
                    }
                return meta_data
            
        except Exception as exc:
            logging.info(f"Error occured: {exc}")
            return f"Error occured: {exc}"
        
    def delete_metadata(self, file):
        reader = PdfReader(file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        buffer = BytesIO()
        writer.write(buffer)
        buffer.seek(0)

        return buffer
            

class PhotoFile:

    def get_metadata(self, file):
        image = Image.open(file)
        exif_data = image.getexif()
        meta_data = {}

        for tag_id in exif_data:
            
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)

            #continue to not decode or print byte data 
            if isinstance(data, bytes):
                continue
                
            meta_data[f"{tag}"] = data
        return meta_data
    
    def delete_metadata(self, file):
        pass