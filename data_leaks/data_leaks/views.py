from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from . import forms
from .file_type import FileType

import logging

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
                #sending meta_data in session
                request.session['meta_data'] = meta_data

                return render(request, "meta_view.html", {"meta_data":meta_data})
        else:
            logging.debug("not valid")
            form = forms.UploadFileForm()
        return render(request, "home.html", {"form":form})
    
    except Exception as exc:
        logging.error(f"Error {exc}")
        return HttpResponse(f"Internal error: {exc}", status=500)

def meta_view(request):
    try:
        if request.method == "POST":
            #JSON view for metadata
            meta_data = request.session.get("meta_data")
            if not meta_data:
                return HttpResponse("Invalid or no metadata")
            return JsonResponse(meta_data)
    except Exception as exc:
        return HttpResponse(f"Error: {exc}")
    
    del request.session["meta_data"]
        
    return render(request, "meta_view.html")

def delete_meta_data(request):
    try:
        if request.method == "POST":
            pass
    except Exception as exc:
        return HttpResponse(f"Error: {exc}")
    
def valentine(request):
    return render(request, "valentine.html")