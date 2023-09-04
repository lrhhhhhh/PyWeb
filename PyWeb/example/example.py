from PyWeb.app import PyWeb
from PyWeb.response import TextPlainResponse, TextHTMLResponse
from PyWeb.middlewares import MiddleWareInterface, BEFORE_REQUEST


def index(request):
    return TextPlainResponse(f"Welcome to PyWeb index")


def hello(request, username):
    return TextPlainResponse(f'hello, {username}')


def welcome(request, username):
    return TextHTMLResponse(context={'username': username}, template_path='template', template_name='welcome.html')


class MyMiddleware(MiddleWareInterface):
    type = BEFORE_REQUEST

    def apply_before(self, request, **kwargs):
        print('middleware apply before', request)

    def apply_after(self, response, **kwargs):
        pass


if __name__ == "__main__":
    app = PyWeb()
    app.router.register([
        ('/', index, 'index'),
        ('/<username>', hello, 'hello'),
        ('/welcome/<username>', welcome, 'welcome')
    ])
    app.middleware_manager.register([MyMiddleware(), ])
    app.run(debug=True)
