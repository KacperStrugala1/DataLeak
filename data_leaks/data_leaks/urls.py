from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.asView(), name="home_view"),
    path("meta_view/", views.meta_view, name="meta_view"),
    path('admin/', admin.site.urls),
]
