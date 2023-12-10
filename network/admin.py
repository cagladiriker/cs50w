from django.contrib import admin
from .models import User, AllPost, Follow
# Register your models here.
admin.site.register(User)
admin.site.register(AllPost)
admin.site.register(Follow)
