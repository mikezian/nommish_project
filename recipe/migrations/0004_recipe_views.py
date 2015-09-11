# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20150906_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
