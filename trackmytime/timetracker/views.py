from django.shortcuts import render, redirect
from django.db.models import Sum

import datetime


from .models import TimeEntry


def index(request):

    entries = TimeEntry.objects.all().order_by('-start')

    return render(request, "timetracker/index.html", {'entries': entries})


def overview(request):
    grouped_entries = TimeEntry.objects.all().values('start__date').annotate(count=Sum(1))

    for entry in grouped_entries:
        duration_total = datetime.timedelta()
        entries_of_day = TimeEntry.objects.filter(start__date=entry['start__date'])
        for entry_of_day in entries_of_day:
            duration_total = duration_total + entry_of_day.duration
        entry['duration'] = duration_total

    return render(request, 'timetracker/overview.html', {'entries': grouped_entries})


def add(request):
    TimeEntry.objects.create()

    return redirect('index')


def stop(request, entry_id):
    entry = TimeEntry.objects.get(pk=entry_id)
    entry.end = datetime.datetime.now()
    entry.save()

    return redirect('index')
