from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

import random

from . import util

def index(request):
    try: 
        if request.GET['q']:
            results = [i for i in util.list_entries() if request.GET['q'].lower() in i.lower()]
            return render(request, "encyclopedia/search.html", {
                'results': results,
                "random": random.choice(util.list_entries()),
            })
    except: 
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "random": random.choice(util.list_entries()),
        })



def entry(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry,
        "random": random.choice(util.list_entries()),
    })


class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data['title'], form.cleaned_data['content'])
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    
    return render(request, "encyclopedia/new.html", {
        "random": random.choice(util.list_entries()),
        "form": NewEntryForm(),
    })
