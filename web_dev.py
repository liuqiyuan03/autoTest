# coding=utf8

from webob import dec,Request,Response
from webob.exc import HTTPNotFound
from wsgiref.simple_server import make_server

class Route:
    ROUTETABLE = {}

    @classmethod
    def register(self,path):
        def warper(handler):
            self.ROUTETABLE[path] = handler
            return handler
        return warper

@Route.register("/")
def index(request):
    # ret = Response()
    # ret.body
    return "<h1>hello world</h1>"

@Route.register("/python")
def pythonpath(request):
    return "<h1>hello python </h1>"

@Route.register("/java")
def javapath(request):
	return "<h1>hello java</h1>"

class Application:
    _Route = Route

    @dec.wsgify
    def __call__(self, request):
        try:
            return self._Route.ROUTETABLE[request.path](request)
        except Exception:
            raise HTTPNotFound("<h1>你访问的页面被外星人劫持了~</h1>")

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 9999
    server = make_server(ip,port,Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()