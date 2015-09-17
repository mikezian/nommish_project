#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Button, Submit, Field, HTML, Div
from crispy_forms.bootstrap import InlineCheckboxes, FieldWithButtons, StrictButton

from .models import Profile, UserCollection, RecipesCollection, Recipe

def choice_tuple(collections):
    return tuple((c.id, c.name.upper()) for c in collections)

class SignupForm(forms.Form):
        first_name = forms.CharField(
            max_length=400,
            label='First Name',
            widget=forms.TextInput(attrs={'placeholder': 'First Name'})
        )
        last_name = forms.CharField(
            max_length=400,
            label='Last Name',
            widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
        )

        def signup(self, request, user):
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            profile = Profile(user=user, first_name=user.first_name, last_name=user.last_name)
            profile.save()

        class Meta:
            model = get_user_model()

class SearchKeywordForm(forms.Form):
    keyword = forms.CharField(
        max_length=200,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Looking for recipes?'})
    )

    def __init__(self, *args, **kwargs):
        super(SearchKeywordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = reverse('recipe-search')

        self.helper.disable_csrf = True
        self.fields['keyword'].value = kwargs.get('keyword')
        self.helper.form_class = 'navbar-form'
        self.helper.layout = Layout(
            HTML(
                '<div class="input-group-sm">'
            ),
            FieldWithButtons(
                Field('keyword', css_class='input-sm form-control'),
                HTML("""
                    <button type="submit" class="btn btn-sm btn-info"><span class="glyphicon glyphicon-search"></span></button>
                """),
            ),
            HTML('</div>'),
        )
        # self.helper.layout = Layout(
        #     FieldWithButtons(
        #         Field('keyword', css_class='input-large'),
        #         HTML("""
        #             <button type="submit" class="btn btn-info"><span class="glyphicon glyphicon-search"></span></button>
        #         """),
        #     ),
        # )

class UserRecipeCollectionForm(forms.Form):
    # recipes = forms.ModelChoiceField(queryset=Recipe.objects.all().values('id'), widget=forms.HiddenInput())
    recipecollection = forms.MultipleChoiceField(
        choices=(),
        label=(u''),
        widget=forms.CheckboxSelectMultiple(),
    )
    name = forms.CharField(
        label=(u''),
        required = False,
    )

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.get('initial').get('user')
        super(UserRecipeCollectionForm, self).__init__(*args, **kwargs)
        self.fields['recipecollection'].choices = choice_tuple(kwargs.get('initial').get('recipe_collection'))
        self.fields['recipecollection'].initial = kwargs.get('initial').get('user_recipe_collection')

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        FieldWithButtons(
                            Field('name', css_class='input-large', title='Collection Name', placeholder='My Collection'),
                            StrictButton("Add", css_class='btn-add'),
                        ),
                        css_class="col-md-12",
                    ),
                    css_class="row"
                ),
                Div(
                    Div(
                        HTML("""
                            <h5>My Recipe Collection</h5>
                        """),
                        css_class="col-md-12 modal-subheader",
                    ),
                    css_class="row"

                ),
                Div(
                    Div(
                        Field('recipecollection', css_class='faChkRnd'),
                        css_class="col-md-12 collection-checkbox",
                    ),
                    css_class="row",
                )
            )
        )

class AddUserCollectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddUserCollectionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field(
                'name',
                css_class='input-large',
                title='Collection Name'
            ),
            ButtonHolder(
                Submit('save', 'Save', css_class='btn-info')
            ),
        )

    class Meta:
        model = UserCollection
        fields = ('name',)
