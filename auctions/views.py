from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required


from .models import User, AuctionItem, Watchlist, Bid, ClosedItem, Comment, Category


#class CreateNewListing(forms.Form):
    #title = forms.CharField(widget=forms.TextInput(attrs={'style':'width:400px;','class':'form-control'}),label="Title")
    #description = forms.CharField(label = 'Description', widget=forms.Textarea(attrs={'style':'width:400px;height:100px','class':'form-control'}))
    #price = forms.DecimalField(widget=forms.NumberInput(attrs={'style':'width:100px;','class':'form-control'}),min_value=0.1, label="Price ($):")
    #image = forms.FileField(widget=forms.ClearableFileInput(attrs={'style':'width:400px;','class':'form-control'}), required = False, label= "Upload Image")
    #category = forms.CharField(widget=forms.TextInput(attrs={'style':'width:400px;','class':'form-control'}), required = False, label="Cetagory:")

def index(request):
    return render(request, "auctions/index.html",{
        "auctions" : AuctionItem.objects.all()
    })

# Create New Listing
@login_required
def create_listing(request):
    if request.method == "POST": #if the create listing form is submitted
        title = request.POST["title"] #get the provided title
        description = request.POST["description"] #get the provided description
        price = request.POST["price"] #get the provided price
        image = request.POST["image"] #get the provided image
        category = request.POST["category"] #get the provided category

        try:
            all_categories = Category.objects.get(name = category.capitalize())
            item = AuctionItem.objects.create( #create new auction item with given properties
            user = request.user,
            title = title,
            description = description,
            price = price,
            image = image,
            category = all_categories
            )
        except:
            all_categories = Category.objects.create(name = category.capitalize())
            item = AuctionItem.objects.create( #create new auction item with given properties
            user = request.user,
            title = title,
            description = description,
            price = price,
            image = image,
            category = all_categories
            )
        
        item.save()

        return HttpResponseRedirect(reverse("index")) #after submitting the form, redirect user to the main page

    return render(request, "auctions/create_listing.html")

# Display specific listing page
def listing(request,listing_id): 
    listing = AuctionItem.objects.get(id = listing_id)
    user = request.user
    added = Watchlist.objects.filter(watchlisted_item_id=listing_id, user = user) #to check if the item is added to watchlist or not
    comments = Comment.objects.filter(comment_item_id = listing_id, user = user)
    try:
        bid = Bid.objects.get(bid_item_id = listing_id)
    except Bid.DoesNotExist:
        bid = Bid.objects.create(bid_item_id = listing_id, user = listing.user, bid = listing.price)
    
    if request.method == "POST":
        if request.POST.get('add'):
            add_item = Watchlist.objects.create(watchlisted_item_id=listing_id, user = user)
        if request.POST.get('remove'):
            deleted_item = Watchlist.objects.get(watchlisted_item_id=listing_id, user = user)
            deleted_item.delete()

        if request.POST.get('close'):
            closed_item = ClosedItem.objects.create(
                user = listing.user,
                winner = bid.user,
                winning_bid = bid.bid,
                id = listing_id, 
                title= listing.title, 
                description = listing.description, 
                price = listing.price, 
                image = listing.image,
                category = listing.category,
                date = listing.date 
                )
            deleted_item = AuctionItem.objects.get(id = listing.id)
            deleted_item.delete()
            return render(request, "auctions/closed.html",{
                "closed_items": ClosedItem.objects.all(),
                "user": user,
                "winning_bid":bid.bid,
                "winner":bid.user
            })
            

        if request.POST.get('bid'):
            new_bid = int(request.POST.get("bid_value"))
            if bid:
                if new_bid <= bid.bid:
                    return render(request, "auctions/listing.html",{
                        "listing":listing,
                        "user":user,
                        "added":added,
                        "comments":comments,
                        "bid":bid.bid,
                        "alert_message":"Your Bid should be higher than the Current Bid!"
                    })
                else:
                    bid = Bid.objects.filter(bid_item_id = listing_id) #get the bids that wew submitted to the listing with id listing_id
                    if bid:
                        bid.delete()
                    new = Bid.objects.create(bid_item_id = listing_id, user = user)
                    new.bid = new_bid
                    new.save()
                    return render(request, "auctions/listing.html",{
                        "listing":listing,
                        "user":user,
                        "added":added,
                        "comments":comments,
                        "bid":new.bid,
                        "success_message":f"You have bidded ${new_bid}"
                    })
            else:
                if new_bid <= listing.price:
                    return render(request, "auctions/listing.html",{
                            "listing":listing,
                            "user":user,
                            "added":added,
                            "comments":comments,
                            "bid":bid,
                            "alert_message":"Your Bid should be higher than the Current Bid!"
                        })

                else:
                    new = Bid.objects.create(bid_item_id = listing_id, user = user)
                    new.bid = new_bid
                    new.save()
                    return render(request, "auctions/listing.html",{
                        "listing":listing,
                        "user":user,
                        "added":added,
                        "comments":comments,
                        "bid":new,
                        "success_message":f"You have bidded ${new_bid}"
                    })
                    
            
        if request.POST.get('post_comment'):
            new_comment = request.POST["new_comment"]
            add_comment = Comment.objects.create(
                comment_item_id = listing_id, 
                user = user, 
                comment = request.POST["new_comment"] 
                )

    return render(request, "auctions/listing.html",{
        "listing":listing,
        "user":user,
        "added":added,
        "comments":comments,
        "bid":bid.bid
    })

# Display the watclist of logged in user
@login_required
def watchlist(request,user):
    user = request.user #get the watclist of the logged in user
    item_list = AuctionItem.objects.filter(watchlist__user=user) #list the items that were added to the watclist of that user
    return render(request, "auctions/watchlist.html",{
        "item_list" : item_list
    })

@login_required
def closed(request):
    user = request.user
    closed_items = ClosedItem.objects.all()
    return render(request,"auctions/closed.html",{
        "closed_items":closed_items,
        "user":user
    })


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    items = AuctionItem.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "items" : items,
        "name" : category.name
    })

def all_categories(request):
    categories = Category.objects.all()
    return render(request,"auctions/all_categories.html",{
        "categories":categories
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

