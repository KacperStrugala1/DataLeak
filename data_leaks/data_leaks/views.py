from django.http import HttpResponse, JsonResponse, Http404, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View

from .forms import UploadFileForm
from .file_type import FileType
from django.core.cache import cache
from io import BytesIO

import logging
import json
import uuid


logger = logging.getLogger(__name__)


class HomeView(View):
    form_class = UploadFileForm
    template_name = "home.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        action = request.POST.get("action")
        form = self.form_class(request.POST, request.FILES)
        file_type = FileType()
        if action == "show_metadata":
            try:
                if form.is_valid():
                    file = form.cleaned_data["file"]
                    file_name = file.name
                    file_id = str(uuid.uuid4())
                    file_content = file.read()
                    file.seek(0)
                    cache.set(file_id, file_content, timeout=300) 

                    file_extension = file.content_type
                    if file_type.is_supported(file_extension):
                        #get proper metadata for file extension
                        meta_data = file_type.check_file_meta(file)
                        
                        request.session["meta_data"] = meta_data
                        request.session["extension"] = file_extension
                        request.session["file_name"] = file_name
                        request.session["file_id"] = file_id

                        return redirect("meta_view")
                    else:
                        return HttpResponse("Invalid extension", status=400)
                else:
                    return render(request, "home.html", {"form": form})

            except Exception as exc:
                logger.error(f"Error {exc}")
                return HttpResponse(f"Internal error: {exc}", status=500)

        elif action == "download_without_meta":

            if form.is_valid():
                file = form.cleaned_data["file"]
                file_name = file.name 
                file_extension = file.content_type

                if file_extension is not None:
                    cleared_file = file_type.delete_file_meta(file)
                    try:
                        response = HttpResponse(
                            cleared_file, 
                            content_type="application/octet-stream"
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
                logger.info("Invalid form")
                return HttpResponse("Invalid send file")
        else:
            logger.info("Wrong operation")
            return HttpResponse("Wrong operation")


class MetaView(View):
    template_name = "meta_view.html"
    form_class = UploadFileForm
    

    def get(self, request):
        try:
            meta_data = request.session.get("meta_data")
            file_id = request.session.get("file_id")
            if not file_id:
                raise Http404("No active session file")
            
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
            file_id = request.session.get("file_id")
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

                if not file_id:
                    return HttpResponse("No file", status=400)

                file_content = cache.get(file_id)
                if not file_content:
                    return HttpResponse("File does not exists, or session ends", status=404)

                file_object = BytesIO(file_content)
                file_object.content_type = file_extension

                if file_type.is_supported(file_extension):
                    cleared_file = file_type.delete_file_meta(file_object)
                    response = HttpResponse(cleared_file, content_type=f"{file_extension}")
                    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
                    cache.delete(file_id)
                    return response
                else:
                    return HttpResponse("Invalid extension")

            else:
                if not meta_data:
                    raise Http404("Invalid session process or get no metadata")

        except Exception as exc:
            logger.exception(f"Error with getting data session. Error {exc}")
            return HttpResponseServerError("Server error occured")
