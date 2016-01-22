#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django Models.

A model is the single, definitive source of information about your data.
It contains the essential fields and behaviors of the data you’re storing.
Generally, each model maps to a single database table.
https://docs.djangoproject.com/es/1.9/topics/db/models/
"""
from datetime import date, datetime, timedelta
from django.db import models
from django.contrib.auth.models import User


POINTS = (
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
    (8, "8"),
    (9, "9"),
    (10, "10"),
)


class Questionnaire(models.Model):
    """Model for points and more of the questionnaire."""

    usr = models.ForeignKey(User)

    # p = part; q = question; f = finished

    # Part 1
    p1q1 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p1q2 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p1q3 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p1q4 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p1q5 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p1q6 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p1q7 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p1q8 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p1f = models.IntegerField(default=0)

    # Part 2
    p2q1 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p2q2 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p2q3 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p2q4 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p2q5 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p2q6 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p2q7 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p2q8 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p2f = models.IntegerField(default=0)

    # Part 3
    p3q1 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p3q2 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p3q3 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p3q4 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p3q5 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p3q6 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p3q7 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p3q8 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p3f = models.IntegerField(default=0)

    # Part 4
    p4q1 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p4q2 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p4q3 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p4q4 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p4q5 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p4q6 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p4q7 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p4q8 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p4f = models.IntegerField(default=0)

    # Part 5
    p5q1 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p5q2 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p5q3 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p5q4 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p5q5 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p5q6 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p5q7 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p5q8 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p5f = models.IntegerField(default=0)

    # Part 6
    p6q1 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p6q2 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p6q3 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p6q4 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p6q5 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p6q6 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p6q7 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p6q8 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p6f = models.IntegerField(default=0)

    # Part 7
    p7q1 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p7q2 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p7q3 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p7q4 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p7q5 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p7q6 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p7q7 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p7q8 = models.CharField(choices=POINTS,
                            default=0,
                            max_length=2, )
    p7f = models.IntegerField(default=0)

    # All Parts finished

    apf = models.BooleanField(default=False)

    # timestamp

    date_test_finished = models.DateField(default=date.today)

    def __str__(self):
        """Return the user as string."""
        return self.usr


class Event(models.Model):
    """Model for events."""

    event_name = models.SlugField(max_length=24, unique=True, error_messages={
        'max_length': "Veranstaltungskürzel ungültig.\
                      Erlaubte Zeichenanzahl: 24",
        'unique': "Das Veranstaltungskürzel existiert bereits.",
    })

    event_creator = models.CharField(max_length=64, default=None)

    event_public = models.BooleanField(default=False)

    event_public_date = models.DateField(default=date.today)

    event_closed = models.BooleanField(default=False)

    event_calculated = models.BooleanField(default=False)

    expiration_date = models.DateField(
        default=datetime.now() + timedelta(days=360)
    )

    event_changed_date = models.DateField(default=datetime.now)

    event_member = models.ManyToManyField(User, blank=True)

    def __str__(self):
        """Return the event name."""
        return self.event_name


class Group(models.Model):
    """Model for groups."""

    event_name = models.ForeignKey(Event)
    group_name = models.CharField(max_length=64, unique=True)
    user_id = models.ManyToManyField(User)

    def __str__(self):
        """Return the group name."""
        return self.group_name
