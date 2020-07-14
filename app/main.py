import tornado.web
import tornado.ioloop
import tornado.httpserver
from app.web.rest.API_ROUTES import API_ROUTES
import logging


def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

    app = tornado.web.Application(
        API_ROUTES
    )
    port = 7979
    http_server = tornado.httpserver.HTTPServer(app, max_buffer_size=800*1024*1024)
    http_server.listen(port)

    logging.critical('#######################################################################')
    logging.critical('    PYPI-PROXY service started')
    logging.critical('    Listening at port: {}'.format(port))
    logging.critical('#######################################################################')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
