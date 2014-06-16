# -*- coding: utf-8 -*-
from atlantis.base import ExpiredError
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
import os

env = None

class AtlantisEnvironment(Environment):
    def getattr(self, obj, attr):
        try:
            return getattr(obj, attr)
        except ExpiredError:
            return None

def init(dirname=None):
    global env
    dirnames = [] if dirname is None else [dirname]
    dirnames.append(os.path.join(os.path.dirname(__file__), 'templates'))
    loader = FileSystemLoader(dirnames)
    env = AtlantisEnvironment(loader=loader, extensions=['jinja2.ext.with_'], trim_blocks=True)
    
def render(template_name, **kw):
    template = env.get_template(template_name)
    return template.render(**kw)
