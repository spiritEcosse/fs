#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=fs.settings tornado_main.py
# Serves by default at
# http://localhost:8080/hello-tornado and
# http://localhost:8080/hello-django

from fs.settings import BASE_DIR
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fs.settings")

# Activate your virtual env
activate_env = os.path.expanduser(os.path.join(BASE_DIR, "ENV/bin/activate_this.py"))
execfile(activate_env, dict(__file__=activate_env))


from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
if django.VERSION[1] > 5:
    django.setup()

define('port', type=int, default=8888)


def main():
    parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)), ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
