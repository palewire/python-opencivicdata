#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Committee-related models.
"""
from django.contrib import admin
from opencivicdata.core.admin import base
from .. import models


class FilingIdentifierInline(base.IdentifierInline):
    """
    Custom inline administrative panely for FilingIdentifier model.
    """
    model = models.FilingIdentifier


class FilingSourceInline(base.ReadOnlyTabularInline):
    """
    Custom inline administrative panely for FilingSource model.
    """
    readonly_fields = ("url", "note")
    model = models.FilingSource


@admin.register(models.Filing)
class FilingAdmin(base.ModelAdmin):
    """
    Custom administrative panel for the Filing model.
    """
    readonly_fields = (
        "id",
        "filer",
        "classification",
        "recipient",
        "coverage_start_date",
        "coverage_end_date",
        "extras",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "filer",
        "classification",
        "coverage_start_date",
        "coverage_end_date",
    )
    fields = readonly_fields
    search_fields = ("filer__name",)
    list_filter = ("filer__name",)
    date_hierarchy = "coverage_start_date"
    inlines = (
        FilingIdentifierInline,
        FilingSourceInline
    )
