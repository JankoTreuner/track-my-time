from django.test import TestCase

from .models import TimeEntry

class TimeEntryTestCase(TestCase):
    def setUp(self):
        TimeEntry.objects.create()

    def test_timeentry_exists(self):
        entry = TimeEntry.objects.all()
        self.assertEqual(1, entry.count())

    def test_timeentry_active(self):
        entry = TimeEntry.objects.first()
        self.assertEqual(True, entry.is_active) 
