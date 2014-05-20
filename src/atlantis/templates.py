# -*- coding: utf-8 -*-
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
import os

env = None

def init():
    global env
    dirname = os.path.join(os.path.dirname(__file__), 'templates')
    loader = FileSystemLoader(dirname)
    env = Environment(loader=loader, extensions=['jinja2.ext.with_'], trim_blocks=True)
    
def render(template_name, **kw):
    template = env.get_template(template_name)
    return template.render(**kw)

init()
