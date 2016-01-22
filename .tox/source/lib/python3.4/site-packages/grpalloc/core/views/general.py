#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of all general, non-specific functions."""
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import pygal
from .. import models


def current_user_instance(username):
    """Return the current user as instance."""
    return User.objects.get(username=username)  # pylint: disable=no-member


def home(request):
    """Render index with information about this site."""
    return render(request, "grpalloc/index.html", {})


def change_first_name(request, name, user):
    """Change first name of the current logged in user."""
    if name.isalpha():
        user.first_name = name
    else:
        messages.warning(request,
                         "Kein gültiger Vorname",
                         extra_tags='names')


def change_last_name(request, name, user):
    """Change last name of the current logged in user."""
    if name.isalpha():
        user.last_name = name
    else:
        messages.warning(request,
                         "Kein gültiger Nachname",
                         extra_tags='names')


def search_user(request, search_input):
    """Return Queryset of filtered users."""
    if len(search_input) < 3:
        messages.warning(request,
                         "Bitte mindestens 3 Buchstaben eingeben.",
                         extra_tags='search')
    else:
        return User.objects.filter(  # pylint: disable=no-member
            username__contains=search_input)


@login_required
def profile(request):
    """Profile with a chart of the personality and a search-member field."""
    current_user = request.user
    user = current_user_instance(current_user)
    chart = None
    users = None
    search = None
    date_test_finished = None

    if request.method == 'POST':
        if 'name' in request.POST and request.POST['name'] != "":
            change_last_name(request, request.POST['name'], current_user)
        if 'vname' in request.POST and request.POST['vname'] != "":
            change_first_name(request, request.POST['vname'], current_user)
        if 'email' in request.POST and request.POST['email'] != "":
            current_user.email = request.POST['email']
        current_user.save()
        if 'user_search' in request.POST:
            users = search_user(request, request.POST['user_search'])

    try:
        model = models.Questionnaire.objects.get(usr=user)
        date_test_finished = model.date_test_finished
        # show_chart is True if all parts of the questionnaire are finished
        show_chart = model.apf
        chart = draw_chart([user], None, 500)

    except ObjectDoesNotExist:
        show_chart = False

    args = {
        "show_chart": show_chart,
        "active_home": "active",
        "chart": chart,
        "date_test_finished": date_test_finished,
        "users": users,
        "search": search,
    }

    return render(request, "grpalloc/profile.html", args)


def draw_chart(group_member, title, height):
    """Create / draw a chart with pygal."""
    organisator = 0
    praesident = 0
    macher = 0
    kreative = 0
    aufklaerer = 0
    abwaeger = 0
    mitspieler = 0
    fertigsteller = 0

    for member in group_member:
        user = current_user_instance(member)
        points = models.Questionnaire.objects.get(usr=user)

        # Get calculated points
        organisator += round(10 / 7 * (int(points.p1q7) + int(points.p2q1) +
                                       int(points.p3q8) + int(points.p4q4) +
                                       int(points.p5q2) + int(points.p6q6) +
                                       int(points.p7q5)) / len(group_member),
                             1)
        praesident += round(10 / 7 * (int(points.p1q4) + int(points.p2q2) +
                                      int(points.p3q1) + int(points.p4q8) +
                                      int(points.p5q6) + int(points.p6q3) +
                                      int(points.p7q7)) / len(group_member), 1)
        macher += round(10 / 7 * (int(points.p1q6) + int(points.p2q5) +
                                  int(points.p3q3) + int(points.p4q2) +
                                  int(points.p5q4) + int(points.p6q7) +
                                  int(points.p7q1)) / len(group_member), 1)
        kreative += round(10 / 7 * (int(points.p1q3) + int(points.p2q7) +
                                    int(points.p3q4) + int(points.p4q5) +
                                    int(points.p5q8) + int(points.p6q1) +
                                    int(points.p7q6)) / len(group_member), 1)
        aufklaerer += round(10 / 7 * (int(points.p1q1) + int(points.p2q3) +
                                      int(points.p3q6) + int(points.p4q7) +
                                      int(points.p5q5) + int(points.p6q8) +
                                      int(points.p7q4)) / len(group_member), 1)
        abwaeger += round(10 / 7 * (int(points.p1q8) + int(points.p2q4) +
                                    int(points.p3q7) + int(points.p4q3) +
                                    int(points.p5q1) + int(points.p6q5) +
                                    int(points.p7q2)) / len(group_member), 1)
        mitspieler += round(10 / 7 * (int(points.p1q2) + int(points.p2q6) +
                                      int(points.p3q5) + int(points.p4q1) +
                                      int(points.p5q3) + int(points.p6q2) +
                                      int(points.p7q8)) / len(group_member), 1)
        fertigsteller += round(10 / 7 * (int(points.p1q5) + int(points.p2q8) +
                                         int(points.p3q2) + int(points.p4q6) +
                                         int(points.p5q7) + int(points.p6q4) +
                                         int(points.p7q3)) / len(group_member),
                               1)

    bar_chart = pygal.Bar(
        title=title,
        style=pygal.style.CleanStyle,
        show_legend=False,
        human_readable=True,
        height=height,
    )
    bar_chart.x_labels = 'Organisator', 'Präsident', 'Macher', 'Kreative', \
        'Aufklärer', 'Abwäger', 'Mitläufer', 'Fertigsteller'
    bar_chart.add(
        'Prozent',
        [organisator, praesident, macher, kreative, aufklaerer,
         abwaeger, mitspieler, fertigsteller]
    )
    return bar_chart


def home_files(request, filename):
    """Get files like robots.txt and humans.txt."""
    return render(request, filename, {}, content_type="text/plain")


def login_page(request):
    """User can log in."""
    return render(request, "grpalloc/login.html")


def logout_page(request):
    """User can log out."""
    logout(request)
    messages.info(request, "Sie haben sich erfolgreich ausgeloggt")
    return HttpResponseRedirect(reverse('home'))
