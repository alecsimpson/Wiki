from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

import markdown2
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
    # markdowner = Markdown()
    convertedEntry = markdown2.markdown(entry).strip()
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": convertedEntry,
        "random": random.choice(util.list_entries()),
    })


class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': '3', 'label': 'content', 'style': 'resize:none'}))

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


def edit(request):
    try:
        if request.method == "GET":
            if request.GET['title']:
                form = NewEntryForm({'title': request.GET['title'], 'content': util.get_entry(request.GET['title'])})
                # form.title = request.GET['title']
                # form.content = util.get_entry(request.GET['title'])
                return render(request, "encyclopedia/edit.html", {
                    "title": request.GET['title'],
                    "form": form,
                })

        if request.method == "POST":
            form = NewEntryForm(request.POST)
            if form.is_valid():
                util.save_entry(form.cleaned_data['title'], form.cleaned_data['content'])
                return HttpResponseRedirect(reverse("encyclopedia:index"))

    except:
        return HttpResponseRedirect(reverse("encyclopedia:index"))