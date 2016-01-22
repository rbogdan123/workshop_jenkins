#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of all functions for groups."""
import ast
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django_q.tasks import async, result
from django_q.brokers import get_broker
from .. import models
from .ggrp import Person
from . import general


@login_required
def groups_list(request):
    """Show all groups the member is part of."""
    user = request.user

    # Groups that are already calculated
    calculated_groups = {}
    for group_calculated in models.Group.objects.filter(user_id=user):
        group_member = []
        for member in group_calculated.user_id.all():
            group_member.append(member)
        calculated_groups[group_calculated] = general.draw_chart(
            group_member, 'Gruppenverteilung {}'.format(group_calculated), 300)

    context = {
        "active_group": "active",
        "dict_calculated_groups": calculated_groups,
    }

    return render(request, "grpalloc/groups_list.html", context)


def groups_calculate(participants, max_group_size):
    """
    Return the calculated groups.

    Calculate the groups and return two dictionaries.
    One with the group number as key and the user IDs as value and
    the second one with charts and the user names.
    """
    # instantiate an async task
    task_id = async('grpalloc.core.views.main',
                    participants,
                    max_group_size,
                    sync=True,
                    group='calculate_groups',
                    broker=get_broker())

    # wait an unlimited (-1) time for the result of the task
    # the ggrpalloc algorithm itself limits the time
    task_result = result(task_id, -1)

    dict_group = {}
    dict_group_id = {}

    for number, group in enumerate(task_result.groups()):
        list_member = []
        list_member_id = []
        # pylint: disable=protected-access
        for _id in sorted(p._id for p in group):
            usr = User.objects.get(id=_id)  # pylint: disable=no-member
            list_member.append(usr.username)
            list_member_id.append(usr.id)

        dict_group_id[number + 1] = list_member_id
        dict_group[general.draw_chart(
            list_member, 'Gruppenverteilung', 300)] = list_member

    return [dict_group_id, dict_group]


@login_required
def groups_temporarily(request, eventname):
    """Temporarily created groups for the group creator."""
    event = models.Event.objects.get(event_name=eventname)

    if request.method == 'POST' and event.event_closed is True:
        # if the user filters the group name
        if 'calculate' in request.POST:
            try:
                max_group_size = int(request.POST['max_group_size'])
            except ValueError:
                messages.warning(request, "Keine gültige Eingabe")
                return HttpResponseRedirect(reverse("event_new"))

            if max_group_size < 2:
                messages.warning(request, "Kleinste Gruppengröße besteht\
                                          aus mindestens 2 Mitgliedern!")
                return HttpResponseRedirect(reverse("event_new"))

        else:
            raise Http404("Keine gültige Eingabe")

        participants = []

        for member in event.event_member.all():
            results = []
            pnt = models.Questionnaire.objects.get(usr=member)

            # Get calculated points
            results.append(int(pnt.p1q7) + int(pnt.p2q1) + int(pnt.p3q8) +
                           int(pnt.p4q4) + int(pnt.p5q2) + int(pnt.p6q6) +
                           int(pnt.p7q5))
            results.append(int(pnt.p1q4) + int(pnt.p2q2) + int(pnt.p3q1) +
                           int(pnt.p4q8) + int(pnt.p5q6) + int(pnt.p6q3) +
                           int(pnt.p7q7))
            results.append(int(pnt.p1q6) + int(pnt.p2q5) + int(pnt.p3q3) +
                           int(pnt.p4q2) + int(pnt.p5q4) + int(pnt.p6q7) +
                           int(pnt.p7q1))
            results.append(int(pnt.p1q3) + int(pnt.p2q7) + int(pnt.p3q4) +
                           int(pnt.p4q5) + int(pnt.p5q8) + int(pnt.p6q1) +
                           int(pnt.p7q6))
            results.append(int(pnt.p1q1) + int(pnt.p2q3) + int(pnt.p3q6) +
                           int(pnt.p4q7) + int(pnt.p5q5) + int(pnt.p6q8) +
                           int(pnt.p7q4))
            results.append(int(pnt.p1q8) + int(pnt.p2q4) + int(pnt.p3q7) +
                           int(pnt.p4q3) + int(pnt.p5q1) + int(pnt.p6q5) +
                           int(pnt.p7q2))
            results.append(int(pnt.p1q2) + int(pnt.p2q6) + int(pnt.p3q5) +
                           int(pnt.p4q1) + int(pnt.p5q3) + int(pnt.p6q2) +
                           int(pnt.p7q8))
            results.append(int(pnt.p1q5) + int(pnt.p2q8) + int(pnt.p3q2) +
                           int(pnt.p4q6) + int(pnt.p5q7) + int(pnt.p6q4) +
                           int(pnt.p7q3))

            participants.append(
                Person
                (
                    member.id,
                    tuple(results)
                )
            )

        # instantiate an async task
        if len(participants) > 3:

            calculated_groups = groups_calculate(participants, max_group_size)

            context = {
                "active_group": "active",
                "results": calculated_groups[1],
                "results_url": calculated_groups[0],
                "name": eventname,
                "max_group_size": max_group_size,
            }

            return render(request, "grpalloc/groups_temporarily.html", context)

        else:
            messages.warning(request, "Mindestens vier Teilnehmer notwendig")
            return HttpResponseRedirect(reverse("event_new"))

    else:
        messages.warning(request, "Keine gültige Eingabe")
        return HttpResponseRedirect(reverse("event_new"))


@login_required
def groups_save(request, results, eventname):
    """Save groups in the db if the event creator agreed."""
    # changes type from string to dict
    results_dict = ast.literal_eval(results)

    event = models.Event.objects.get(event_name=eventname)

    for group, usr_id in results_dict.items():

        group_name = "{0} - #{1}".format(event, group)

        grp = models.Group.objects.create(
            event_name=event,
            group_name=group_name
        )

        grp.save()

        for member in usr_id:
            grp.user_id.add(member)

    models.Event.objects.filter(
        event_name=eventname).update(event_calculated=True)

    messages.success(request, "Die Gruppen wurden gespeichert.")

    return HttpResponseRedirect(reverse("event_new"))
