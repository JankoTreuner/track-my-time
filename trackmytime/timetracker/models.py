from django.db import models
from django.utils import timezone
import datetime


class TimeEntry(models.Model):
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField(null=True)

    date = models.DateField(default=datetime.date.today)

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
