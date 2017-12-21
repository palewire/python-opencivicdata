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
    pass
