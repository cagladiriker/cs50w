from django.contrib import admin
from .models import User, Game, Member, Event, Idea

# Register your models here.
admin.site.register(User)
admin.site.register(Game)
admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Idea)
