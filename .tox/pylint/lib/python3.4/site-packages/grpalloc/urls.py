#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""grpalloc URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from datetime import timedelta
from django.conf.urls import include, url
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth import views as auth_views
from django_q.tasks import Task
from .core import views

admin.autodiscover()

# execute only on system / server start

TASK_ID = Task.get_task_group('delete_expired_events')
# check whether there is already a task named 'delete_expired_events' running
if not TASK_ID:
    # if not, create one
    views.events_expired_schedule()
else:
    # get the last executed task
    LAST_EXECUTED_TASK = TASK_ID[0]
    # get the time when he was executed
    TASK_STARTED = LAST_EXECUTED_TASK.started
    if TASK_STARTED < (timezone.now() - timedelta(days=2)):
        # if the task hasn't been executed for 2 days make a new one
        views.events_expired_schedule()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^questionnaire_instructions/$', views.questionnaire_instructions,
        name='questionnaire_instructions'),
    url(r'^questionnaire_parts/(?P<part>[-\w]+)/$',
        views.questionnaire_parts, name='questionnaire_parts'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^groups_list/$', views.groups_list, name='groups_list'),
    url(r'^groups_temporarily/(?P<eventname>[-\w]+)/$',
        views.groups_temporarily, name='groups_temporarily'),
    url(r'^groups_save/(?P<results>[^/]+)/(?P<eventname>[-\w]+)/$',
        views.groups_save, name='groups_save'),
    url(r'^event_close/(?P<eventname>[-\w]+)/$', views.event_close,
        name='event_close'),
    url(r'^event_reopen/(?P<eventname>[-\w]+)/$', views.event_reopen,
        name='event_reopen'),
    url(r'^event_new/$',
        views.event_new, name='event_new'),
    url(r'^event_new/(?P<edit>[-\w]+)/$',
        views.event_new, name='event_new'),
    url(r'^event_public/(?P<eventname>[-\w]+)/$',
        views.event_public, name='event_public'),
    url(r'^event_delete/(?P<eventname>[-\w]+)/$',
        views.event_delete, name='event_delete'),
    url(r'^event_public_list/$',
        views.event_public_list, name='event_public_list'),
    url(r'^event_entered/$',
        views.event_entered, name='event_entered'),
    url(r'^event_public_member_enters/(?P<eventname>[-\w]+)/$',
        views.event_public_member_enters, name='event_public_member_enters'),
    url(r'^event_member_leave/(?P<eventname>[-\w]+)/$',
        views.event_member_leave, name='event_member_leave'),
    url(r'^event_creator_kicks_member/(?P<member>[-\w]+)/ \
        (?P<eventname>[-\w]+)/$',
        views.event_creator_kicks_member, name='event_creator_kicks_member'),
    url(r'^login_page/$', views.login_page, name='login_page'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'grpalloc/login.html'}),
    url(r'^logout/$', views.logout_page, name='logout'),
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        views.home_files, name='home-files'),
]
