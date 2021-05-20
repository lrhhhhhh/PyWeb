from werkzeug.exceptions import HTTPException
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request

from JJCale.middlewares import MiddlewareManager
from JJCale.router import Router


class JJCale:
    def __init__(self):
        self.middleware_manager = MiddlewareManager()
        self.router = Router()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        request = self.before_request(request)

        try:
            view_func, kwargs = self.router.route(request)
            response = view_func(request, **kwargs)
        except HTTPException as e:
            return e

        response = self.after_response(request, response)
        return response.__call__(environ, start_response)

    def before_request(self, request):
        return self.middleware_manager.apply_before(request)

    def after_response(self, request, response):
        return self.middleware_manager.apply_after(request, response)

    def run(self, host='localhost', port=23333, debug=False):
        run_simple(
            hostname=host,
            port=port,
            application=self.wsgi_app,
            use_reloader=debug,
            use_debugger=debug,
        )
