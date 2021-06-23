from django.db import models
from django.db.models.enums import IntegerChoices
from django.utils import timezone
import datetime


class Customer(models.Model):
    name = models.CharField(max_length=255)


class WorkDay(models.Model):

    class WorkDays(IntegerChoices):
        MONDAY = 0
        TUSDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

    day = models.IntegerField(choices=WorkDays.choices)
    customer = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE, related_name='workdays')
    workinghours = models.DurationField(null=True)

    class Meta:
        unique_together = ["day", "customer"]


class TimeEntry(models.Model):
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField(null=True, blank=True)

    date = models.DateField(default=datetime.date.today)

    customer = models.ForeignKey(Customer, default=None, null=True, on_delete=models.CASCADE,
                                 related_name='time_entries')

    @property
    def is_active(self):
        return self.end is None

    @property
    def duration(self):
        if self.end is None:
            end = timezone.now()
        else:
            end = self.end

        return end - self.start
