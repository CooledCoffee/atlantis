# -*- coding: utf-8 -*-
import inflection

def calc_name(cls):
    name = inflection.underscore(cls.__name__)
    ss = name.split('_')
    return '_'.join(ss[:-1])
