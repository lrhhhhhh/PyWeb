from abc import ABCMeta, abstractmethod

BEFORE_REQUEST = 0x1
AFTER_RESPONSE = 0x2


class MiddleWareInterface(metaclass=ABCMeta):
    type = BEFORE_REQUEST
    # type = AFTER_RESPONSE

    @abstractmethod
    def apply_before(self, request, **kwargs):
        pass

    @abstractmethod
    def apply_after(self, response, **kwargs):
        pass


class MiddlewareManager:
    def __init__(self, middlewares=None):
        if not middlewares:
            self.middlewares = list()
        else:
            self.middlewares = middlewares

    def register(self, middlewares):
        self.middlewares.extend(middlewares)

    def apply_before(self, request):
        for middleware in self.middlewares:
            if middleware.type == BEFORE_REQUEST:
                middleware.apply_before(request)
        return request

    def apply_after(self, request, response):
        for middleware in self.middlewares:
            if middleware.type == AFTER_RESPONSE:
                middleware.apply_after(response, request=request)
        return response

