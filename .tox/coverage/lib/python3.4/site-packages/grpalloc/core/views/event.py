#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collection of all functions for events."""
from datetime import date, datetime
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django_q.tasks import schedule
from .. import forms
from .. import models
from . import general


def events_expired():
    """Delete all events that are expired."""
    for event in models.Event.objects.all():
        if event.expiration_date < date.today():
            event.delete()


def events_expired_schedule():
    """Schedule which runs daily and executes events_expired()."""
    schedule('grpalloc.core.views.events_expired',
             name='delete_expired_events',
             schedule_type='D',)


def filter_event(request, myevent, input_filter):
    """Return the filtered list of events."""
    myevent = myevent.filter(
        event_name__contains=input_filter)
    if myevent.count() > 0:
        messages.success(
            request,
            "Einträge erfolgreich nach `{}` "
            "gefiltert".format(input_filter))
    else:
        messages.warning(
            request,
            "Keine Einträge für `{}` "
            "gefunden".format(input_filter))
    return myevent


def create_new_event(request):
    """User can create new events."""
    form_create_event = forms.EventForm(request.POST)
    if form_create_event.is_valid():
        event = form_create_event.save(commit=False)
        event_date = form_create_event.cleaned_data[
            "expiration_date"]
        if event_date < date.today():
            messages.warning(
                request,
                "Datum kann nicht in der Vergangenheit liegen")
        else:
            event.event_creator = request.user
            event.save()
            messages.success(
                request,
                "Die Veranstaltung wurde erfolgreich erstellt")
    return form_create_event


def edit_event(request, edit):
    """User can edit his events as long as they aren't public."""
    try:
        i = models.Event.objects.get(event_name=edit)
    except ObjectDoesNotExist:
        raise Http404('{} nicht gefunden'.format(edit))

    form_edit_event_name = forms.EventNameEditForm(
        request.POST,
        instance=i)

    if form_edit_event_name.is_valid():

        # Check whether event is public; in case user has 2 tabs open
        # and he switches in the first one to publicize it
        # it would be possible to change the name in the second one
        if i.event_public is not True:
            new_eventname = form_edit_event_name.cleaned_data[
                "event_name"]
            new_date = form_edit_event_name.cleaned_data[
                "expiration_date"]
            if new_date < date.today():
                messages.warning(
                    request,
                    "Datum kann nicht in der Vergangenheit liegen")
            else:
                instance = form_edit_event_name.save(commit=False)
                instance.event_name = new_eventname
                instance.expiration_date = new_date
                instance.event_changed_date = datetime.now()
                instance.save()
                messages.success(
                    request, "Name und/oder Datum erfolgreich geändert")

        else:
            messages.warning(
                request, "Name kann nicht (mehr) geändert werden."
                " Entweder ist die Veranstaltung bereits "
                "veröffentlicht oder Sie haben nicht die "
                "entsprechenden Rechte")
    return form_edit_event_name


@login_required
def event_new(request, edit=None):
    """
    Main function for events.

    This renders the template with the list of your created events.
    You can also create a new event, filter for event names and
    update the event name or expiration date.
    """
    user = request.user
    # get all created events from the current user
    myevent = models.Event.objects.filter(event_creator=user)

    groups = {}
    for event in myevent:
        groups[str(event)] = models.Group.objects.filter(event_name=event)

    if request.method == 'POST':
        form_create_event = forms.EventForm()
        form_edit_event_name = forms.EventNameEditForm()

        # if the user creates a new event
        if 'new_event' in request.POST:
            form_create_event = create_new_event(request)

        # if the user updates the event name
        elif 'edit_event' in request.POST:
            form_edit_event_name = edit_event(
                request, edit)
        # update the event list
        myevent = models.Event.objects.filter(event_creator=user)
        # if the user filters the event name
        if 'filter_event' in request.POST:
            myevent = filter_event(
                request, myevent, request.POST['input_filter'])

    else:
        form_create_event = forms.EventForm()
        form_edit_event_name = forms.EventNameEditForm()

    context = {
        'myevent': myevent,
        "form_create_event": form_create_event,
        "form_edit_event_name": form_edit_event_name,
        "active_event": "active",
        "groups": groups,
    }

    return render(request, "grpalloc/my_events.html", context)


@login_required
def event_public(request, eventname):
    """The event gets public for members to enter."""
    event = models.Event.objects.get(event_name=eventname)

    if str(event.event_creator) == str(request.user):
        models.Event.objects.filter(event_name=eventname).update(
            event_public=True,
            event_public_date=date.today()
        )

        messages.success(
            request, "Veranstaltung `{}` öffentlich, "
            "es können nun Teilnehmer beitreten.".format(eventname))

    else:
        messages.warning(
            request, "Nicht genügend Rechte / Nicht Ihre Gruppe")

    return HttpResponseRedirect(reverse("event_new"))


@login_required
def event_close(request, eventname):
    """Set the status of an event to closed."""
    event = models.Event.objects.get(event_name=eventname)

    if str(event.event_creator) == str(request.user):
        models.Event.objects.filter(event_name=eventname).update(
            event_closed=True,
        )

        messages.success(
            request, "Veranstaltung `{}` geschlossen. "
            "Es können keine neuen Teilnehmer beitreten.".format(eventname))

    else:
        messages.warning(
            request, "Nicht genügend Rechte / Nicht Ihre Gruppe")

    return HttpResponseRedirect(reverse("event_new"))


@login_required
def event_reopen(request, eventname):
    """Set the status of an event to open."""
    event = models.Event.objects.get(event_name=eventname)

    if str(event.event_creator) == str(request.user) and  \
            event.event_calculated is False:
        models.Event.objects.filter(event_name=eventname).update(
            event_closed=False,
        )

        messages.success(
            request, "Veranstaltung `{}` wieder geöffnet. "
            "Es können wieder Teilnehmer beitreten.".format(eventname))

    else:
        messages.warning(
            request, "Nicht genügend Rechte / Nicht Ihre Gruppe")

    return HttpResponseRedirect(reverse("event_new"))


@login_required
def event_delete(request, eventname):
    """Delete an event."""
    event = models.Event.objects.get(event_name=eventname)

    if str(event.event_creator) == str(request.user):
        models.Event.objects.filter(event_name=eventname).delete()

        messages.success(
            request, "Veranstaltung `{}` gelöscht.".format(eventname))
    else:
        messages.warning(
            request, "Nicht genügend Rechte / Nicht Ihre Veranstaltung")

    return HttpResponseRedirect(reverse("event_new"))


@login_required
def event_public_list(request):
    """Display all published events in a list."""
    user = request.user
    current_user = general.current_user_instance(user)
    try:
        id_from_entry = models.Questionnaire.objects.get(usr=current_user).id
        entry = models.Questionnaire.objects.get(id=id_from_entry)
        all_parts_finished = entry.apf
    except ObjectDoesNotExist:
        all_parts_finished = False

    events_public = models.Event.objects.filter(
        event_public=True,
        event_closed=False
    )

    if request.method == 'POST':
        # if the user filters the event name
        if 'filter_event' in request.POST:
            input_filter = request.POST['input_filter']
            events_public = models.Event.objects.filter(
                event_public=True,
                event_name__contains=input_filter,
            )

            if len(events_public) > 0:
                messages.success(
                    request,
                    "Einträge erfolgreich nach `{}` "
                    "gefiltert".format(input_filter))
            else:
                messages.warning(
                    request,
                    "Keine Einträge für `{}` "
                    "gefunden".format(input_filter))

    context = {
        "public_events": events_public,
        "active_event": "active",
        "user": user,
        "all_parts_finished": all_parts_finished,
    }

    return render(request, "grpalloc/public_events.html", context)


@login_required
def event_entered(request):
    """Show all events the user is part of."""
    user = request.user

    # events the user is part of
    entered_events = []
    for event_ent in models.Event.objects.filter(
            event_public=True,
            event_closed=False,
            event_member=user,):

        entered_events.append(event_ent)

    # events that are already closed
    closed_events = []
    for event_closed in models.Event.objects.filter(
            event_public=True,
            event_closed=True,
            event_calculated=False,
            event_member=user,):

        closed_events.append(event_closed)

    context = {
        "active_event": "active",
        "list_entered_events": entered_events,
        "list_closed_events": closed_events,
    }

    return render(request, "grpalloc/events_entered.html", context)


@login_required
def event_public_member_enters(request, eventname):
    """Check if all parts of the questionnaire are finished."""
    try:
        i = models.Event.objects.get(event_name=eventname)
        public = i.event_public
        closed = i.event_closed
    except ObjectDoesNotExist:
        raise Http404('{0} nicht gefunden'.format(eventname))

    # get current user
    current_user = request.user
    # get the user object with the id from the current user
    user = general.current_user_instance(current_user)
    try:
        entry = models.Questionnaire.objects.get(usr=user)
        all_parts_finished = entry.apf
    except ObjectDoesNotExist:
        all_parts_finished = False

    # In case of url-manipulation: check whether the user finished all
    # of the questionnaire and whether the event is set to public.
    if all_parts_finished is True and public is True and closed is False:

        # get models object with the passed event name
        event = models.Event.objects.get(event_name=eventname)
        # save it
        event.save()
        # add the user to the manytomany relationship of the event
        event.event_member.add(user)

        messages.success(
            request, "Sie sind der Gruppe {} erfolgreich "
                     "beigetreten".format(eventname))
    else:
        messages.warning(
            request, "Diese Aktion kann nicht ausgeführt werden. "
                     "Bitte kehren Sie zur Startseite zurück.")

    return HttpResponseRedirect(reverse("event_public_list"))


@login_required
def event_member_leave(request, eventname):
    """Member can leave an event he already entered."""
    current_user = request.user
    user = general.current_user_instance(current_user)

    try:
        i = models.Event.objects.get(event_name=eventname)

    except:
        raise Http404('{0} nicht gefunden'.format(eventname))

    i.event_member.remove(user)

    messages.success(
        request, "Erfolgreich aus der Veranstaltung"
        " {} ausgetreten".format(eventname))

    return HttpResponseRedirect(reverse("event_entered"))


@login_required
def event_creator_kicks_member(request, member, eventname):
    """Event creator can remove members from his event."""
    user = general.current_user_instance(member)

    try:
        event = models.Event.objects.get(event_name=eventname)

    except:
        raise Http404('{0} nicht gefunden'.format(eventname))

    if event.event_public is True and event.event_calculated is False:
        event.event_member.remove(user)

        messages.success(
            request, "Sie haben den/die TeilnehmerIn {} erfolgreich aus der "
            "Veranstaltung entfernt".format(member))
    else:
        messages.warning(
            request, "Der/Die TeilnehmerIn {} konnte nicht entfernt "
            "werden".format(member))

    return HttpResponseRedirect(reverse("event_new"))
