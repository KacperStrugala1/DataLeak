from django.http import HttpResponse, JsonResponse, Http404, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View

from . import forms
from .file_type import FileType

import logging
import json

logger = logging.getLogger(__name__)


class HomeView(View):
    form_class = forms.UploadFileForm
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
                    file_type = FileType()
                    if file_type.get_file_extension(file) in ("pdf", "image"):
                        meta_data = file_type.check_file_format(file)
                        logger.info(meta_data)
                        # sending meta_data in session to meta_view
                        request.session["meta_data"] = meta_data

                        return redirect("meta_view")
                    else:
                        logger.info("Sent invalid extension")
                        return HttpResponse("Invalid extension")
                else:
                    form = forms.UploadFileForm()
                    return render(request, "home.html", {"form": form})

            except Exception as exc:
                logger.error(f"Error {exc}")
                return HttpResponse(f"Internal error: {exc}", status=500)

        elif action == "download_without_meta":
            form = self.form_class(request.POST, request.FILES)

            if form.is_valid():
                file = form.cleaned_data["file"]

                file_type = FileType()
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
            logger.info("Wrong operation")
            return HttpResponse("Wrong operation")


class MetaView(View):
    template_name = "meta_view.html"
    form_class = forms.UploadFileForm

    def get(self, request):
        try:
            meta_data = request.session.get("meta_data")
            # del request.session["meta_data"]
        except Exception as exc:
            logger.exception(f"Error with getting data session. Error {exc}")
            return HttpResponseServerError("Server error occured")

        return render(request, self.template_name, {"meta_data": meta_data})

    def post(self, request):
        try:
            action = request.POST.get("action")
            meta_data = request.session.get("meta_data")

            if action == "show_json":
                return JsonResponse(meta_data, json_dumps_params={"ensure_ascii": False})

            # add here changing to proper filename
            elif action == "download_json":
                response = HttpResponse(
                    json.dumps(meta_data, ensure_ascii=False), content_type="application/json"
                )
                response["Content-Disposition"] = 'attachment; filename="file.json"'
                return response

            # repair downloading
            elif action == "download_clear_file":
                # pass a file from homeview
                form = self.form_class(request.POST, request.FILES)
                if form.is_valid():
                    file = form.cleaned_data["file"]
                    file_type = FileType()
                    meta_data = file_type.delete_file(file)
                try:
                    response = HttpResponse(file.getvalue(), content_type="application/pdf")
                    response["Content-Disposition"] = f"attachment; filename=filename"
                    return response

                except Exception as exc:
                    logger.error(f"Error {exc}")
                    return HttpResponse(f"Error: {exc}")
            else:
                if not meta_data:
                    return Http404("Invalid session process or get no metadata")

        except Exception as exc:
            logger.exception(f"Error with getting data session. Error {exc}")
            return HttpResponseServerError("Server error occured")
