from django.contrib import admin
from django.urls import path
from django.views.generic import View
from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home_view"),
    path("meta_view/", views.MetaView.as_view(), name="meta_view"),
    #path("valentine/", views.valentine, name="valentine"),
    path('admin/', admin.site.urls),
]
