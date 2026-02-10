from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from . import forms
from .services import PdfFile, PhotoFile
import logging
from .file_type import FileType

class IndexView(ListView):
    def get(self, request):
        try:
            if request.method == "POST":
                form = forms.UploadFileForm(request.POST, request.FILES)
                logging.debug(request.FILES)
                logging.debug(request.POST)
                if form.is_valid():
                    
                    file = form.cleaned_data['file']
                    file_type = FileType()
                    meta_data = file_type.check_file_format(file)

                    return render(request, "meta_view.html", {"meta_data":meta_data})
            else:
                logging.debug("not valid")
                form = forms.UploadFileForm()
            return render(request, "home.html", {"form":form})
        
        except Exception as exc:
            logging.error(f"Error {exc}")
            return HttpResponse(f"Internal error: {exc}", status=500)
    def post(self, request):
        pass

def meta_view(request):
    if request.method == "POST":

        return JsonResponse()
    return render(request, "meta_view.html")