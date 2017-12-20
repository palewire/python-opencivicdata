#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Committee-related models
"""
from django.contrib import admin
from opencivicdata.core.admin import base
from .. import models


@admin.register(models.CommitteeType)
class CommitteeTypeAdmin(base.ModelAdmin):
    """
    Custom administrative panel for the CommitteeType model.
    """
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'jurisdiction',
        'extras'
    )
    list_display = (
        "name",
        "jurisdiction",
    )
    fields = ("name",) + readonly_fields
    search_fields = ("name",)
    list_filter = (
        'jurisdiction__name',
    )
