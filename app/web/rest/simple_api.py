import tornado.web
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class SimpleApi(tornado.web.RequestHandler):

    async def get(self, package, *args, **kwargs):

        url = 'https://pypi.douban.com/simple/{}/'.format(package)
        request = HTTPRequest(
            url=url,
            method='GET'
        )

        http = AsyncHTTPClient()
        try:
            res = await http.fetch(request)
        except Exception as e:
            self.send_error(500)
            return

        self.set_status(res.code)
        self._headers = res.headers

        self.write(res.body)
