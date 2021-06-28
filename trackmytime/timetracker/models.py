from django.db import models
from django.db.models.enums import IntegerChoices
from django.utils import timezone
import datetime
import calendar


def get_week(date):
    """Return the full week (Sunday first) of the week containing the given date.
    'date' may be a datetime or date instance (the same type is returned).
    """
    monday = date - datetime.timedelta(days=date.weekday())
    date = monday
    for n in range(0, 6):
        yield date
        date += datetime.timedelta(days=1)


class Client(models.Model):
    name = models.CharField(max_length=255)

    @property
    def workinghours(self):
        workdays = self.workdays.all()
        workinghours = datetime.timedelta(0)
        for workday in workdays:
            workinghours = workinghours + workday.workinghours

        return workinghours

    @property
    def workedhours(self):
        days_this_week = get_week(datetime.date.today())
        workedhours = datetime.timedelta(0)
        for day in days_this_week:
            timeentries = TimeEntry.objects.filter(date=day, client=self)
            for timeentry in timeentries:
                workedhours = workedhours + timeentry.duration
        return workedhours

    def __str__(self):
        return self.name


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
    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE, related_name='workdays')
    workinghours = models.DurationField(null=True)

    def __str__(self):
        return "%s (%s)" % (self.client, calendar.day_name[self.day])

    class Meta:
        unique_together = ["day", "client"]


class TimeEntry(models.Model):
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField(null=True, blank=True)

    date = models.DateField(default=datetime.date.today)

    client = models.ForeignKey(Client, default=None, null=True, on_delete=models.CASCADE,
                                 related_name='time_entries')

    booked = models.BooleanField(default=False, null=False)

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

    def __str__(self):
        return "%s (%s) - %s (Booked: %s)" % (self.date, self.id, self.client, self.booked)
