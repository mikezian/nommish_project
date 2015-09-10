# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'1', max_length=50, choices=[(b'1', b'Main Dishes'), (b'2', b'Desserts'), (b'3', b'Side Dishes'), (b'4', b'Lunch and Snacks'), (b'5', b'Appetizers'), (b'6', b'Salads'), (b'7', b'Breads'), (b'8', b'Breakfast and Brunch'), (b'9', b'Soups'), (b'10', b'Beverages'), (b'11', b'Condiments and Sauces'), (b'12', b'Cocktails')])),
                ('slug', models.SlugField(null=True)),
            ],
            options={
                'db_table': 'nommish_course',
            },
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'1', max_length=50, choices=[(b'1', b'American'), (b'2', b'Italian'), (b'3', b'Asian'), (b'4', b'Mexican'), (b'5', b'Southern & Soul Food'), (b'6', b'French'), (b'7', b'Southwestern'), (b'8', b'Barbecue'), (b'9', b'Indian'), (b'10', b'Chinese'), (b'11', b'Cajun & Creole'), (b'12', b'English'), (b'13', b'Mediterranean'), (b'14', b'Greek'), (b'15', b'Spanish'), (b'16', b'German'), (b'17', b'Thai'), (b'18', b'Moroccan'), (b'19', b'Irish'), (b'20', b'Japanese'), (b'21', b'Cuban'), (b'22', b'Hawaiian'), (b'23', b'Swedish'), (b'24', b'Hungarian'), (b'25', b'Portugese')])),
                ('slug', models.SlugField(null=True)),
            ],
            options={
                'db_table': 'nommish_cuisine',
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'1', max_length=50, choices=[(b'1', b'Christmas'), (b'2', b'Summer'), (b'3', b'Thanksgiving'), (b'4', b'New Year'), (b'5', b'Super Bowl / Game Day'), (b'6', b'Halloween'), (b'7', b'Hanukkah'), (b'8', b'4th of July')])),
                ('slug', models.SlugField(null=True)),
            ],
            options={
                'db_table': 'nommish_holiday',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name=b'user')),
                ('first_name', models.CharField(max_length=500, null=True, verbose_name=b'First Name')),
                ('last_name', models.CharField(max_length=500, null=True, verbose_name=b'First Name')),
            ],
            options={
                'ordering': ('user',),
                'db_table': 'nommish_userprofile',
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('recipe_source_id', models.CharField(unique=True, max_length=4000)),
                ('name', models.CharField(max_length=2000)),
                ('ingredients', models.TextField(null=True)),
                ('attribution_text', models.CharField(max_length=2000)),
                ('attribution_url', models.TextField(null=True)),
                ('source_text', models.TextField(null=True)),
                ('source_url', models.TextField(null=True)),
                ('large_image', models.TextField(null=True)),
                ('small_image', models.TextField(null=True)),
                ('url', models.TextField()),
                ('preparation_time', models.IntegerField(default=60)),
                ('likes', models.IntegerField(default=0)),
                ('servings', models.IntegerField(default=1)),
                ('json_response', jsonfield.fields.JSONField(null=True)),
                ('is_indexed', models.NullBooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(null=True)),
                ('courses', models.ManyToManyField(related_name='courses', verbose_name=b'courses', to='recipe.Course')),
                ('cuisines', models.ManyToManyField(related_name='cuisines', verbose_name=b'cuisines', to='recipe.Cuisine')),
                ('holidays', models.ManyToManyField(related_name='holidays', verbose_name=b'holidays', to='recipe.Holiday')),
            ],
            options={
                'db_table': 'nommish_recipe',
            },
        ),
        migrations.CreateModel(
            name='RecipesCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'nommish_recipe_collection',
            },
        ),
        migrations.CreateModel(
            name='UserCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=2000)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(null=True)),
                ('cover', models.TextField(null=True)),
                ('user', models.ForeignKey(related_name='collections', verbose_name=b'collections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nommish_user_collection',
            },
        ),
        migrations.AddField(
            model_name='recipescollection',
            name='collection',
            field=models.ForeignKey(related_name='user_collections', default=None, verbose_name=b'user_collections', to='recipe.UserCollection'),
        ),
        migrations.AddField(
            model_name='recipescollection',
            name='recipe',
            field=models.ForeignKey(related_name='recipes', verbose_name=b'recipes', to='recipe.Recipe'),
        ),
        migrations.AlterUniqueTogether(
            name='recipescollection',
            unique_together=set([('collection', 'recipe')]),
        ),
    ]
