#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
# from django.contrib import admin

from .views import *

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^(?P<filename>(robots.txt)|(humans.txt))$', home_files, name='home-files'),
    # recipe views
    url(r'^$', RecipeListView.as_view(), name='recipes'),

    url(r'^courses/$', CourseListView.as_view(), name='courses'),
    url(r'^cuisines/$', CuisineListView.as_view(), name='cuisines'),
    url(r'^sources/$', SourceListView.as_view(), name='sources'),

    url(r'^recipe/course/(?P<slug>.+?)/$', RecipeCourseListView.as_view(), name='course-list'),
    url(r'^recipe/cuisine/(?P<slug>.+?)/$', RecipeCuisineListView.as_view(), name='cuisine-list'),
    url(r'^recipe/source/(?P<slug>.+?)/$', RecipeSourceListView.as_view(), name='recipe-source-list'),

    url(r'^recipe/(?P<slug>.+?)/redirect/$', RecipeSourceRedirectView.as_view(), name='recipe-source-redirect'),
    url(r'^recipe/(?P<slug>.+?)/$', RecipeDetailView.as_view(), name='recipe-detail'),

    url(r'^collections/(?P<slug>.+?)/$', RecipeCollectionListView.as_view(), name='recipe-collection-list'),
    url(r'^my-collection/$', UserRecipeCollectionListView.as_view(), name='user-recipe-collection'),


    url(r'^search/$', SearchListView.as_view(), name='recipe-search'),


    url(r'^api/collections/', UserCollectionList.as_view(), name='api-collection-list'),
    url(r'^api/recipe-collections/delete/(?P<pk>[0-9]+)/$', RecipesCollectionDelete.as_view(), name='api-recipe-collection-list-delete'),
    url(r'^api/recipe-collections/', RecipesCollectionList.as_view(), name='api-recipe-collection-list'),

]
