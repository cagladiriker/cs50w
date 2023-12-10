from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about",views.about, name="about"),
    path("contact",views.contact, name="contact"),
    path("games",views.games, name="games"),
    path("events",views.events, name="events"),
    path("new_game",views.new_game, name="new_game"),
    path("new_event",views.new_event, name="new_event"),
    path("edit_profile/<int:member_id>",views.edit_profile, name="edit_profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("close/<int:idea_id>", views.close, name = "close"),
    path("like/<int:idea_id>", views.like, name = "like")
]
