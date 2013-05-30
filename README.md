circus_tornado
==============

A tornado application implementation compatible with circus sockets.

As tornado is not WSGI complient, we cannot use chaussette to run tornado
applications with circus sockets.

This project package a compatible version of tornado Application so you can
easily run tornado with all circus awesomeness.

Use circus_tornado
==================

Let's take a simple example, the hello world:

    import tornado.ioloop
    import tornado.web

    from tornado.web import Application

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")

    application = Application([
        (r"/", MainHandler),
    ])

    if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

If you want to run it with circus, you can't use socket web and fallback to
launch them and let it bind its socket:

    [watcher:hello]
    cmd = python hello_world.py

But good news, with circus_tornado, it's no longer true. Just import Application
from circus_tornado package:

    import tornado.ioloop
    import tornado.web

    from tornado_circus import Application

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")

    application = Application([
        (r"/", MainHandler),
    ])

    if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

One more requirement, you must call tornado.options.parse_command_line
**before** calling application.listen or it will not use circus socket. So the
real code is:

    import tornado.ioloop
    import tornado.web

    from tornado.options import parse_command_line
    from tornado_circus import Application

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, world")

    application = Application([
        (r"/", MainHandler),
    ])

    if __name__ == "__main__":
        parse_command_line()
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

And finally the circus configuration:

    [watcher:hello]
    cmd = python hello_world.py --fd=$(circus.sockets.hello)
    use_sockets = True

    [socket:hello]
    host = 127.0.0.1
    port = 9000

And you're done. You can go to http://localhost:9000 to check if it works.

You can even launch a quick benchmark and check that it holds the load:

    $> boom -n 10000 -c 100 http://localhost:9000                       10:38:48
    Server Software: TornadoServer/2.4.1
    Running GET http://127.0.0.1:9000
        Host: localhost
    Running 10000 times per 100 workers.
    Starting the load [===...===] Done

    -------- Errors --------

    -------- Results --------
    Successful calls        10000
    Total time              9.3364 s
    Average                 0.0656 s
    Fastest                 0.0228 s
    Slowest                 0.1009 s
    Amplitude               0.0781 s
    RPS                     1071
    BSI                     Woooooo Fast

    -------- Status codes --------
    Code 200                10000 times.

    -------- Legend --------
    RPS: Request Per Second
    BSI: Boom Speed Index
