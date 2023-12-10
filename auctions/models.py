from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length = 64, null = True)

    def __str__(self):
        return f"{self.name}"


class AuctionItem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "created_by")
    title = models.CharField(max_length = 64)
    description = models.TextField()
    price = models.DecimalField(max_digits = 100 ,decimal_places = 2)
    image = models.URLField(blank = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "item_category")
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Item {self.id}: {self.title} / ${self.price}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_bid", null = True)
    bid_item = models.ForeignKey(AuctionItem, on_delete = models.CASCADE, related_name = "item_bid")
    bid = models.DecimalField(max_digits = 100 , decimal_places = 2, null= True, default = 0)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Item: {self.bid_item.id}: {self.bid_item.title} / Starting Bid: ${self.bid_item.price} / Current Bid: ${self.bid}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, name = "user")
    comment_item = models.ForeignKey(AuctionItem, on_delete = models.CASCADE, related_name = "item_comment")
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Commented On Item: {self.comment_item.id} / {self.user}: {self.comment} / {self.date}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, name = "user")
    item = models.ForeignKey(AuctionItem,on_delete = models.CASCADE, name = "watchlisted_item", null=True)

    def __str__(self):
        return f"Username: {self.user} / {self.watchlisted_item} "


class ClosedItem(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user", null = True)
    #winner = models.CharField(max_length = 64, null = True)
    winner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "winner", null = True)
    title = models.CharField(max_length = 64, null = True)
    description = models.TextField(null = True)
    price = models.DecimalField(max_digits = 100 ,decimal_places = 2, null = True)
    winning_bid = models.DecimalField(max_digits = 100 ,decimal_places = 2, null = True)
    image = models.URLField(blank = True, null = True)
    category = models.CharField(max_length = 64, blank = True)
    date = models.DateTimeField(auto_now_add = True, null = True, blank = True)

    def __str__(self):
        return f"Closed Item: {self.id}: {self.title} / Winner: {self.winner}"

