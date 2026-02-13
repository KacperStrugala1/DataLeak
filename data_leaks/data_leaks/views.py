from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from . import forms
from .file_type import FileType

import logging

class HomeView(View):
    form_class = forms.UploadFileForm
    template_name = "home.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
            try:

                form = self.form_class(request.POST, request.FILES)
                if form.is_valid():
                    file = form.cleaned_data['file']
                    file_type = FileType()
                    meta_data = file_type.check_file_format(file)

                    #sending meta_data in session
                    request.session['meta_data'] = meta_data
                    return redirect("meta_view")
                else:
                    form = forms.UploadFileForm()
                    return render(request, "home.html", {"form":form})
                
            except Exception as exc:
                logging.error(f"Error {exc}")
                return HttpResponse(f"Internal error: {exc}", status=500)
        
class MetaView(View):
    template_name = "meta_view.html"

    def get(self, request):
        meta_data = request.session.get("meta_data")
            # del request.session["meta_data"]
        if not meta_data:
            return HttpResponse("Invalid session get or no metadata")
        return render(request, self.template_name, {"meta_data":meta_data})

    def post(self, request):
        try:
            #JSON view for metadata
            meta_data = request.session.get("meta_data")
            
            if not meta_data:
                return HttpResponse("Invalid session get or no metadata")
            
            del request.session["meta_data"]
            return JsonResponse(meta_data)
            
        except Exception as exc:
            return HttpResponse(f"Error: {exc}")
    
    

def delete_meta_data(request):
    try:
        if request.method == "POST":
            pass
    except Exception as exc:
        return HttpResponse(f"Error: {exc}")


# def valentine(request):
#     return render(request, "valentine.html")