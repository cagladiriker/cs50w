from django.contrib import admin
from .models import User, AuctionItem, Bid, Comment, Watchlist, ClosedItem, Category

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionItem)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(ClosedItem)
admin.site.register(Category)



