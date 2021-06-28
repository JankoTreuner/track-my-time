from django.shortcuts import render, redirect
from django.db.models import Sum

import readabledelta
import datetime


from .models import Client, TimeEntry, WorkDay


def index(request):

    entries = TimeEntry.objects.all().order_by('-start')

    return render(request, "timetracker/index.html", {'entries': entries})


def overview(request):
    grouped_entries = TimeEntry.objects.filter(booked=False, client__isnull=False,
                                               client__has_booking=True).values('start__date', 'client__name').annotate(
        count=Sum(1))

    for entry in grouped_entries:
        duration_total = datetime.timedelta()
        current_date = entry['start__date']
        entries_of_day = TimeEntry.objects.filter(booked=False, client__isnull=False, client__has_booking=True,
                                                  start__date=current_date)
        for entry_of_day in entries_of_day:
            duration_total = duration_total + entry_of_day.duration
        entry['duration'] = duration_total
        try:
            entry['workinghours'] = WorkDay.objects.get(client__name=entry['client__name'],
                                                        day=current_date.weekday()).workinghours
        except WorkDay.DoesNotExist:
            entry['workinghours'] = datetime.timedelta(0)

        entry['timediff'] = readabledelta.readabledelta(entry['duration'] - entry['workinghours'])

    return render(request, 'timetracker/overview.html', {'entries': grouped_entries})


def add(request):
    TimeEntry.objects.create()

    return redirect('index')


def stop(request, entry_id):
    entry = TimeEntry.objects.get(pk=entry_id)
    entry.end = datetime.datetime.now()
    entry.save()

    return redirect('index')


def clients(request):
    clients = Client.objects.all()

    return render(request, 'timetracker/clients.html',  {'clients': clients})
