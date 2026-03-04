import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#для масштаба
# class ScaleManager:
#     def __init__(self, initial_scale=1.0):
#         self.factor = initial_scale

#     def scale_value(self, value):
#         return int(value * self.factor)

class ScaleManager(QObject):
    scaleFactorChanged = pyqtSignal(float)

    def __init__(self, initial_scale=1.0):
        super().__init__()
        self._factor = initial_scale

    @property
    def factor(self):
        return self._factor

    @factor.setter
    def factor(self, value):
        if value != self._factor:
            self._factor = value
            self.scaleFactorChanged.emit(value)

    def scale_value(self, value):
        return int(value * self._factor)

