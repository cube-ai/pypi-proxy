import os
import tornado.web
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import requests


class PackagesApi(tornado.web.RequestHandler):

    async def get(self, path, *args, **kwargs):

        full_path = os.path.join(os.getcwd() + '/packages', path)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as file:
                self.write(file.read())
                return
        else:
            url = 'http://mirrors.aliyun.com/pypi/packages/{}'.format(path)
            request = HTTPRequest(
                url=url,
                method='GET',
                request_timeout=900
            )

            http = AsyncHTTPClient()
            try:
                res = await http.fetch(request)
                res_code = res.code
                res_headers = res.headers
                res_body = res.body
            except Exception as e:
                res = requests.get(url)  # 如果异步下载失败则尝试同步下载
                if res.status_code != 200:
                    self.send_error(500)
                    return
                res_code = res.status_code
                res_headers = res.headers
                res_body = res.content

            i = full_path.rfind('/')
            path_prefix = full_path[:i]
            if not os.path.exists(path_prefix):
                os.makedirs(path_prefix)

            with open(full_path, 'wb') as file:
                file.write(res_body)

            self.set_status(res_code)
            self._headers = res_headers
            self.write(res_body)
