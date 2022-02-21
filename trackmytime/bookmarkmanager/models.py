from django.db import models

import datetime

from timetracker.models import Client


class Bookmark(models.Model):

    url = models.URLField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
