from django.shortcuts import render, redirect
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title.replace("#", "").replace("*", ""),
        "content": entry_content.replace("#", "").replace("*", "")
    })

def search(request):
    query = request.GET.get('q', '')
    if util.get_entry(query):
        return redirect('entry', query)
    else:
        entries = util.list_entries()
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": results
        })

def create_new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        
        if util.get_entry(title):
            return render(request, "encyclopedia/new_page.html", {
                "error": "An entry with this title already exists."
            })
        
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/new_page.html")

def random_page(request):
    # Add your random page logic here
    return render(request, "encyclopedia/random.html")