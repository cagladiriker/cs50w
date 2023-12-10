from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AllPost(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "posted_by")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    liked_by = models.ManyToManyField(User, blank=True, related_name="likes")

    def likes(self):
        """Returns total number of likes on post"""
        return self.liked_by.all().count()

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "following", null = True)
    following = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "follower", null = True)

    def __str__(self):
        return f"Follower: {self.follower} / Following: {self.following}"