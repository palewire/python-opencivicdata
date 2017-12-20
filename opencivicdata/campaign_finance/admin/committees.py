#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Committee-related models.
"""
from django.contrib import admin
from opencivicdata.core.admin import base
from opencivicdata.core.admin.base import ModelAdmin, ReadOnlyTabularInline, IdentifierInline
from .. import models


@admin.register(models.CommitteeType)
class CommitteeTypeAdmin(base.ModelAdmin):
    """
    Custom administrative panel for the CommitteeType model.
    """
    readonly_fields = (
        "name",
        "id",
        "jurisdiction",
        "extras",
        "created_at",
        "updated_at",
    )
    list_display = (
        "name",
        "jurisdiction",
    )
    fields = readonly_fields
    search_fields = ("name",)
    list_filter = ("jurisdiction__name",)


class CommitteeIdentifierInline(base.IdentifierInline):
    """
    Custom inline administrative panely for CommitteeIdentifier model.
    """
    model = models.CommitteeIdentifier


class CommitteeSourceInline(base.LinkInline):
    """
    Custom inline administrative panely for CommitteeSource model.
    """
    readonly_fields = ('url', 'note')
    model = models.CommitteeSource


@admin.register(models.Committee)
class CommitteeAdmin(base.ModelAdmin):
    """
    Custom administrative panel for the Committee model.
    """
    readonly_fields = (
        "name",
        "id",
        "committee_type",
        "image",
        "parent",
        "ballot_measure_options_supported",
        "extras",
        "created_at",
        "updated_at",
    )
    list_display = (
        "name",
        "committee_type"
    )
    fields = readonly_fields
    search_fields = ("name",)
    list_filter = ("committee_type__name",)
    inlines = (
        CommitteeIdentifierInline,
        CommitteeSourceInline
    )
