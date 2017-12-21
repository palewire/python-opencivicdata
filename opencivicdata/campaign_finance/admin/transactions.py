#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Transaction-related models.
"""
from django.contrib import admin
from opencivicdata.core.admin import base
from .. import models


class TransactionIdentifierInline(base.IdentifierInline):
    """
    Custom inline administrative panely for TransactionIdentifier model.
    """
    model = models.TransactionIdentifier


class TransactionSourceInline(base.ReadOnlyTabularInline):
    """
    Custom inline administrative panely for TransactionSource model.
    """
    readonly_fields = ("url", "note")
    model = models.TransactionSource


class TransactionNoteInline(base.ReadOnlyTabularInline):
    """
    Custom inline administrative panely for FilingAction model.
    """
    readonly_fields = ("note",)
    model = models.TransactionNote


@admin.register(models.Transaction)
class TransactionAdmin(base.ModelAdmin):
    """
    Custom administrative panel for the Transaction model.
    """
    def get_filer_name(self, obj):
        return truncatechars(obj.filing_action.filer.name, 40)
    get_filer_name.short_description = 'Filer'

    readonly_fields = (
        "id",
        "filing_action",
        "classification",
        "date",
        "amount_value",
        "amount_currency",
        "is_in_kind",
        "election",
        "sender_entity_type",
        "sender_committee",
        "sender_organization",
        "sender_person",
        "recipient_entity_type",
        "recipient_committee",
        "recipient_organization",
        "recipient_person",
        "extras",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "get_filer_name",
        "classification",
        "date",
        "amount_value",
    )
    fields = readonly_fields
    search_fields = ("filingaction__filer__name",)
    list_filter = ("classification",)
    date_hierarchy = "date"
    inlines = (
        TransactionIdentifierInline,
        TransactionNoteInline,
        TransactionSourceInline
    )
