#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
# from django.contrib import admin

from .views import JointLoginSignupView

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^(?P<filename>(robots.txt)|(humans.txt))$', home_files, name='home-files'),

    # recipe views
    url(r'', include('recipe.urls')),

    # all-auth views

    # url(r'^accounts/login/$', JointLoginSignupView.as_view()),
    # url(r'^accounts/signup/$', JointLoginSignupView.as_view()),
    url(r'^accounts/', include('allauth.urls')),
]
