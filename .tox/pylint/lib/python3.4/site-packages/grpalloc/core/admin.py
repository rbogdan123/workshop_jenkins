#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The Django admin site.

https://docs.djangoproject.com/en/1.9/ref/contrib/admin/
One of the most powerful parts of Django is the automatic admin interface.
It reads metadata in your model to provide a powerful and production-ready
interface that content producers can immediately use to start adding
content to the site.
"""
from django.contrib import admin
from . import models


class EventAdmin(admin.ModelAdmin):
    """Class to configure Admin view of events."""

    list_display = ('event_name', 'event_creator', 'expiration_date')

    readonly_fields = ('event_public', 'event_public_date',
                       'event_changed_date')


admin.site.register(models.Event, EventAdmin)


class GroupAdmin(admin.ModelAdmin):
    """Class to configure Admin view of groups."""

    readonly_fields = ('event_name', 'user_id')


admin.site.register(models.Group, GroupAdmin)
