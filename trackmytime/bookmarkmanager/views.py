from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import Bookmark


@login_required
def index(request):

    bookmarks = Bookmark.objects.all()

    return render(request, 'bookmarkmanager/index.html', {'bookmarks': bookmarks})
