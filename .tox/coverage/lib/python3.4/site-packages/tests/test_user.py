# -*- coding: utf-8 -*-
"""This is just a showcase of a test."""
from django.test import TestCase
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    """Simple TestCase for creating a user."""

    def setUp(self):
        """Set up a new User."""
        User.objects.create(username="normal", email="test@t.t")

    def test_user_name(self):
        """Check the email of a user."""
        user = User.objects.get(username="normal")
        self.assertEqual(user.email, "test@t.t")
