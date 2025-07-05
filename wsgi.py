from asgi_wsgi import WsgiMiddleware
from main import app as asgi_app

# Wrap the FastAPI ASGI app with WsgiMiddleware for WSGI compatibility
application = WsgiMiddleware(asgi_app)
