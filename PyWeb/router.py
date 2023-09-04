from werkzeug.routing import Map, Rule
from werkzeug.exceptions import NotFound
from dataclasses import dataclass


@dataclass
class SubRouter:
    url: str
    view_func: callable
    endpoint: str

    def __iter__(self):
        return iter([self.url, self.view_func, self.endpoint])


class Router:
    def __init__(self):
        self.rules = dict()
        self.url_set = set()
        self.map = Map()

    def merge(self, url, sub_router, endpoint):
        sub_url, view_func, sub_endpoint = sub_router
        new_url = url + sub_url
        new_endpoint = endpoint + '.' + sub_endpoint,
        self.add(new_url, view_func, new_endpoint)

    def add(self, url, view_func, endpoint):
        if url in self.url_set:
            raise ValueError(f'url {url} already exists')
        else:
            self.url_set.add(url)

        if endpoint in self.rules:
            raise ValueError(f'endpoint {endpoint} already exists')

        self.map.add(
            Rule(url, endpoint=endpoint)
        )
        self.rules[endpoint] = {
            'view_func': view_func,
            'url': url
        }

    def register(self, rules):
        for rule in rules:
            url, x, endpoint = rule

            if isinstance(x, SubRouter):
                self.merge(url, x, endpoint)
            elif callable(x):
                self.add(url, x, endpoint)
            else:
                raise TypeError('Expect router or view_func')

    def route(self, request):
        map_adapter = self.map.bind_to_environ(request.environ)
        try:
            endpoint, kwargs = map_adapter.match()
            view_func = self.rules.get(endpoint)['view_func']
            return view_func, kwargs
        except NotFound as e:
            raise NotFound(f'path {request.path} not found')

    def reverse(self, endpoint):
        res = self.rules.get(endpoint)
        if res:
            return res['url']
        else:
            return None


if __name__ == '__main__':
    routes = [
        ('/index/something', SubRouter(url='/people', view_func=lambda: 'fake view func1', endpoint='people'), 'index'),
        ('/blog', SubRouter(url='/article1', view_func=lambda: 'fake view func2', endpoint='article'), 'blog'),
        ('/about', lambda: 'fake view func3', 'about'),
    ]
    router = Router()
    router.register(routes)
    print(router.rules)
    print(router.map)
