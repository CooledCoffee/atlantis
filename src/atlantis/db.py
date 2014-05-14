# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime, Boolean
from sqlalchemy_dao import Model

dao = None

class Problem(Model):
    name = Column(String, primary_key=True)
    exists = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)

class Sensor(Model):
    name = Column(String, primary_key=True)
    time = Column(DateTime, nullable=False)
    value = Column(String, nullable=False)
    
ProblemModel = Problem
SensorModel = Sensor
