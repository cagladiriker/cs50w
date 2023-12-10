from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import constraints
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
import json



from .models import User, AllPost, Follow

def index(request):
    post_list = AllPost.objects.all().order_by("date").reverse()
    paginator = Paginator(post_list, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": post_list,
        "page_obj": page_obj
    })

@login_required
def new_post(request):
    if request.method == "POST":
       content = request.POST["post_content"]
       new_post = AllPost.objects.create(user = request.user, content = content)
       new_post.save()
       return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    post = AllPost.objects.get(id = post_id)

    if request.user == post.user:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']
        AllPost.objects.filter(id=post_id).update(content=f'{content}')
        return JsonResponse({"message": "Successful", "content": content}, status=200)

    else:
        return JsonResponse({"error": ""}, status=400)

@csrf_exempt
@login_required
def like(request, post_id):
    
    # Saves user and post from the request
    user = request.user

    # Query for requested post
    try:
        post = AllPost.objects.get(pk = post_id)
    except AllPost.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # If the user has liked the post, unlike it
    if (user.likes.filter(pk=post_id).exists()):
        post.liked_by.remove(user)
        likes_post = False
    # If the user doesn't like the post, like it
    else: 
        post.liked_by.add(user)
        likes_post = True
    
    # Save updated no of likes on post
    likes = post.likes()
    
    return JsonResponse({"likesPost": likes_post, "likesCount": likes}, status=200)

def profile(request, username):
    # Submit button is pressed
    if request.method == "POST":
        follower = request.user
        following = User.objects.get(username  = username)
        # User submits the follow button
        if request.POST.get("follow"):
            new_follow = Follow.objects.create(follower = follower, following = following)
            new_follow.save()
        # User submits the unfollow button
        elif request.POST.get("unfollow"):
            delete_follow = Follow.objects.get(follower = follower, following = following)
            delete_follow.delete()
        return HttpResponseRedirect(reverse("profile", kwargs={"username":username}))

    
    else: # Gets the page
        posted_by = User.objects.get(username = username)
        session_user = request.user
        following_number = posted_by.following.count()
        follower_number = posted_by.follower.count()

        if session_user.is_authenticated: #if the user is logged in
            #Check if the user follows someone or not
            try: 
                is_following = Follow.objects.get(follower = session_user, following = posted_by)
            except Follow.DoesNotExist:
                is_following = False
        else: #if the user is not logged in
            is_following = False

        post_list = AllPost.objects.filter(user = posted_by).order_by("date").reverse()
        paginator = Paginator(post_list, 10) # Show 10 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            "posts": post_list,
            "page_obj": page_obj,
            "posted_by": posted_by,
            "following_number": following_number,
            "follower_number": follower_number,
            "session_user": session_user,
            "is_following": is_following
        })
        
@login_required
def following(request, username):
    try:
        all_posts = []
        follow_item = Follow.objects.filter(follower = request.user)
        for item in follow_item:
            posted_by = item.following
            posts = AllPost.objects.filter(user = posted_by).order_by("date").reverse()
            all_posts.append(posts)
        post_list = all_posts
        paginator = Paginator(post_list, 10) # Show 10 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/following.html",{
            "page_obj":page_obj,
            "follow_item": follow_item
        })
    except:
        follow_item = False
        return render(request,"network/following.html",{
            "posts": post_list
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
