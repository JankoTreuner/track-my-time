from django.shortcuts import render, redirect
from django.db.models import Sum

import readabledelta
import datetime


from .models import Customer, TimeEntry, WorkDay


def index(request):

    entries = TimeEntry.objects.all().order_by('-start')

    return render(request, "timetracker/index.html", {'entries': entries})


def overview(request):
    grouped_entries = TimeEntry.objects.filter(booked=False).values('start__date', 'customer__name').annotate(
        count=Sum(1))

    for entry in grouped_entries:
        duration_total = datetime.timedelta()
        current_date = entry['start__date']
        entries_of_day = TimeEntry.objects.filter(booked=False, start__date=current_date)
        for entry_of_day in entries_of_day:
            duration_total = duration_total + entry_of_day.duration
        entry['duration'] = duration_total
        try:
            entry['workinghours'] = WorkDay.objects.get(customer__name=entry['customer__name'],
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


def customers(request):
    customers = Customer.objects.all()

    return render(request, 'timetracker/customers.html',  {'customers': customers})
