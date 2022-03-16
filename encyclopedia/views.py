from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import markdown2
import random

from . import util

class AddPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
        })
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    title = util.get_entry(title)
    # if we check util get entry and inforation is available
    if title:
        # NOW Check to see if we need to define the variable first - title and content
        content = markdown2.markdown(title)
        # display title of the page
        # display content of the page
        context = {
            "title": title,
            "content": content,
        }

        return render(request, "encyclopedia/entrypage.html", context)
    # if we check util get entry and information is not available
        # display error page 
    else:
        return render(request, "encyclopedia/errorpage.html")

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        entries = util.list_entries()
        content = markdown2.markdown(query)
        search_list = []

        for entry in entries:
            if query.upper() in entry.upper():
                search_list.append(entry)

        for entry in entries:
            if query.upper() == entry.upper():

                context = {
                   "entry": content,
                    "query": query
                }
                return render(request, "encyclopedia/entrypage.html", context)

            elif search_list != []:
                return render(request, "encyclopedia/search.html", {
                    "entries": search_list
                })
                
            else:
                return render(request, "encyclopedia/errorpage.html", {
                    "querytitle": query
                })


def add_page(request):
    if request.method == "POST":
        form = AddPageForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            entries = util.list_entries()
            for entry in entries:
                if title.upper() == entry.upper():
                    return render(request, "encyclopedia/exist.html")
            util.save_entry(title, content)
            return redirect('encyclopedia:entrypage', title=title)
    else:
        return render(request, "encyclopedia/addpage.html", {
            "form": AddPageForm()
        })

def edit_page(request, title):
    if request.method == "GET":
        title = title
        content = util.get_entry(title)
        form = AddPageForm({"content": title})
        return render(request,"encyclopedia/editpage.html", {"form": form, "title": title})

    form = AddPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")

        util.save_entry(title=title, content=content)
        return redirect('encyclopedia:entrypage', title)


def random_page(request):
    entries = util.list_entries()
    random_entries = random.choice(entries)
    return redirect('encyclopedia:entrypage', title=random_entries)

