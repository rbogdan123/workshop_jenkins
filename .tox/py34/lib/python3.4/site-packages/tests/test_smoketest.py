# -*- coding: utf-8 -*-
"""This is just a showcase of a test."""
from django.test import TestCase
from django.contrib.auth.models import User
from grpalloc.core.models import Event
from grpalloc.core.models import Group
from grpalloc.core.models import Questionnaire
import datetime


class EventTestCase(TestCase):
    """Simple TestCase for creating a Events."""

    def setUp(self):
        """Set up. Create a user and a event."""
        User.objects.create(username="normal", email="test@t.t")
        Event.objects.create(event_creator="normal", event_name="pbi")

    def test_event_name(self):
        """Testing Event_Name and Event_Creator."""
        event1 = Event.objects.get(event_creator="normal")
        self.assertEqual(event1.event_creator, "normal")
        self.assertEqual(event1.event_name, "pbi")

    def test_group_name(self):
        """Test the group name."""
        event1 = Event.objects.get(event_creator="normal")
        Group.objects.create(group_name="besteGruppe", event_name=event1)
        group1 = Group.objects.get(group_name="besteGruppe")
        self.assertEqual(group1.group_name, "besteGruppe")
        self.assertEqual(group1.event_name, event1)

    def test_user_edit(self):
        """Add the first and last name and test it."""
        user2 = User.objects.get(username="normal")
        user2.first_name = "Theodor"
        user2.last_name = "Müller"
        self.assertEqual(user2.first_name, "Theodor")
        self.assertEqual(user2.last_name, "Müller")

    def test_questionnaire(self):
        """Create a questionnaire and test some entries."""
        user2 = User.objects.get(username="normal")
        Questionnaire.objects.create(p1q1=10, p2q4=10, p3q5=10, p4q4=10,
                                     p5q4=10, p6q2=10, p7q2=10, p1f=2, p2f=2,
                                     p3f=2, p4f=2, p5f=2, p6f=2, p7f=2,
                                     date_test_finished=datetime.date.today(),
                                     usr=user2,)
        quest1 = Questionnaire.objects.get(usr=user2)
        self.assertEqual(quest1.p4f, 2)
