import socket

from tornado.options import define, options
from tornado.web import Application as BaseApplication


class Application(BaseApplication):
    """
    A tornado implementation compatible with circus socket.
    """

    def listen(self, port, address="", **kwargs):
        if options.fd:
            from tornado.httpserver import HTTPServer
            sock = socket.fromfd(options.fd, socket.AF_INET, socket.SOCK_STREAM)

            server = HTTPServer(self, **kwargs)
            server.add_socket(sock)
        else:
            super(Application, self).listen(port, address, **kwargs)

define("fd", default=None, help="File Descriptor given by circus", type=int)
