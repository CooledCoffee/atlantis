# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DateTime, Boolean, Float
from sqlalchemy_dao import Model

dao = None

class Problem(Model):
    name = Column(String, primary_key=True)
    exists = Column(Boolean, nullable=False)

class Sensor(Model):
    name = Column(String, primary_key=True)
    error_rate = Column(Float)
    time = Column(DateTime)
    value = Column(String, nullable=False, default='null')
    
class Solution(Model):
    name = Column(String, primary_key=True)
    applied = Column(Boolean, nullable=False)
    
ProblemModel = Problem
SensorModel = Sensor
SolutionModel = Solution
