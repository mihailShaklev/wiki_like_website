from django.shortcuts import render
import random
import markdown2
import html2markdown
from . import util


def index(request):

    if request.GET.get('q'):
        query = request.GET.get('q')
        list_of_entries = util.list_entries()
        return search_handler(request, query, list_of_entries)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def get_title(request, title):

    if request.GET.get('q'):
        query = request.GET.get('q')
        list_of_entries = util.list_entries()
        return search_handler(request, query, list_of_entries)

    else:

        if util.get_entry(title):
            return render(request, "encyclopedia/entry.html", {
             "content": markdown2.markdown(util.get_entry(title)), "title": title
            })
        else:
            return render(request, "encyclopedia/pageNotFound.html")


def create_new_page(request):

    if request.GET.get('q'):
        query = request.GET.get('q')
        list_of_entries = util.list_entries()
        return search_handler(request, query, list_of_entries)
    elif request.GET.get('title') and request.GET.get('content'):
        title = str(request.GET.get('title'))
        content = str(request.GET.get('content'))

        if title in util.list_entries():
            error = "Entry already exists!"
            return render(request, "encyclopedia/CreateNewPage.html", {"error": error})
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {"content": markdown2.markdown(util.get_entry(title)), "title": title})

    return render(request, "encyclopedia/CreateNewPage.html")


def edit_page(request):

    if request.GET.get('q'):
        query = request.GET.get('q')
        list_of_entries = util.list_entries()
        return search_handler(request, query, list_of_entries)

    if request.GET.get('oldTitle') and request.GET.get('oldContent'):
        oldTitle = request.GET.get('oldTitle')
        oldContent = html2markdown.convert(request.GET.get('oldContent'))
        return render(request, "encyclopedia/editPage.html", {"oldTitle": oldTitle, "oldContent": oldContent})

    if request.GET.get('title') and request.GET.get('content'):
        title = request.GET.get('title')
        content = request.GET.get('content')
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {"content": markdown2.markdown(content), "title": title})


def get_random_page(request):

    list_of_entries = util.list_entries()

    if request.GET.get('q'):
        query = request.GET.get('q')
        return search_handler(request, query, list_of_entries)

    random_entry = str(random.choice(list_of_entries))
    return render(request, "encyclopedia/entry.html", {
        "content": markdown2.markdown(util.get_entry(random_entry)), "title": random_entry})


def search_handler(request, query, list_of_entries):

    result_list = []

    for entry in list_of_entries:
        if entry == query:
            return render(request, "encyclopedia/entry.html", {
                "content": markdown2.markdown(util.get_entry(entry)), "title": entry
            })
        elif query in entry:
            result_list.append(entry)

    if result_list:
        return render(request, "encyclopedia/search_results.html", {
            "results": result_list
        })
    else:
        return render(request, "encyclopedia/queryNotFound.html", {"query": query})
