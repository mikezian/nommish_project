#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *

class UserCollectionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserCollection
        fields = ('id', 'name', 'user')

    def create(self, validated_data):
        recipe = validated_data.pop('recipe')
        if recipe:
            try:
                recipe = Recipe.objects.get(pk=recipe)
            except ObjectDoesNotExist:
                # don't do anything log it
                recipe = None
            except IntegrityError:
                # don't do anything log it
                recipe = None
        c = UserCollection.objects.create_or_addto_collection(
            collection=validated_data.get('name'),
            recipe=recipe,
            user=validated_data.get('user')
        )
        # todo: increment likes
        return c

class RecipesCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipesCollection
        fields = ('collection', 'recipe')

    def create(self, validated_data):
        try:
            c = UserCollection.objects.create_or_addto_collection(
                collection=validated_data.get('collection'),
                recipe=validated_data.get('recipe'),
                user=validated_data.get('user')
            )
        except ObjectDoesNotExist:
            # don't do anything log it
            pass
        except IntegrityError:
            # don't do anything log it
            pass
        print 'ccc', c
        return c

    @staticmethod
    def delete(data):
        try:
            c = UserCollection.objects.remove_from_collection(
                collection=data.get('collection'),
                recipe=data.get('recipe'),
                user=data.get('user')
            )
            # todo: delete likes
        except ObjectDoesNotExist:
            # don't do anything log it
            pass
        except IntegrityError:
            # don't do anything log it
            pass
        return c
