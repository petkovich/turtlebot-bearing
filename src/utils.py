from constants import *
from math import pi, atan2, sin, cos
import numpy as np

def anglediff(reference, measured):
    return pi/2 - abs(pi/2 - abs(reference - measured) % pi)
    #return atan2(cos(reference-measured), sin(reference-measured))


