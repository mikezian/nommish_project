#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast

import logging
from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import View, ListView, DetailView

from braces.views import PrefetchRelatedMixin, LoginRequiredMixin


from .models import Recipe, Course, Cuisine, UserCollection, RecipesCollection
from .forms import UserRecipeCollectionForm, SearchKeywordForm
# Create your views here.

logger = logging.getLogger(__name__)


from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

# Q - shortcut for Query
# A - shortcut for Aggregation

from recipe.models import *
from recipe.search_indexes import *


es = Elasticsearch([
    {'host': 'localhost', 'port': 9200},
])

class RecipeView(View):
    pass


class SearchListView(ListView):
    template_name = "recipe_list.html"
    paginate_by = 20
    context_object_name = 'recipe_objects'

    def get_page_title(self, **kwargs):
        count = kwargs.get('context').get('paginator').count
        if count:
            return '%s recipes found' % count
        return 'No recipes found'

    def get_queryset(self):
        try:
            keyword = self.request.GET['keyword']
            s = Search(using=es, index='recipe')
            s.update_from_dict({
                'query': {
                    'match': {
                        'name': {
                            'query': keyword,
                            'type': 'phrase_prefix',
                            'slop': 2
                        }
                    },
                }
            })
            s = s.extra(size=1000)
            results = s.execute()
            return results
        except MultiValueDictKeyError:
            pass

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        try:
            keyword = self.request.GET.get('keyword')
            if keyword:
                searchform = SearchKeywordForm({'keyword': keyword})
                context['searchform'] = searchform if searchform.is_valid() else SearchKeywordForm()
            else:
                context['searchform'] = SearchKeywordForm()
        except MultiValueDictKeyError:
            context['searchform'] = SearchKeywordForm()
        kwargs['context'] = context
        context['title'] = self.get_page_title(**kwargs)

        return context


class CollectionListingsView(ListView):
    template_name = "recipe_list.html"
    context_object_name = 'recipe_objects'
    queryset = Recipe.objects.published_recipes().latest()
    paginate_by = 20

    def get_page_title(self, **kwargs):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super(CollectionListingsView, self).get_context_data(**kwargs)
        kwargs['context'] = context
        context['title'] = self.get_page_title(**kwargs)
        context['searchform'] = SearchKeywordForm()
        return context

class RecipeListView(CollectionListingsView, ListView):

    def get_page_title(self, **kwargs):
        return 'Recently added recipes'

    def get_queryset(self):
        qs = super(RecipeListView, self).get_queryset()
        qs = qs.only(
            'courses__name',
            'source_url',
            'source_text',
            'id',
            'name',
            'preparation_time',
            'url',
            'large_image',
            'slug',
            'source_slug',
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super(CollectionListingsView, self).get_context_data(**kwargs)
        kwargs['context'] = context
        context['title'] = self.get_page_title(**kwargs)
        context['total_recipe'] = context.get('paginator').count
        context['main_searchform'] = SearchKeywordForm()
        return context

class RecipeSourceListView(CollectionListingsView, ListView):
    allow_empty = False

    def get(self, request, *args, **kwargs):
        try:
            return super(RecipeSourceListView, self).get(request, *args, **kwargs)
        except Http404:
            # change this to 404
            logger.error('[unknown source to 404]')
            return HttpResponseRedirect(reverse('recipe'))

    def get_queryset(self):
        qs = super(RecipeSourceListView, self).get_queryset()
        qs = qs.filter(source_slug=self.kwargs['slug'])
        if not qs:
            logger.error('[Unknown Source] [%s]' % str(qs.query))
        return qs

    def get_page_title(self, **kwargs):
        return 'Collection from %s' % self.kwargs['slug'].replace('-', ' ').title()

class RecipeCourseListView(CollectionListingsView, ListView):

    def get_queryset(self):
        qs = super(RecipeCourseListView, self).get_queryset()
        qs = qs.filter(courses__slug=self.kwargs['slug'])
        return qs

    def get_page_title(self, **kwargs):
        return '%s Recipes' % self.kwargs['slug'].replace('-', ' ').title()

class RecipeCuisineListView(CollectionListingsView, ListView):

    def get_queryset(self):
        qs = super(RecipeCuisineListView, self).get_queryset()
        qs = qs.filter(cuisines__slug=self.kwargs['slug'])
        return qs

    def get_page_title(self, **kwargs):
        return '%s Recipes' % self.kwargs['slug'].replace('-', ' ').title()


class CollectionView(ListView):
    context_object_name = 'collections'
    template_name = "collection_list.html"

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        context['title'] = self.title
        _collections = []
        for collection in context['collections']:
            collection = {
                'name': collection.get('name'),
                'cover': collection.get('cover'),
                'count': collection.get('count'),
                'url': reverse(self.reverse_url, kwargs={'slug': collection.get('slug')})
            }
            _collections.append(collection)

        context['collections'] = _collections
        return context

class UserRecipeCollectionListView(LoginRequiredMixin, CollectionView, ListView):
    model = UserCollection
    title = 'My Collection'
    reverse_url = 'recipe-collection-list'

    def get_queryset(self):
        if hasattr(self.request, 'user') and self.request.user.is_authenticated():
            current_user = self.request.user
        else:
            current_user = None
        qs = self.model.user_collection_count(user=current_user)
        return qs

class CourseListView(CollectionView, ListView):
    queryset = Course.objects.values('name', 'slug', 'cover').annotate(count=Count('courses'))
    title = 'Recipe by Course'
    reverse_url = 'course-list'

class CuisineListView(CollectionView, ListView):
    queryset = Cuisine.objects.values('name', 'slug', 'cover').annotate(count=Count('cuisines'))
    title = 'Recipe by Cuisine'
    reverse_url = 'cuisine-list'

class SourceListView(CollectionView, ListView):
    queryset = Recipe.objects.extra(select={'name': 'source_text', 'slug': 'source_slug'})\
        .values('name', 'slug')\
        .annotate(count=Count('slug'))
    title = 'Recipe by Source'
    reverse_url = 'recipe-source-list'
    paginate_by = 20


class RecipeCollectionListView(ListView):
    model = RecipesCollection
    title = '%s Recipes'
    template_name = "recipe_list.html"
    context_object_name = 'recipe_objects'

    def get_queryset(self):
        qs = self.model.objects\
            .select_related('recipe', 'collection')\
            .filter(collection__slug=self.kwargs.get("slug"))\
            .only(
                'collection__name',
                'recipe__source_url',
                'recipe__source_text',
                'recipe__id',
                'recipe__name',
                'recipe__preparation_time',
                'recipe__url',
                'recipe__large_image',
                'recipe__courses',
                'recipe__slug',
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super(RecipeCollectionListView, self).get_context_data(**kwargs)
        context['title'] = context['recipe_objects'][0].collection.name
        context['recipe_objects'] = [recipe.recipe for recipe in context['recipe_objects']]
        return context


class RecipeDetailView(PrefetchRelatedMixin, DetailView):
    model = Recipe
    prefetch_related = ["courses"]
    template_name = "recipe_detail.html"
    context_object_name = 'recipe'

    def get_queryset(self):
        return Recipe.objects.prefetch_related('courses', 'holidays')\
            .filter(slug=self.kwargs.get("slug"))\
            .only(
                'courses',
                'holidays',
                'name',
                'slug',
                'large_image',
                'attribution_url',
                'ingredients',
                'preparation_time',
                'source_text',
                'url',
                'servings'
        )

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        recipe = self.get_queryset().all()[0]
        # increment count
        if not self.request.session.get('recipe_viewed_%s' % recipe.pk, None):
            recipe.increment_views()
            self.request.session['recipe_viewed_%s' % recipe.pk] = 1
        logger.error('recipe views %s', recipe.views)
        logger.error('recipe session %s', self.request.session.keys())
        course_info = recipe.courses.all()
        holiday_info = recipe.holidays.all()


        context['title'] = context['recipe'].name

        s = Search(using=es, index='recipe')

        exclude_clause = []
        match_clause = []

        exclude_clause.append(
            {"term": {"document_id": recipe.id}}
        )
        if course_info:
            course_id = course_info[0].id
            match_clause.append({'match': {'courses': {'query': course_id, 'boost': 5}}})
        if holiday_info:
            holiday_id = holiday_info[0].id
            match_clause.append({'match': {'holidays': holiday_id}})

        match_clause.append({'match': {'name': {'query': recipe.name, 'boost': 2}}})

        s = Search(using=es, index='recipe')
        s.update_from_dict({
            'query': {
                'function_score': {
                    'query': {
                        'bool': {
                            "must_not": exclude_clause,
                            'should': match_clause
                        }
                    },
                    'random_score': {
                        'seed': 12371203
                    }
                }
            }
        })

        s = s.extra(size=6)
        results = s.execute()
        context['suggested_recipes'] = results

        if self.request.user.is_authenticated():
            user_collection = UserCollection.objects.filter(user=self.request.user)
            recipe_collection = RecipesCollection.objects\
                .filter(recipe_id=context['recipe'].id, collection__user=self.request.user)\
                .only('collection__id')
            user_recipe_collection = set(i.collection_id for i in recipe_collection.all())
            initial = {
                'recipes': self.kwargs.get("pk"),
                'recipe_collection': user_collection,
                'user_recipe_collection': user_recipe_collection
            }
            context['form'] = UserRecipeCollectionForm(
                initial=initial
            )
        context['searchform'] = SearchKeywordForm()
        context['current_recipe_name'] = recipe.name
        return context

class RecipeSourceRedirectView(RecipeDetailView):

    def dispatch(self, request, *args, **kwargs):
        recipe = self.get_queryset().all()
        print recipe[0].source_url
        url_info = urlparse(recipe[0].source_url)
        print url_info
        return HttpResponseRedirect('http://%s%s' % (url_info.netloc, url_info.path))


############ API ####################

from rest_framework import permissions, status
from rest_framework.generics import (ListCreateAPIView, DestroyAPIView)
from rest_framework.response import Response


from .serializers import UserCollectionSerializer, RecipesCollectionSerializer
from .permissions import IsOwnerOrReadOnly
class UserCollectionMixin(object):
    serializer_class = UserCollectionSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )

    def get_queryset(self):
        return UserCollection.objects.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        # raise Http404 if not user.is_authenticated()
        recipe = ''
        if self.request.data.get('recipe', None):
            recipe = self.request.data['recipe']
        serializer.save(user=self.request.user, recipe=recipe)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserCollectionList(UserCollectionMixin, ListCreateAPIView):
    """
    List user collections or create a new collection
    """
    pass

class RecipesCollectionMixin(object):
    serializer_class = RecipesCollectionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return RecipesCollection.objects\
            .prefetch_related('collection', 'recipe')\
            .filter(collection__user=self.request.user)\
            .only('collection__id', 'recipe__id', 'recipe__name').all()[:5]

    def perform_create(self, serializer):
        # raise Http404 if not user.is_authenticated()
        serializer.save(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # raise Http404 if not user.is_authenticated()
        self.serializer_class.delete({
            'recipe': request.data.get('recipe'),
            'collection': request.data.get('collection'),
            'user': request.user

        })
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipesCollectionList(RecipesCollectionMixin, ListCreateAPIView):
    """
    List user recipe collections or add recipe to user collection
    """
    pass

class RecipesCollectionDelete(RecipesCollectionMixin, DestroyAPIView):
    """
    List user recipe collections or add recipe to user collection
    """
    pass
