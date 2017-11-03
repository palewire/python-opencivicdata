#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Committee-related models.
"""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.postgres.fields import ArrayField
from opencivicdata.core.models import Jurisdiction
from opencivicdata.core.models.base import (
    IdentifierBase,
    LinkBase,
    OCDBase,
    OCDIDField,
)
from opencivicdata.core.models.people_orgs import OtherNameBase
from opencivicdata.elections.models import (
    BallotMeasureContestOption,
    Candidacy,
)


@python_2_unicode_compatible
class CommitteeType(OCDBase):
    """
    A category defined by the Jurisdiction in which the Committee is regulated.
    """

    id = OCDIDField(ocd_type='campaign-finance-committee-type')
    name = models.CharField(
        max_length=100,
        help_text='Name of the Committee Type.',
    )
    jurisdiction = models.ForeignKey(
        Jurisdiction,
        on_delete=models.PROTECT,
        related_name='campaign_finance_committee_types',
        help_text='Reference to the Jurisdiction which defines the Committee Type.',
    )

    def __str__(self):
        return '{0.name} in {0.jurisdiction}'.format(self)

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_committeetype'


@python_2_unicode_compatible
class Committee(OCDBase):
    """
    An Organization required to submit campaign finance filings.
    """

    id = OCDIDField(ocd_type='campaign-finance-committee')
    name = models.CharField(max_length=300, help_text="The name of the Committee.")
    image = models.URLField(
        blank=True,
        max_length=2000,
        help_text="A URL leading to an image that identifies the Committee visually."
    )
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        # parent can be deleted w/o affecting children
        on_delete=models.SET_NULL,
        help_text="A link to another Committee that serves as this Committee's parent."
    )
    committee_type = models.ForeignKey(
        CommitteeType,
        related_name='committees',
        on_delete=models.PROTECT,
        help_text="Reference to the Committee's type, as defined by its Jurisdiction."
    )
    ballot_measure_options_supported = models.ManyToManyField(
        BallotMeasureContestOption,
        related_name='supporting_committees',
        db_table='opencivicdata_committeeballotmeasureoptionsupported',
        help_text='Ballot Measure Options for which the Committee declared support.',
    )

    def __str__(self):
        return self.name

    # Access all "ancestor" organizations
    def get_parents(self):
        org = self
        while True:
            org = org.parent
            # Django accesses parents lazily, so have to check if one actually exists
            if org:
                yield org
            else:
                break

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_committee'


@python_2_unicode_compatible
class CommitteeStatus(models.Model):
    """
    A Committee's (e.g., "active"), including the time period when applied.
    """

    committee = models.ForeignKey(
        Committee,
        related_name='statuses',
        on_delete=models.CASCADE,
        help_text='Reference to the Committee.'
    )
    classification = ArrayField(
        models.CharField(max_length=100, blank=True),
        help_text='Classification for the status, such as "active" or '
                  '"contesting election".',
    )
    note = models.CharField(
        max_length=300,
        blank=True,
        help_text="Description of the status"
    )
    start_date = models.CharField(
        max_length=10,
        blank=False,
        help_text="First date at which the status applied (inclusive).",
    )
    end_date = models.CharField(
        max_length=10,
        blank=True,
        help_text=" Last date at which the status applied (inclusive). In many "
                  "cases, the current status won’t have a known end_date "
                  "associated with it.",
    )

    def __str__(self):
        tmp = '{0} is {1} ({2}-{3})'.format(
            self.committee, self.classification, self.start_date, self.end_date
        )
        return tmp

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_committeestatus'


@python_2_unicode_compatible
class CommitteeCandidacyDesignation(models.Model):
    """
    A Candidacy for which a Committee declared a position or focused its activity.
    """

    committee = models.ForeignKey(
        Committee,
        related_name='candidacy_designations',
        help_text='Reference to a Committee with the which the Candidacy has a '
                  'designated relationship.',
    )
    candidacy = models.ForeignKey(
        Candidacy,
        related_name='committees',
        help_text='Reference to a Candidacy with the which the Committee has a '
                  'designated relationship.',
    )
    DESIGNATIONS = (
        ("supports", "Supports"),
        ("opposes", "Opposes"),
        ("primary-vehicle-for", "Primary vehicle for"),
        ("surplus-account-for", "Surplus account for"),
        ("independent-expenditure", "Independent Expenditure"),
    )
    designation = models.CharField(
        max_length=10,
        choices=DESIGNATIONS,
        help_text='Describes the relationship betweent the Committee and '
                  'Candidacy.',
    )

    def __str__(self):
        return '{0.committee} {0.designation} {0.candidacy}'.format(self)

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_committeecandidacydesignation'


@python_2_unicode_compatible
class CommitteeIdentifier(IdentifierBase):
    """
    Upstream identifiers of a Committee.
    """

    committee = models.ForeignKey(
        Committee,
        related_name='identifiers',
        on_delete=models.CASCADE,
        help_text="Reference to the Committee identified by this alternative identifier.",
    )

    def __str__(self):
        tmpl = '%s identifies %s'
        return tmpl % (self.identifier, self.committee)

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_committeeidentifier'


class CommitteeName(OtherNameBase):
    """
    Alternate or former name for a Committee.
    """

    committee = models.ForeignKey(
        Committee,
        related_name='other_names',
        on_delete=models.CASCADE,
        help_text="A link to the Committee with this alternative name.",
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_committeename'


class CommitteeSource(LinkBase):
    """
    Source used in assembling a Committee.
    """
    committee = models.ForeignKey(
        Committee,
        related_name='sources',
        on_delete=models.CASCADE,
        help_text="Reference to the Committee this source verifies.",
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_committeesource'
