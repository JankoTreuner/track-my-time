from django.db import models

import datetime


class Bookmark(models.Model):

    url = models.URLField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
