import logging
import azure.functions as func
from django.core.wsgi import get_wsgi_application
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobgenie.settings')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

application = get_wsgi_application()

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(application).handle(req, context)
