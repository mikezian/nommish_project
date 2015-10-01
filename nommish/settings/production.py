# -*- coding: utf-8 -*-
from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    'nommish.com',  # Allow domain and subdomains
    '.nommish.com',  # Allow domain and subdomains
]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
#CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
#SESSION_COOKIE_SECURE = True