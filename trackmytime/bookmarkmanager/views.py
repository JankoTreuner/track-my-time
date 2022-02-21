from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

from .forms import AddEntryForm
from .models import Bookmark
from timetracker.models import Client


@login_required
def index(request):

    bookmarks = Bookmark.objects.all()

    form = AddEntryForm()

    return render(request, 'bookmarkmanager/index.html', {'bookmarks': bookmarks, 'form': form })


@login_required
def add(request):

        # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = AddEntryForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            client_name = form.cleaned_data['client']
            url = form.cleaned_data['url']
            if(client_name):
                client = Client.objects.get(name=client_name)
            else:
                client = None
            Bookmark.objects.create(client=client, url=url)

            return redirect('bookmarks')

    return redirect('bookmarks')
