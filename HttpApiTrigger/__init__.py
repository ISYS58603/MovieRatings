import logging
import azure.functions as func
from api import app
from azure.functions import WsgiMiddleware

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Received request for Flask API.')
    return WsgiMiddleware(app.wsgi_app).handle(req, context)
