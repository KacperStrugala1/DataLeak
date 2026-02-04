from django.http import HttpResponse, request


def homeview():
    return HttpResponse(request, "Hello world")