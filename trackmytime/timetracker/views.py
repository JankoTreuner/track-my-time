from django.shortcuts import render, redirect
from django.db.models import Sum, Count
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
    clients = Client.objects.all()
    entries = list()
    for client in clients:
        year_infos = list()
        for year in client.years:
            a = client.workedhours_year(year)
            b = client.workinghours_year(year)

            year_info = {'year': year, 'hours': a, 'expected': b, 'diff': readabledelta.readabledelta(a-b)}
            year_infos.append(year_info)
        
        entries.append({'client': client, 'years': year_infos})
    
    return render(request, 'timetracker/overview.html', {'entries': entries})


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


def unbooked_by_date(request):
    unbooked_entries = TimeEntry.objects.filter(booked=False, client__isnull=False, client__has_booking=True).values(
                                                'date', 'client__name').annotate(datecount=Count('date'))

    for entry in unbooked_entries:
        duration = datetime.timedelta()
        entries = TimeEntry.objects.filter(booked=False, client__isnull=False, client__has_booking=True,
                                           date=entry['date'], client__name=entry['client__name'])
        for e in entries:
            duration = duration + e.duration
        entry['duration'] = duration

    return render(request, 'timetracker/unbooked_by_date.html', {'unbooked_entries': unbooked_entries})


@login_required()
def mark_as_booked(request, entry_id):
    entry = TimeEntry.objects.get(pk=entry_id)
    entry.booked = True
    entry.save()

    return redirect('unbooked')


@login_required()
def mark_as_booked_by_date(request, date, clientname):
    entries = TimeEntry.objects.filter(date=date, client__name=clientname, booked=False)
    for entry in entries:
        print(entry)
        entry.booked = True
        entry.save()
    return redirect('unbooked-by-date')


@login_required()
def delete(request, entry_id):
    entry = TimeEntry.objects.get(pk=entry_id)
    entry.delete()

    return redirect('index')
