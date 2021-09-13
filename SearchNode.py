import math
from enum import Enum

class SearchNode():
  pos = (None, None)
  g = math.inf
  h = math.inf
  parent = None
  children = None

  def __init__(self, pos, h, parent = None):
    self.pos = pos
    self.parent = parent
    self.h = h(self.pos)

  def f(self):
    return self.g + self.h

  def __gt__(self, other):
    return self.f() > other.f()