from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . import forms, services
import logging

def index(request):
    try:
        if request.method == "POST":
            form = forms.UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                logging.debug("Valid")
                file = form.cleaned_data['file']
                cleaned_file = services.get_metadata(file)
                logging.debug("Cleanded")

                return HttpResponse(f"{cleaned_file}")
        else:
            logging.debug("not valid")
            form = forms.UploadFileForm()
        return render(request, "home.html", {"form":form})
    except Exception as exc:
        logging.error(f"Error {exc}")