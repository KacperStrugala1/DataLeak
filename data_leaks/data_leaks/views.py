from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from . import forms
from .services import PdfFile, PhotoFile
import logging
from .file_type import FileType

def index(request):
    try:
        if request.method == "POST":
            form = forms.UploadFileForm(request.POST, request.FILES)
            logging.debug(request.FILES)
            logging.debug(request.POST)
            if form.is_valid():
                
                file = form.cleaned_data['file']
                file_type = FileType()
                meta_data = file_type.check_file_format(file)
                logging.debug(meta_data)
    
                return redirect("meta")
        else:
            logging.debug("not valid")
            form = forms.UploadFileForm()
        return render(request, "home.html", {"form":form})
    
    except Exception as exc:
        logging.error(f"Error {exc}")
        return HttpResponse(f"Internal error: {exc}", status=500)

def meta(request):
    return render(request, "meta.html")