#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Transaction-related models.
"""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from opencivicdata.core.models.base import (
    IdentifierBase,
    LinkBase,
    OCDBase,
    OCDIDField
)
from opencivicdata.core.models import Organization, Person
from opencivicdata.elections.models import Election
from .committees import Committee
from .filings import FilingAction


@python_2_unicode_compatible
class Transaction(OCDBase):
    """
    A contribution, expenditure, loan or other two-party transfer reported on a Filing.
    """
    id = OCDIDField(ocd_type='campaign-finance-filing-transaction')
    filing_action = models.ForeignKey(
        FilingAction,
        related_name='transactions',
        on_delete=models.CASCADE,
        help_text='Reference to the FilingAction in which the Transaction is '
                  'reported.',
    )
    classification = models.CharField(
        max_length=100,
        help_text='Type of transaction - contribution, expenditure, loan, '
                  'transfer, other receipt, etc.',
    )
    amount_value = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        help_text='Decimal amount of transaction.',
    )
    amount_currency = models.CharField(
        max_length=3,
        help_text='Currency denomination of transaction.',
    )
    is_in_kind = models.BooleanField(
        default=False,
        help_text='Indicates this is an in-kind (i.e., non-monetary) Transaction.',
    )
    election = models.ForeignKey(
        Election,
        related_name='transactions',
        null=True,
        help_text='Reference to the Election to which the transaction is designated.',
    )
    ENTITY_TYPES = (
        ("committee", "Committee"),
        ("organization", "Organization"),
        ("person", "Person"),
    )
    sender_entity_type = models.CharField(
        max_length=50,
        choices=ENTITY_TYPES,
        help_text='Type of entity of sender (e.g., "Person", "Organization", '
                  '"Committee").',
    )
    sender_committee = models.ForeignKey(
        Committee,
        related_name='transactions_sent',
        on_delete=models.PROTECT,
        null=True,
        help_text='Reference to Committee that sent the transaction, if '
                  'sender_entity_type is "Committee".',
    )
    sender_organization = models.ForeignKey(
        Organization,
        related_name='transactions_sent',
        on_delete=models.PROTECT,
        null=True,
        help_text='Reference to Organization that sent the transaction, if '
                  'sender_entity_type is "Organization".',
    )
    sender_person = models.ForeignKey(
        Person,
        related_name='transactions_sent',
        on_delete=models.PROTECT,
        null=True,
        help_text='Reference to Person that sent the transaction, if '
                  'sender_entity_type is "Person".',
    )
    recipient_entity_type = models.CharField(
        max_length=50,
        choices=ENTITY_TYPES,
        help_text='Type of entity of recipient (e.g., "Person", "Organization", '
                  '"Committee").',
    )
    recipient_committee = models.ForeignKey(
        Committee,
        related_name='transactions_received',
        on_delete=models.PROTECT,
        null=True,
        help_text='Reference to Committee that received the transaction, if '
                  'recipient_entity_type is "Committee".',
    )
    recipient_organization = models.ForeignKey(
        Organization,
        related_name='transactions_received',
        on_delete=models.PROTECT,
        null=True,
        help_text='Reference to Organization that received the transaction, if '
                  'recipient_entity_type is "Organization".',
    )
    recipient_person = models.ForeignKey(
        Person,
        related_name='transactions_received',
        on_delete=models.PROTECT,
        null=True,
        help_text='Reference to Person that sent the transaction, if '
                  'recipient_entity_type is "Person".',
    )
    date = models.DateField(
        null=True,
        help_text='Date reported for transaction.',
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_transaction'

    def __str__(self):
        return '{0.amount_value} {0.classification} on {0.date}'.format(self)


@python_2_unicode_compatible
class TransactionIdentifier(IdentifierBase):
    """
    Upstream identifiers of a Transaction.
    """
    transaction = models.ForeignKey(
        Transaction,
        related_name='identifiers',
        on_delete=models.CASCADE,
        help_text="Reference to the Transaction identified by this alternative identifier.",
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_transactionidentifier'

    def __str__(self):
        tmpl = '%s identifies %s'
        return tmpl % (self.identifier, self.transaction)


@python_2_unicode_compatible
class TransactionNote(models.Model):
    """
    A note describing a Transaction.
    """
    transaction = models.ForeignKey(
        Transaction,
        related_name='notes',
        help_text='Reference to a Transaction described by the note.',
    )
    note = models.TextField(
        help_text='Text of the note.',
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_transactionnote'

    def __str__(self):
        tmpl = '%s (%s)'
        return tmpl % (self.note, self.transaction)


class TransactionSource(LinkBase):
    """
    Source used in assembling a Transaction.
    """
    transaction = models.ForeignKey(
        Transaction,
        related_name='sources',
        help_text="Reference to the Transaction this source verifies.",
        on_delete=models.CASCADE,
    )

    class Meta:
        """
        Model options.
        """
        db_table = 'opencivicdata_transactionsource'
