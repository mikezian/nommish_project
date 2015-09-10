#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on https://godjango.com/43-permissions-authentication-django-rest-framework-part-2/

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
