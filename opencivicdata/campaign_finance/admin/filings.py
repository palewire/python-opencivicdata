#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Committee-related models.
"""
from django.contrib import admin
from opencivicdata.core.admin import base
from django.template.defaultfilters import truncatechars
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


class FilingActionInline(base.ReadOnlyTabularInline):
    """
    Custom inline administrative panely for FilingAction model.
    """
    readonly_fields = ("date", "classification", "is_current",)
    fields = readonly_fields
    model = models.FilingAction


@admin.register(models.Filing)
class FilingAdmin(base.ModelAdmin):
    """
    Custom administrative panel for the Filing model.
    """
    def get_filer_name(self, obj):
        return truncatechars(obj.filer.name, 40)
    get_filer_name.short_description = 'Filer'

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
        "get_filer_name",
        "classification",
        "coverage_start_date",
        "coverage_end_date",
    )
    fields = readonly_fields
    search_fields = ("filer__name",)
    list_filter = ("classification",)
    date_hierarchy = "coverage_start_date"
    inlines = (
        FilingIdentifierInline,
        FilingActionInline,
        FilingSourceInline
    )


@admin.register(models.FilingAction)
class FilingActionAdmin(base.ModelAdmin):
    """
    Custom administrative panel for the FilingAction model.
    """
    def get_filer_name(self, obj):
        return truncatechars(obj.filing.filer.name, 40)
    get_filer_name.short_description = 'Filer'

    readonly_fields = (
        "id",
        "filing",
        "date",
        "classification",
        "description",
        "agent",
        "supersedes_prior_versions",
        "is_current",
        "extras",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "get_filer_name",
        "date",
        "classification",
        "is_current",
    )
    fields = readonly_fields
    search_fields = ("filing__filer__name", "filing__id",)
    list_filter = ("classification", "is_current")
    date_hierarchy = "date"
