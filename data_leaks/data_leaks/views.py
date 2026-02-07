from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . import forms
from .services import PdfFile, PhotoFile
import logging
from . import file_type

def index(request):
    try:
        if request.method == "POST":
            form = forms.UploadFileForm(request.POST, request.FILES)
            logging.debug(request.FILES)
            logging.debug(request.POST)
            if form.is_valid():
                
                file = form.cleaned_data['file']
                file_format = file_type.FileType()
                meta_data = file_format.check_file_format(file)
    
                return HttpResponse(f"{meta_data}")
        else:
            logging.debug("not valid")
            form = forms.UploadFileForm()
        return render(request, "home.html", {"form":form})
    except Exception as exc:
        logging.error(f"Error {exc}")