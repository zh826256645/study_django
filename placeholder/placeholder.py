# -*- coding:utf-8 -*-

import os
import sys
import hashlib

from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY', '5yrc$dbu1b*gqf-9-%^i%khhqn1c4txvc^h6)r$#b^90dp4+qs')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASS=(

    ),
)
from io import BytesIO

from PIL import Image, ImageDraw
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.core.cache import cache


class ImageForm(forms.Form):
    """
    Form to validate requested placeholder image.
    """
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):
        """
        Generate an image of the given type and return as raw bytes.
        """
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        # django 缓存
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)

        if content is None:
            print('Generating image...')
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            text_width, text_height = draw.textsize(text)

            if text_width < width and text_height < height:
                text_top = (height - text_height) // 2
                text_left = (width - text_width) // 2
                draw.text((text_left, text_top), text, fill=(255, 255, 255))

            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60 * 60)
        return content


def generate_etag(request, width, height):
    content = 'Placeholder: {0} x {1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(generate_etag)
def placeholder(request, width, height):
    # TODO: Rest of the view will go here
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Request')


def index(request):
    return HttpResponse('Hello World')


urlpatterns = (
    url('^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
    url('^$', index, name='homepage'),
)


application = get_wsgi_application()


if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
