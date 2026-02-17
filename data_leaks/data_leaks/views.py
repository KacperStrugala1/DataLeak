from django.http import HttpResponse, JsonResponse, Http404, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View

from .forms import UploadFileForm
from .file_type import FileType
from django.core.cache import cache

import logging
import json
import uuid
import re

logger = logging.getLogger(__name__)


class HomeView(View):
    form_class = UploadFileForm
    template_name = "home.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        action = request.POST.get("action")
        
        if action == "show_metadata":
            try:
                form = self.form_class(request.POST, request.FILES)
                if form.is_valid():
                    file = form.cleaned_data["file"]
                    file_name = file.name
                    uploaded_file = form.cleaned_data["file"] 
                    file_id = str(uuid.uuid4())
                    
                    file_content = uploaded_file.read()
                    cache.set(file_id, file_content, timeout=300) 

                    file_type = FileType()
                    file_extension = file_type.get_file_extension(uploaded_file)
                    if re.search("application/pdf", file_extension) or re.search("image/*", file_extension):
                        meta_data = file_type.check_file_format(uploaded_file)
                        
                        request.session["meta_data"] = meta_data
                        request.session["extension"] = file_extension
                        request.session["file_name"] = file_name

                        return redirect(f"/meta_view/?file_id={file_id}")
                    else:
                        return HttpResponse("Invalid extension", status=400)
                else:
                    form = self.form_class()
                    return render(request, "home.html", {"form": form})

            except Exception as exc:
                logger.error(f"Error {exc}")
                return HttpResponse(f"Internal error: {exc}", status=500)

        elif action == "download_without_meta":
            form = self.form_class(request.POST, request.FILES)

            if form.is_valid():
                file = form.cleaned_data["file"]

                file_type = FileType()
                file_name = file.name
                uploaded_file = form.cleaned_data["file"] 
                
                file_extension = file_type.get_file_extension(uploaded_file)
                if re.search("application/pdf", file_extension) or re.search("image/*", file_extension):
                    cleared_file = file_type.delete_file(file)
                    try:
                        response = HttpResponse(
                            cleared_file.getvalue(), content_type="application/octet-stream"
                        )
                        response["Content-Disposition"] = f"attachment; filename={file.name}"
                        return response
                    except Exception as exc:
                        logger.error(f"Error {exc}")
                        return HttpResponse(f"Error: {exc}")
                else:
                    logger.info("Sent invalid extension")
                    return HttpResponse("Invalid extension")
        else:
            logger.info("Wrong operation")
            return HttpResponse("Wrong operation")


class MetaView(View):
    template_name = "meta_view.html"
    form_class = UploadFileForm
    

    def get(self, request):
        try:
            meta_data = request.session.get("meta_data")
            file_id = request.GET.get("file_id")
            if not file_id:
                return HttpResponse("There's no file_id", status=400)

            # del request.session["meta_data"]
        except Exception as exc:
            logger.exception(f"Error with getting data session. Error {exc}")
            return HttpResponseServerError("Server error occured")

        return render(request, self.template_name,  {"file_id": file_id, "meta_data": meta_data})

    def post(self, request):
        try:
            action = request.POST.get("action")
            meta_data = request.session.get("meta_data")
            file_extension = request.session.get("extension")
            file_name = request.session.get("file_name")
            file_type = FileType()

            if action == "show_json":
                return JsonResponse(meta_data, json_dumps_params={"ensure_ascii": False})

            elif action == "download_json":
                response = HttpResponse(
                    json.dumps(meta_data, ensure_ascii=False), content_type="application/json"
                )
                response["Content-Disposition"] = f'attachment; filename="meta_data.json"'
                return response

            elif action == "download_clear_file":
                file_id = request.POST.get("file_id")
                if not file_id:
                    return HttpResponse("No file", status=400)

                file_content = cache.get(file_id)
                if not file_content:
                    return HttpResponse("File does not exists, or session ends", status=404)

                #Add there deleting metadata from that view

                if re.search("application/pdf", file_extension):
                    cleared_file = file_type.delete_file(file_id)
                    response = HttpResponse(cleared_file, content_type="application/octet-stream")
                    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
                    return response
                elif re.search("image/*", file_extension):
                    cleared_file = file_type.delete_file(file_id)
                    response = HttpResponse(cleared_file, content_type=f"{file_extension}")
                    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
                    return response
                
                cache.delete(file_id)

            else:
                if not meta_data:
                    return Http404("Invalid session process or get no metadata")

        except Exception as exc:
            logger.exception(f"Error with getting data session. Error {exc}")
            return HttpResponseServerError("Server error occured")
