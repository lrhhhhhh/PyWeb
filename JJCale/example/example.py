from JJCale.app import JJCale
from JJCale.response import TextPlainResponse, TextHTMLResponse
from JJCale.middlewares import MiddleWareInterface, BEFORE_REQUEST


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


app = JJCale()
app.router.register([
    ('/<username>', hello, 'index'),
    ('/welcome/<username>', welcome, 'welcome')
])
app.middleware_manager.register([MyMiddleware(), ])
app.run(debug=True)
