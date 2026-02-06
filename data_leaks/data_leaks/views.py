from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . import forms, services
from loguru import logger

def index(request):
    try:
        if request.method == "POST":
            form = forms.UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                cleaned_file = services.get_metadata(file)
                return HttpResponse(f"{cleaned_file}")
        else:
            form = forms.UploadFileForm()
        return render(request, "home.html", {"form":form})
    except Exception as exc:
        logger.error(f"Error {exc}")