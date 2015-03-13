# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.core.controller import Controller
from atlantis.core.device import AbstractDevice
from atlantis.core.problem import Problem
from atlantis.core.sensor import Sensor
from atlantis.core.solution import Solution, DisableByProblem

AbstractDevice = AbstractDevice
sensor = Sensor
controller = Controller
problem = Problem
solution = Solution
disable_by_problem = DisableByProblem

init = util.init
