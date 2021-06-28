from django.test import TestCase

from .models import Client, TimeEntry


class TimeEntryTestCase(TestCase):
    def setUp(self):
        TimeEntry.objects.create()

    def test_timeentry_exists(self):
        entry = TimeEntry.objects.all()
        self.assertEqual(1, entry.count())

    def test_timeentry_active(self):
        entry = TimeEntry.objects.first()
        self.assertEqual(True, entry.is_active)

    def test_timeentry_not_booked(self):
        entry = TimeEntry.objects.first()
        self.assertEqual(False, entry.booked)
        self.assertEqual(True, entry.is_booked)

    def test_timeentry_booked(self):
        entry, _ = TimeEntry.objects.get_or_create(booked=True)
        self.assertEqual(True, entry.booked)
        self.assertEqual(True, entry.is_booked)

    def test_timeentry_client_not_has_booking_booked(self):
        client, _ = Client.objects.get_or_create(name="NoBookingClient", has_booking=False)
        entry_booked, _ = TimeEntry.objects.get_or_create(client=client, booked=True)
        entry_not_booked, _ = TimeEntry.objects.get_or_create(client=client, booked=False)

        self.assertEqual(True, entry_booked.booked)
        self.assertEqual(True, entry_booked.is_booked)
        self.assertEqual(False, entry_not_booked.booked)
        self.assertEqual(True, entry_not_booked.is_booked)


class ClientTestCase(TestCase):
    def setUp(self):
        Client.objects.create(name="DefaultTestClient")

    def test_client_exists(self):
        client = Client.objects.get(name="DefaultTestClient")
        self.assertIsInstance(client, Client)
        self.assertEqual("DefaultTestClient", client.name)
        self.assertEqual(True, client.has_booking)
