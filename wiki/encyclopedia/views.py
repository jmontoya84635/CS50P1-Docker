import os.path
import random

from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
import markdown2


class WikiPage(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
        "class": "form-control",
    }))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 4,
    }))


class EditForm(forms.Form):
    content = forms.CharField(label="Edit Content:", widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 10,
    }))


# Home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


# Page that shows up when editing url
def searchResult(request, title):
    # Checks if there is a result for search
    result = util.get_entry(title)
    isFound = False
    if result is not None:
        isFound = True

    # Returns Title, if it was found, and, metadata
    return render(request, "encyclopedia/searchResult.html", {
        "title": title.capitalize(),
        "isFound": isFound,
        # fixme: fix the the title showing up in information about the topic
        "result": markdown2.markdown(result),
    })


# Page that loads when querying with "q"
def searchBar(request):
    # Grabs the q parameter from the get request and does the same as previous func
    search = request.GET.get('q')
    result = util.get_entry(search)
    isFound = False
    subStringEntries = []
    if result is not None:
        isFound = True
    else:
        allEntries = util.list_entries()
        for entry in allEntries:
            if search.lower() in entry.lower():
                subStringEntries.append(entry)

    return render(request, "encyclopedia/searchResult.html", {
        "title": search.capitalize(),
        "isFound": isFound,
        "result": markdown2.markdown(str(result)),
        "foundRelated": False if (len(subStringEntries) == 0) else True,
        "relatedEntries": subStringEntries,

    })


# Page where user can create new page
def addPage(request):
    if request.method == "POST":
        form = WikiPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            allEntries = util.list_entries()
            for entry in allEntries:
                if title.lower() == entry.lower():
                    print("trying to warn user")
                    return render(request, "encyclopedia/addPage.html", {
                        "form": form,
                        "alreadyExist": True
                    })
            filepath = os.path.join('entries', f'{title}.md')
            print(filepath)
            newFile = open(filepath, "x")
            newFile.write("# " + title + "\n\n")
            newFile.write(content)
            return HttpResponseRedirect(f'/wiki/{title}')
        else:
            return
    return render(request, "encyclopedia/addPage.html", {
        "form": WikiPage(),
    })


def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            filepath = os.path.join('entries', f'{title}.md')
            with open(filepath, 'w') as file:
                file.write(f'# {title}\n\n{content}')
            return HttpResponseRedirect(f'/wiki/{title}')
    form = EditForm()
    try:
        content = util.get_entry(title).split('\n')[2:]
    except AttributeError:
        return HttpResponseRedirect(f'/wiki/{title}')
    content = ''.join(content)
    form.fields['content'].initial = content
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form,
    })


def randomEntry(request):
    allEntries = util.list_entries()
    randEntry = allEntries[random.randint(0, len(allEntries)-1)]
    return HttpResponseRedirect(f'/wiki/{randEntry}')
