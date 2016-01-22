#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for good HTML."""

from django.core.urlresolvers import reverse
from django.test import TestCase


class BasicHtmlTests(TestCase):
    """Needed HTML properties."""

    def test_doctype(self):
        """Title page must have a DOCTYPE declaration."""
        response = self.client.get(reverse('home'))
        self.assertRegex(response.content, rb'^<!DOCTYPE html>')

    def test_utf8(self):
        """Title page must contain a charset declaration for UTF8."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<meta charset="utf-8">')

    def test_viewpoint(self):
        """Title page must contain a viewport declaration."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<meta name="viewport" content="')

    def test_uses_index_template(self):
        """Test whether the home function uses the index.html."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "grpalloc/index.html")

    def test_uses_base_template(self):
        """Test whether the home function uses also the base.html."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")
