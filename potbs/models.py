from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Game(models.Model):
    title = models.CharField(max_length = 64)
    sub_title = models.TextField(blank = True)
    description = models.TextField(blank = True)
    image = models.ImageField(blank = True)
    platform = models.CharField(max_length = 100)
    link = models.URLField(max_length = 200, blank = True)
    launch_date = models.DateField(auto_now = False, auto_now_add = False, null = True)
    created_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.title}"

class Member(models.Model):
    profile_picture = models.ImageField(blank = True )
    username = models.CharField(max_length = 64)
    skills = models.CharField(max_length = 64)
    instagram = models.URLField(max_length = 200, blank = True, null = True)
    itch_profile = models.URLField(max_length = 200, blank = True, null = True)
    bio = models.TextField(blank = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.username} // last modified: {self.last_modified}"

class Event(models.Model):
    event_poster = models.ImageField(blank = True)
    event_name = models.CharField(max_length = 64)
    event_description = models.TextField(blank = True)
    event_date = models.DateTimeField(auto_now = False, null = True)
    event_country = models.CharField(max_length = 64)
    event_city = models.CharField(max_length = 64)
    map_url = models.URLField(max_length = 200, blank = True, null = True)
    created_date = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f"{self.event_name}: {self.event_city}, {self.event_date}"

class Idea(models.Model):
    GAME_GENRE_CHOICES = [
        ("Interactive Story", "Interactive Story"),
        ("Platformer", "Platformer"),
        ("Point & Click", "Point & Click"),
        ("Puzzle", "Puzzle"),
        ("RPG", "RPG"),
        ("Simulation", "Simulation"),
    ]

    MUSIC_GENRE_CHOICES = [
        ("8-bit", "8-bit"),
        ("Ambient", "Ambient"),
        ("Electronic", "Electronic"),
        ("Folk", "Folk"),
        ("Orchestral", "Orchestral"),
        ("Synthwave", "Synthwave")
    ]
    character = models.ImageField(blank = True)
    genre = models.CharField(max_length = 64, choices = GAME_GENRE_CHOICES, blank = True)
    bg_image = models.ImageField(blank = True)
    music_genre = models.CharField(max_length = 64, choices = MUSIC_GENRE_CHOICES, blank = True)
    voice_acting = models.BooleanField(null = True)
    liked_by = models.ManyToManyField(User, blank = True, related_name = "likes" )
    status = models.BooleanField(default = False)
    last_modified = models.DateTimeField(auto_now = True)
