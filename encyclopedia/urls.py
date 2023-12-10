from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.search, name= "search"),
    path("new",views.new_page, name="new_page"),
    path("edit/<title>",views.edit, name= "edit"),
    path("random",views.random, name="random"),
    path("<str:title>",views.entry, name="entry")
]
