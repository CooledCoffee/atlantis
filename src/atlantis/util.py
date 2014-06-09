# -*- coding: utf-8 -*-
from atlantis import templates
from decorated.util import modutil
import inflection

def calc_name(cls):
    name = inflection.underscore(cls.__name__)
    ss = name.split('_')
    return '_'.join(ss[:-1])

def init(dao, templates_dir):
    import db
    db.dao = dao
    templates.init(templates_dir)
    modutil.load_tree('devices')
    modutil.load_tree('rules')
    import worker  # @UnusedImport
    