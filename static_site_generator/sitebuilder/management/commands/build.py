# -*- coding:utf-8 -*-

import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.test.client import Client


def get_pages():
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
        if name.endswith('.html'):
            yield name[:-5]


class Command(BaseCommand):
    help = 'Build static site output.'
    leave_locale_alone = True

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        """Request pages and build output."""
        # 带参数
        settings.DEBUG = False
        if args:
            pages = args
            available = list(get_pages())
            invalid = []
            # 校验文件是否存在
            for page in pages:
                if page not in available:
                    invalid.append(page)
            if invalid:
                msg = 'Invalid pages: {}'.format(', '.join(invalid))
                raise CommandError(msg)
        # 不带参数
        else:
            pages = get_pages()
            # 检查目录是否存在
            if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
                # 存在就删除它
                shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
            os.mkdir(settings.SITE_OUTPUT_DIRECTORY)

        os.makedirs(settings.STATIC_ROOT, exist_ok=True)
        call_command('collectstatic', interactive=False,
                     clear=True, verbosity=0)
        client = Client()
        for page in pages:
            url = reverse('page', kwargs={'slug': page})
            response = client.get(url)
            if page == 'index':
                output_dir = settings.SITE_OUTPUT_DIRECTORY
            else:
                output_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY, page)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

            with open(os.path.join(output_dir, page + '.html'), 'wb') as f:
                f.write(response.content)
