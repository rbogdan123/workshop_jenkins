#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
grpalloc forms collection.

This is the file where the django documentation recommends you to
place all your forms code to keep your code easily maintainable.
"""
from django import forms
from django.utils.safestring import mark_safe
from django.forms import ModelForm, TextInput, DateInput
from . import models


ERROR_INVALID = "Es dürfen keine Sonderzeichen und keine Leerzeichen \
    enthalten sein. Maximale Zeichenlänge: 24; Erlaubte Zeichen: a-z A-Z \
    0-9 _ -"
ERROR_REQUIRED = "Bitte geben Sie ein Veranstaltungskürzel ein, das Feld darf \
    nicht leer sein."


# pylint: disable=too-few-public-methods
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """Custom widget for the RadioSelect."""

    def render(self):
        """Render the builtin radiobuttons horizontal."""
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class QuestionnaireForm(forms.Form):
    """Form for the eight radiobuttons from the questionnaire."""

    pointsq1 = forms.ChoiceField(choices=models.POINTS,
                                 initial=0,
                                 widget=forms.RadioSelect(
                                     renderer=HorizontalRadioRenderer),
                                 label="",)

    pointsq2 = forms.ChoiceField(choices=models.POINTS,
                                 initial=0,
                                 widget=forms.RadioSelect(
                                     renderer=HorizontalRadioRenderer),
                                 label="",)

    pointsq3 = forms.ChoiceField(choices=models.POINTS,
                                 initial=0,
                                 widget=forms.RadioSelect(
                                     renderer=HorizontalRadioRenderer),
                                 label="",)

    pointsq4 = forms.ChoiceField(choices=models.POINTS,
                                 initial=0,
                                 widget=forms.RadioSelect(
                                     renderer=HorizontalRadioRenderer),
                                 label="",)

    pointsq5 = forms.ChoiceField(choices=models.POINTS,
                                 initial=0,
                                 widget=forms.RadioSelect(
                                     renderer=HorizontalRadioRenderer),
                                 label="",)

    pointsq6 = forms.ChoiceField(choices=models.POINTS,
                                 initial=0,
                                 widget=forms.RadioSelect(
                                     renderer=HorizontalRadioRenderer),
                                 label="",)

    pointsq7 = forms.ChoiceField(choices=models.POINTS,
                                 initial=0,
                                 widget=forms.RadioSelect(
                                     renderer=HorizontalRadioRenderer),
                                 label="",)

    pointsq8 = forms.ChoiceField(choices=models.POINTS,
                                 initial=0,
                                 widget=forms.RadioSelect(
                                     renderer=HorizontalRadioRenderer),
                                 label="",)


class EventForm(ModelForm):
    """Form for new created events."""

    class Meta:
        """A container with some options (metadata) attached to the model."""

        model = models.Event
        fields = ['event_name', 'expiration_date']
        error_messages = {
            'event_name': {
                'invalid': ERROR_INVALID,
                'required': ERROR_REQUIRED,
            },
        }

    def __init__(self, *args, **kwargs):
        """Initialize fields / widgets."""
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['event_name'].widget = TextInput(attrs={
            'id': "event_name",
            'placeholder': 'Veranstaltungskürzel | Bsp: win-psmu-ws15',
            'class': 'form-control'})
        self.fields['expiration_date'].widget = DateInput(
            attrs={'id': "datepicker",
                   'class': 'form-control'})


class EventNameEditForm(ModelForm):
    """Form for changes / updates of events."""

    class Meta:
        """A container with some options (metadata) attached to the model."""

        model = models.Event
        fields = ['event_name', 'expiration_date']
        error_messages = {
            'event_name': {
                'invalid': ERROR_INVALID,
                'required': ERROR_REQUIRED,

            },
        }

    def __init__(self, *args, **kwargs):
        """Initialize fields / widgets."""
        super(EventNameEditForm, self).__init__(*args, **kwargs)
        self.fields['event_name'].widget = TextInput(attrs={
            'class': 'form-control'})
        self.fields['expiration_date'].widget = DateInput(
            attrs={'class': 'datepicker form-control'})
