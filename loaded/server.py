"""
The HTTP webserver for build agents.
"""

import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({1: 4, 'b': 'c'})


agent_application = tornado.web.Application([
    (r'/', MainHandler),
])
