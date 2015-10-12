"""
Handle configuration files.
"""

import six
import yaml

from voluptuous import (
    Any,
    Required,
    Schema,
)


def List(type):
    def f(v):
        v = type(v)

        if not isinstance(v, list):
            return [v]
        else:
            return v

    return f



class Config(object):
    schema = Schema({
        Required('run', default=[]): List(Any([six.text_type], six.text_type)),
    })

    @classmethod
    def from_file(path):
        """
        Load a configuration from a file.

        :param path: The path to the configuration file to load.
        :returns: A `Config` instance.
        """
        with open(path) as file_:
            return Config(data=yaml.load(file_))

    def __init__(self, data):
        self.data = self.schema(data)
