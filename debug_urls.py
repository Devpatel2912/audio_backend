import os
import sys
from django.core.wsgi import get_wsgi_application

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "audio_notes_backend.settings")
application = get_wsgi_application()

from django.urls import get_resolver
from django.urls import URLPattern, URLResolver

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    for l in lis:
        if isinstance(l, URLPattern):
            print('/' + ''.join(acc) + str(l.pattern))
        elif isinstance(l, URLResolver):
            list_urls(l.url_patterns, acc + [str(l.pattern)])

list_urls(get_resolver().url_patterns)
