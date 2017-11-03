#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.apps import AppConfig
import os


class BaseConfig(AppConfig):
    name = 'opencivicdata.campaign_finance'
    verbose_name = 'Open Civic Data - Campaign Finance'
    path = os.path.dirname(__file__)
