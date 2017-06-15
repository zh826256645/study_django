# -*- coding:utf-8 -*-

import os
import sys

from django.conf import settings

BASE_DIR = os.path.dirname(__file__)

ALLOWED_HOSTS = ['0.0.0.0']

settings.configure(
    DEBUG=True,
    SECRET_KEY='5yrc$dbu1b*gqf-9-%^i%khhqn1c4txvc^h6)r$#b^90dp4+qs',
    ROOT_URLCONF='sitebuilder.urls',
    MIDDLEWARE_CLASSES=(),
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'sitebuilder',
    ),
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        },
    ),
    STATIC_URL='/static/',
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, 'pages'),
)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
