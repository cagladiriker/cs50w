from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from .models import User, Game, Member, Event, Idea


def index(request):
    if request.method == "POST":
        genre = request.POST["genre"]
        music_genre = request.POST["music"]
        voice_acting = True if request.POST.get("voiceacting") == 'on' else False

        if 'character' in request.FILES:
            character = request.FILES['character']
        else:
            character = None

        if 'bg_image' in request.FILES:
            bg_image = request.FILES['bg_image']
        else:
            bg_image = None
        
        submitted_idea = Idea.objects.create(
            character = character,
            bg_image = bg_image,
            genre = genre,
            music_genre = music_genre,
            voice_acting = voice_acting
            )
        submitted_idea.save()
        return HttpResponseRedirect(reverse("index"))
    games = Game.objects.all()
    events = Event.objects.all()
    ideas = Idea.objects.all().order_by("status", "last_modified")
    return render(request, 'potbs/index.html', {
        "games": games,
        "events": events,
        "ideas": ideas
    })

@csrf_exempt
@login_required
def close(request, idea_id):
    try:
        idea = Idea.objects.get(pk=idea_id)
    except Idea.DoesNotExist:
        return JsonResponse({"error": "Idea not found."}, status=404)
    
    # Update the status to True and save
    idea.status = True
    idea.save()
    
    return JsonResponse({"status": True}, status=200)


@csrf_exempt
@login_required
def like(request, idea_id):
    
    # Saves user and idea from the request
    user = request.user

    # Query for requested idea
    try:
        idea = Idea.objects.get(pk = idea_id)
    except Idea.DoesNotExist:
        return JsonResponse({"error": "Object not found"}, status=404)

    # If the user has liked the idea, unlike it
    if (user.likes.filter(pk=idea_id).exists()):
        idea.liked_by.remove(user)
        likes_idea = False
    # If the user doesn't like the idea, like it
    else: 
        idea.liked_by.add(user)
        likes_idea = True
    
    # Save updated no of likes on idea
    likes = idea.liked_by.count()
    
    return JsonResponse({"likesIdea": likes_idea, "likesCount": likes}, status=200)

def about(request):
    team_members = Member.objects.all().order_by("id")
    return render(request, "potbs/about.html",{
        "team_members":team_members
    })

def contact(request):
    return render(request, "potbs/contact.html")


def events(request):
    events = Event.objects.all().order_by("created_date").reverse()
    return render(request, "potbs/events.html",{
        "events":events
    })

def games(request):
    games = Game.objects.all().order_by("created_date").reverse()
    return render(request, "potbs/games.html",{
        "games":games
    })

def new_game(request):
    if request.method == "POST":
        title = request.POST["title"]
        sub_title = request.POST["sub_title"]
        description = request.POST["description"]
        platform = request.POST["platform"]
        game_link = request.POST["game_link"]
        launch_date = request.POST["launch_date"]

        if 'thumbnail' in request.FILES:
            image = request.FILES['thumbnail']
        else:
            image = None

        submitted_game = Game.objects.create(
            title = title,
            sub_title = sub_title,
            description = description,
            image = image,
            platform = platform,
            link = game_link,
            launch_date = launch_date
            )
        submitted_game.save()
        return HttpResponseRedirect(reverse("games"))
    return render(request, "potbs/games.html")

def new_event(request):
    if request.method == "POST":
        event_name = request.POST["name"]
        event_description = request.POST["description"]
        event_date = request.POST["date"]
        event_country = request.POST["country"]
        event_city = request.POST["city"]
        map_url = request.POST["map_url"]

        if 'poster' in request.FILES:
            event_poster = request.FILES['poster']
        else:
            event_poster = None

        submitted_event = Event.objects.create(
            event_poster = event_poster,
            event_name = event_name,
            event_description = event_description,
            event_date = event_date,
            event_country = event_country,
            event_city = event_city,
            map_url = map_url
            )
        submitted_event.save()
        return HttpResponseRedirect(reverse("events"))
    return render(request, "potbs/events.html")
    

@csrf_exempt
def edit_profile(request, member_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    team_members = Member.objects.get(id = member_id)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    skills = body['skills']
    instagram = body['instagram']
    itch_profile = body['itch_profile']
    bio = body['bio']
    Member.objects.filter(id=member_id).update(username=f'{username}',skills=f'{skills}',instagram=f'{instagram}',itch_profile=f'{itch_profile}',bio=f'{bio}')
    return JsonResponse({"message": "Successful", "username": username, "skills": skills, "instagram":instagram, "itch_profile":itch_profile, "bio": bio}, status=200)

        

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
            return render(request, "potbs/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "potbs/index.html")


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
            return render(request, "potbs/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "potbs/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "potbs/register.html")

