# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime
from sqlalchemy_dao import Model

dao = None

class Sensor(Model):
    name = Column(String, primary_key=True)
    time = Column(DateTime)
    value = Column(String)
    