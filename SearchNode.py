import math
from enum import Enum

class SearchNode():
  state = (None, None)
  g = math.inf
  h = math.inf
  parent = None
  children = None

  def __init__(self, state, h, parent = None):
    self.state = state
    self.parent = parent
    self.h = h(self.state)

  def f(self):
    return self.g + self.h

  def __gt__(self, other):
    return self.f() > other.f()