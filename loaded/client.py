"""
The HTTP web client for build agents.
"""

from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from urllib.parse import urljoin


AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")


class Client(object):
    """
    Implements the client-side of Loaded agents.
    """

    def __init__(self, host, port):
        self.client = AsyncHTTPClient()
        self.host = host
        self.port = port
        self.on_complete = None

    @property
    def base_url(self):
        return 'http://{host}:{port}/'.format(host=self.host, port=self.port)

    def url(self, suffix):
        return urljoin(self.base_url, suffix)

    def fetch_info(self, callback):
        return self.client.fetch(self.url('info'), callback=callback)

    def on_info(self, response):
        try:
            response.rethrow()

            print(json_decode(response.body))
        finally:
            if self.on_complete:
                self.on_complete()

    def build(self):
        self.fetch_info(callback=self.on_info)
