#!/usr/bin/env python
# -*- coding: utf-8 -*-

from allauth.account.views import *
from allauth.account.forms import SignupForm

# http://stackoverflow.com/questions/29499449/django-allauth-login-signup-form-on-homepage
class JointLoginSignupView(LoginView):

    def __init__(self, **kwargs):
        super(JointLoginSignupView, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(JointLoginSignupView, self).get_context_data(**kwargs)
        context['signupform'] = get_form_class(app_settings.FORMS, 'signup', SignupForm())
        return context

login = JointLoginSignupView.as_view()
