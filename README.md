# DataLeak

**DataLeak** is a web-based tool built with **Python and Django** for detecting and analyzing metadata in **PDF and image files**.  
The project focuses on identifying potentially sensitive information hidden in file metadata and helps to clear file from sensitive data.
<br>

## Project Description

DataLeak allows users to upload PDF documents and image files to automatically extract and analyze metadata.  
This helps identify unintentional data leaks such as:

- Author, Creator names
- Software used to create the file
- Creation and modification dates
- Device information
- Hidden technical metadata

The project is designed for **educational and security testing purposes**.

##  Features

- Metadata extraction from PDF files and image files
- Detection of potentially sensitive metadata
- Secure file upload handling
- Clear metadata report
- Possibility to download cleared file
- Option to browse or download meta data in JSON format

##  Tech Stack

- Python 3
- Django
- HTML / CSS (Bulma)
- Black formatter
- Flake for linting
- Pytest for unittests

##  Installation

Install using Docker
```bash
docker build -t data-leaks:1.0 <file_location>
docker run -p 8080:8080 data-leaks:1.0
```

Or install by uv:

1. Clone the repository:
```bash
git clone https://github.com/KacperStrugala1/DataLeak.git
```

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





