from django.contrib import admin

from .models import Holiday, TimeEntry, Client, WorkDay

# Register your models here.
admin.site.register(TimeEntry)
admin.site.register(Client)
admin.site.register(WorkDay)
admin.site.register(Holiday)
