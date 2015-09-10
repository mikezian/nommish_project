#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand

from recipe.models import Recipe, Course, Cuisine, Holiday


class Command(BaseCommand):
    args = 'No arguments needed'
    help = 'Command to populate missing slugs'

    def handle(self, *args, **kwargs):
        items = [Course, Cuisine, Holiday, Recipe]
        for item in items:
            records = item.objects.all()
            for record in records:
                if not record.slug:
                    record.save()
                    time.sleep(0.1)
                if getattr(record, 'source_slug', None) and not record.source_slug:
                    record.save()
