from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_title, name="getTitle"),
    path("CreateNewPage/", views.create_new_page, name="CreateNewPage"),
    path("editPage/", views.edit_page, name="editPage"),
    path("randomPage/", views.get_random_page, name="randomPage")
]
