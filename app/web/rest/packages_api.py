import os
import tornado.web
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import asyncio
import aiofiles
import threading
from app.service import file_service


class PackagesApi(tornado.web.RequestHandler):

    async def get(self, package, *args, **kwargs):

        full_path = os.path.join(os.getcwd() + '/packages', package)
        path = full_path[: full_path.rfind('/')]
        filename = full_path[full_path.rfind('/') + 1:]

        if os.path.exists(full_path):
            async with aiofiles.open(full_path, 'rb') as file:
                self.write(await file.read())
            return

        else:
            # 注意域名： doubanio 而不是 douban
            url = 'https://pypi.doubanio.com/packages/{}'.format(package)
            request = HTTPRequest(
                url=url,
                method='GET',
                request_timeout=600
            )

            http = AsyncHTTPClient()
            try:
                res = await http.fetch(request)

                thread = threading.Thread(
                    target=file_service.write_thread,
                    args=(path, filename, res.body)
                )
                thread.setDaemon(True)
                thread.start()

                self.set_status(res.code)
                self._headers = res.headers
                self.write(res.body)

            except Exception as e:
                finish = {'done': False}
                thread = threading.Thread(
                    target=file_service.download_thread,
                    args=(url, path, filename, finish)
                )
                thread.setDaemon(True)
                thread.start()

                # 等待线程中下载结束
                while not finish['done']:
                    await asyncio.sleep(1)

                if os.path.exists(full_path):
                    async with aiofiles.open(full_path, 'rb') as file:
                        self.write(await file.read())
                        return
                else:
                    self.send_error(404)
