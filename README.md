# DataLeak

**DataLeak** is a web-based tool built with **Python and Django** for detecting and analyzing metadata in **PDF files and images**.  
The project focuses on identifying potentially sensitive information hidden in file metadata.

## Project Description

DataLeak allows users to upload PDF documents and image files to automatically extract and analyze metadata.  
This helps identify unintentional data leaks such as:

- Author names
- Software used to create the file
- GPS coordinates
- Creation and modification dates
- Device information
- Hidden technical metadata

The project is designed for **educational and security testing purposes**.

##  Features

- Metadata extraction from PDF files
- Metadata extraction from image files (EXIF)
- Detection of potentially sensitive metadata
- Web interface built with Django
- Secure file upload handling
- Clear metadata reporting

##  Tech Stack

- Python 3
- Django
- HTML / CSS (Bulma)

##  Installation

1. Clone the repository:
```bash
git clone https://github.com/KacperStrugala1/DataLeak.git
