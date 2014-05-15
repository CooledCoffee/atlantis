# -*- coding: utf-8 -*-
from decorated.util import modutil
import inflection

def calc_name(cls):
    name = inflection.underscore(cls.__name__)
    ss = name.split('_')
    return '_'.join(ss[:-1])

def init():
    modutil.load_tree('devices')
    modutil.load_tree('rules')
    