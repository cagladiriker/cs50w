from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from random import choice
from markdown2 import markdown
from django.contrib import messages

from . import util
import encyclopedia



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() #util.list_entries() returns a list: ['CSS','Django','HTML','Python']
        #we save that list inside "entries" variable to create an ul in index.html
    })

def search(request):
    sub_list = []
    entries = util.list_entries()
    search = request.GET.get("q")

    for entry in entries:
        if search.lower() == entry.lower():
            return redirect("entry", title= search)
        elif search.lower()!=entry.lower() and search.lower() in entry.lower():
            sub_list.append(entry)
    return render(request, "encyclopedia/search.html",{
        "title":search,
        "sub_list":sub_list
    })

    
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        new_entry = request.POST.get("new_entry")
        entries = util.list_entries()

        for entry in entries:
            if title.lower() == entry.lower():
                messages.error(request, f"ERROR: {title} Already Exists.")
                return redirect("new_page")
            
        if title.isupper():
            util.save_entry(title,(new_entry))
        else:
            util.save_entry(title.capitalize(),(new_entry))
        return redirect("entry", title= title)

    else:
        return render(request,"encyclopedia/new_page.html")
         
         
def edit(request,title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title,(content))
        return redirect("entry",title=title)
        
    else:
        return render(request,"encyclopedia/edit.html",{
            "title":title,
            "content":util.get_entry(title)
        })

def entry(request,title): 
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":markdown(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "title":title
        }) 

def random(request):
    title = choice(util.list_entries())
    return redirect("entry",title=title)
