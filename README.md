# DataLeak

**DataLeak** is a web-based tool built with **Python and Django** for detecting and analyzing metadata in **PDF and image files**.  
The project focuses on identifying potentially sensitive information hidden in file metadata.
<br>

Project Preview:
<img width="1865" height="1053" alt="image" src="https://github.com/user-attachments/assets/08d0d9d4-e362-4494-8731-51d722b17102" />
<br>
<img width="1899" height="841" alt="image" src="https://github.com/user-attachments/assets/47694e51-8899-421c-b850-f61e9c454db1" />
<br>
<img width="434" height="347" alt="image" src="https://github.com/user-attachments/assets/810c86a7-e7db-43b3-acf5-3f184dd2b57f" />


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
```
2. Make virtual env
```bash
python -m venv venv 
```
3. Install uv 
```bash
 pip install uv
 ```
4. Sync uv to download all required libraries
```bash
 uv sync
 ```
5. Run server locally
```bash
python programit/manage.py runserver
```


