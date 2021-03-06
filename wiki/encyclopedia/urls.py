from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("<str:title>", views.entry, name="entry"),
]
