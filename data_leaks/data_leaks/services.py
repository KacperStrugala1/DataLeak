from pypdf import PdfReader
import logging

def get_metadata(file):
    try:
        reader = PdfReader(file)
        meta = reader.metadata
        
        if not meta:
            return "Cannot fetch metadata or blank file"
        else:
            return {
                "Author": getattr(meta, 'author', None),
                "Creator": getattr(meta, 'creator', None),
                "Producer": getattr(meta, 'producer', None),
                "Subject": getattr(meta, 'subject', None),
                "Title": getattr(meta, 'title', None)
            }
    except Exception as exc:
        logging.info(f"Error occured: {exc}")
        return f"Error occured: {exc}"
