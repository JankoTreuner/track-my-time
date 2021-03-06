from django.db import models
from django.db.models.enums import IntegerChoices
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.conf import settings
import datetime
import calendar


class UserBasedModel(models.Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    class Meta:
        abstract = True


def get_week(date):
    """Return the full week (Sunday first) of the week containing the given date.
    'date' may be a datetime or date instance (the same type is returned).
    """
    monday = date - datetime.timedelta(days=date.weekday())
    date = monday
    for n in range(0, 6):
        yield date
        date += datetime.timedelta(days=1)


class Client(UserBasedModel):
    name = models.CharField(max_length=255)
    has_booking = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True)

    @property
    def workinghours(self):
        workdays = self.workdays.all()
        today = datetime.date.today()
        dates = [today + datetime.timedelta(days=i) for i in range(0-today.weekday(), 7-today.weekday())]

        workinghours = datetime.timedelta(0)
        for date in dates:
            try:
                workday = workdays.get(day=date.weekday())
                holiay = Holiday.objects.filter(start__lte=date, end__gte=date)
                is_holiday = holiay.count() > 0
            except WorkDay.DoesNotExist:
                workday = None
                pass
            if(workday and not is_holiday):
                workinghours = workinghours + workday.workinghours

        return workinghours

    @property
    def years(self):
        if self.created_at is None:
            # Current year
            return [datetime.date.today().year]
        else:
            # Any year since created
            start_year = self.created_at.year
            current_year = datetime.date.today().year
            return [current_year - i for i in range(0, current_year+1-start_year)]

    def workedhours_year(self, year=datetime.date.today().year):
        tes = TimeEntry.objects.filter(client=self, date__year=year)

        worked = datetime.timedelta(0)
        for te in tes:
            worked = worked + te.duration

        return worked

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + datetime.timedelta(n)

    def workinghours_year(self, year=datetime.date.today().year):

        if self.created_at is None:
            start = datetime.date(year=year, month=1, day=1)
        else:
            if year == self.created_at.year:
                
                start = datetime.date(year=self.created_at.year, month=self.created_at.month, day=self.created_at.day)
            else:
                start = datetime.date(year=year, month=1, day=1)

        if year is datetime.date.today().year:
            end = datetime.date.today()
        else:
            end = datetime.date(year=year, month=12, day=31)


        workdays = self.workdays.all()
        expected = datetime.timedelta(0)
        for single_date in self.daterange(start, end):
            try:
                workday = workdays.get(day=single_date.weekday())
                holiay = Holiday.objects.filter(start__lte=single_date, end__gte=single_date)
                is_holiday = holiay.count() > 0
            except WorkDay.DoesNotExist:
                workday = None
                pass
            if(workday and not is_holiday):
                expected = expected + workday.workinghours

        return expected


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


class Holiday(UserBasedModel):
    start = models.DateField()
    end = models.DateField()
    client = models.ManyToManyField(Client, related_name='holiday')


class WorkDay(UserBasedModel):

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


class TimeEntry(UserBasedModel):
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

    @property
    def is_booked(self):
        if self.client and self.client.has_booking:
            return self.booked
        else:
            return True

    def __str__(self):
        return "%s (%s) - %s (Booked: %s, Active %s)" % (self.date, self.id, self.client, self.booked, self.is_active)
