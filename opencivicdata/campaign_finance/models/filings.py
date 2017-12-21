#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filing-related models.
"""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.postgres.fields import ArrayField
from opencivicdata.core.models.base import (
    IdentifierBase,
    LinkBase,
    OCDBase,
    OCDIDField
)
from opencivicdata.core.models import Organization, Person
from .committees import Committee


@python_2_unicode_compatible
class Filing(OCDBase):
    """
    A campaign finance document filed by a Committee with a regulator.
    """
    id = OCDIDField(ocd_type='campaign-finance-filing')
    classification = models.CharField(
        max_length=100,
        blank=True,
        help_text='The type of filing, as defined by the jurisdiction in which '
                  'it was filed.',
    )
    coverage_start_date = models.DateField(
        blank=True,
        help_text='Date when filing period of coverage begins.',
    )
    coverage_end_date = models.DateField(
        blank=True,
        help_text='Date when filing period of coverage ends.',
    )
    filer = models.ForeignKey(
        Committee,
        related_name='filings',
        on_delete=models.PROTECT,
        help_text='Reference to the Committee making the Filing.',
    )
    recipient = models.ForeignKey(
        Organization,
        related_name='filings_received',
        on_delete=models.PROTECT,
        help_text='Reference to the Organization that is the regulator to which'
                  ' the filing was submitted.',
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_filing'
        ordering = ("-coverage_start_date",)
        get_latest_by = 'coverage_start_date'

    def __str__(self):
        return '{0.filer} ({0.coverage_start_date} – {0.coverage_end_date})'.format(self)


@python_2_unicode_compatible
class FilingAction(OCDBase):
    """
    An action that takes place on a filing, such as amendments, withdrawals, etc.
    """
    id = OCDIDField(ocd_type='campaign-finance-filing-action')
    filing = models.ForeignKey(
        Filing,
        related_name='actions',
        on_delete=models.CASCADE,
        help_text='Reference to the Filing in which the action was reported.',
    )
    classification = ArrayField(
        models.CharField(max_length=100, blank=True),
        help_text='Classification for the action, such as "amendment" or '
                  '"revocation".',
    )
    description = models.CharField(
        max_length=100,
        help_text='Description of the action.',
    )
    date = models.DateField(
        help_text='The date the action occurred',
    )
    agent = models.ManyToManyField(
        Person,
        related_name='filing_actions',
        db_table='opencivicdata_filingactionagent',
        help_text='Person responsible for the action, usually the filer of the '
                  'amendment or withdrawal.',
    )
    supersedes_prior_versions = models.BooleanField(
        default=False,
        help_text='Indicates whether this action renders everything contained in '
                  'previous versions of this Filing invalid.',
    )
    is_current = models.BooleanField(
        default=True,
        help_text='Indicates whether data from this action (primarily the '
                  'transaction list) should be considered current.',
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_filingaction'
        ordering = ("-date",)
        get_latest_by = "date"

    def __str__(self):
        return '{0.description} ({0.date})'.format(self)


@python_2_unicode_compatible
class FilingActionSummaryAmount(models.Model):
    """
    An amount reported on a Filing, not necessarily calculable by aggregating transactions.
    """
    filing_action = models.ForeignKey(
        FilingAction,
        related_name='summary_amounts',
        help_text='Reference to a FilingAction in which the summary amount was reported.',
    )
    label = models.CharField(
        max_length=100,
        help_text='Description of the total (e.g., "Unitemized contributions" '
                  'or "Total expenditures").',
    )
    amount_value = models.FloatField(
        help_text='Decimal amount of transaction.',
    )
    amount_currency = models.CharField(
        max_length=3,
        help_text='Currency denomination of transaction.',
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_filingactionsummaryamount'
        ordering = ("filing_action", "label",)

    def __str__(self):
        tmpl = '%s (%s)'
        return tmpl % (self.amount_value, self.label)


@python_2_unicode_compatible
class FilingIdentifier(IdentifierBase):
    """
    Upstream identifiers of a Filing.
    """
    filing = models.ForeignKey(
        Filing,
        related_name='identifiers',
        on_delete=models.CASCADE,
        help_text="Reference to the Filing identified by this alternative identifier.",
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_filingidentifier'

    def __str__(self):
        tmpl = '%s identifies %s'
        return tmpl % (self.identifier, self.filing)


class FilingSource(LinkBase):
    """
    Source used in assembling a Filing.
    """
    filing = models.ForeignKey(
        Filing,
        related_name='sources',
        on_delete=models.CASCADE,
        help_text="Reference to the Filing this source verifies.",
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_filingsource'
