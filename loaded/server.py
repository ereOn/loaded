"""
The HTTP web server for build agents.
"""

import socket

from tornado.web import (
    Application,
    RequestHandler,
    URLSpec,
)
from tornado.websocket import WebSocketHandler


class InfoHandler(RequestHandler):
    """
    Get information about the current agent.
    """

    def get(self):
        self.write({
            'system': {
                'hostname': socket.getfqdn(),
            },
            'urls': {
                'work': self.reverse_url('work'),
            },
        })


class WorkHandler(WebSocketHandler):
    pass


server = Application([
    URLSpec(r'/info', InfoHandler, name='info'),
    URLSpec(r'/work', WorkHandler, name='work'),
])
