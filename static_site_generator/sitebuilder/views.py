# -*- coding:utf-8 -*-
import json
import os

from django.conf import settings
from django.http import Http404
from django.template import Template, Context
from django.template.loader_tags import BlockNode
from django.shortcuts import render
from django.utils._os import safe_join


def get_page_or_404(name):
    """Return page content as a Django template or raise 404 error"""
    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
    except ValueError:
        raise Http404('Page Not Found')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page Not Found')

    with open(file_path, 'rb') as f:
        this_page = Template(f.read())

    meta = None
    for i, node in enumerate(list(this_page.nodelist)):
        if isinstance(node, BlockNode) and node.name == 'context':
            meta = this_page.nodelist.pop(i)
            break
    this_page._meta = meta
    return this_page


def page(request, slug='index'):
    """Return the requested page if found."""
    file_name = '{}.html'.format(slug)
    this_page = get_page_or_404(file_name)
    context = {
        'slug': slug,
        'page': this_page,
    }

    if this_page._meta is not None:
        meta = this_page._meta.render(Context())
        print(meta)
        extra_context = json.loads(meta)
        context.update(extra_context)
    return render(request, 'page.html', context)
