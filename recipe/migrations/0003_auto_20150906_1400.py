# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_recipe_source_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cover',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cuisine',
            name='cover',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='holiday',
            name='cover',
            field=models.TextField(null=True),
        ),
    ]
