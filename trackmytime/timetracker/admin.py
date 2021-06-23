from django.contrib import admin

from .models import TimeEntry, Customer, WorkDay

# Register your models here.
admin.site.register(TimeEntry)
admin.site.register(Customer)
admin.site.register(WorkDay)
