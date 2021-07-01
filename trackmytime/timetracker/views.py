from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import AddEntryForm
from django.contrib.auth.decorators import login_required
import readabledelta
import datetime


from .models import Client, TimeEntry, WorkDay


@login_required()
def index(request):

    entries = TimeEntry.objects.all().order_by('-start')
    clients = Client.objects.all()

    form = AddEntryForm()

    return render(request, "timetracker/index.html", {'entries': entries, 'clients': clients, 'form': form})


@login_required()
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


@login_required()
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
            client = Client.objects.get(name=client_name)
            TimeEntry.objects.create(client=client)

            return redirect('index')

    return redirect('index')


@login_required()
def stop(request, entry_id):
    entry = TimeEntry.objects.get(pk=entry_id)
    entry.end = datetime.datetime.now()
    entry.save()

    return redirect('index')


@login_required()
def clients(request):
    clients = Client.objects.all()

    return render(request, 'timetracker/clients.html',  {'clients': clients})


@login_required()
def unbooked(request):
    unbooked_entries = TimeEntry.objects.filter(booked=False, client__isnull=False, client__has_booking=True)

    return render(request, 'timetracker/unbooked.html', {'unbooked_entries': unbooked_entries})


@login_required()
def mark_as_booked(request, entry_id):
    entry = TimeEntry.objects.get(pk=entry_id)
    entry.booked = True
    entry.save()

    return redirect('unbooked')


@login_required()
def delete(request, entry_id):
    entry = TimeEntry.objects.get(pk=entry_id)
    entry.delete()

    return redirect('index')
