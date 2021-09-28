from SearchNode import SearchNode
from Map import Map_Obj
import math

from queue import PriorityQueue

class Astar():
  def __init__(self, map, moving_goal = False):
    self.moving_goal = moving_goal
    self.map = map
    self.map_array = map.get_maps()[0]
    self.goal = (map.get_goal_pos()[0], map.get_goal_pos()[1])
    self.start = (map.get_start_pos()[0], map.get_start_pos()[1])
    self.counter = 0
    self.open = PriorityQueue()
    self.open_map = set()
    self.closed_dict = {}
    self.frames = []

    startNode = SearchNode(self.start, self.get_heuristic_distance)
    startNode.g = 0
    self.open.put((0, startNode))
    self.open_map.add(startNode.state)

  def legal_coordinate(self, x,y):
    map_size = len(self.map_array)
    if (x < 0 or x > map_size-1):
      return False
    if (y < 0 or y > map_size-1):
      return False
    if (self.map.get_cell_value([x,y]) == -1):
      return False
    return True

  # Gets the distance (or cost) to move to a position
  def get_distance(self, target):
    return self.map.get_cell_value(target.state)

  # Gets the manhattan distance to the goal
  # If goal is moving, we ignore all y coordinates lower than the start position
  # as we know the moving goal only moves horizontally, and is currently above us
  def get_heuristic_distance(self, state):
    if self.moving_goal:
      if state[0] > self.start[0]:
        return math.inf
      return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])
    else:
      return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

  # Generate successor nodes for a given state
  def get_children(self, parent):
    x = parent.state[0]
    y = parent.state[1]
    explore_positions = [(x-1, y), (x+1, y), (x,y+1), (x, y-1)]

    #Construct nodes for legal coordinates
    children = [SearchNode(state, self.get_heuristic_distance, parent) 
                  for state in explore_positions 
                  if self.legal_coordinate(state[0],state[1])]

    return children

  ###
  # Helper functions for coloring the path on the map
  ###
  def set_node_ispath(self, node):
    self.map.set_cell_value([node.state[0], node.state[1]], ' x ')

  def set_node_expanded(self, node):
    self.map.set_cell_value([node.state[0], node.state[1]], ' y ')

  def set_node_generated(self, node):
    if self.map.get_cell_value(node.state) == 1:
      self.map.set_cell_value([node.state[0], node.state[1]], ' f ')

  def render_path(self, node):
    while(node.parent):
      node = node.parent
      self.set_node_ispath(node)
    self.map.set_cell_value([self.start[0], self.start[1]], ' S ')

  def reset_render_path(self, node):
    while(node.parent):
      node = node.parent
      self.set_node_expanded(node)
    self.map.set_cell_value([self.start[0], self.start[1]], ' S ')

  def render_frame(self):
    self.frames.append(self.map.show_map())

  # The search algorithm loop
  def search(self):
    while not self.open.empty():
      # Pop top priority node and add to closed set
      self.counter = self.counter + 1
      node = self.open.get()[1]
      self.open_map.remove(node.state)
      self.closed_dict[node.state] = node

      # If moving goal, tick 
      if self.moving_goal:
          self.goal = (self.map.get_goal_pos()[0], self.map.get_goal_pos()[1])
          self.map.tick()

      # Render the current best path and add to frame
      self.render_path(node)
      self.render_frame()
      self.reset_render_path(node)

      # Print current node being explored
      print("Exploring ", node.state, " - Iteration ", self.counter, "  ", end="\r", flush=True)

      # If node is goal state, return
      if node.state == self.goal:
        print("\nFinished in", self.counter, "iterations")
        return True

      # Get node children and explore them
      children = self.get_children(node)
      while (any(children)):
        child = children.pop()

        # Node already explored, use that one
        if child.state in self.closed_dict:
          child = self.closed_dict[child.state]
        else:
          self.set_node_generated(child)

        # Distance from start to child through parent
        g = node.g + self.get_distance(child)
        
        # Is path through this parent node a better path to child?
        # If yes, update child node
        if g < child.g:
          child.g = g
          
          # Better path found to child node, propagate to all children
          if child.state not in self.open_map:
            self.open.put((child.f(), child))
            self.open_map.add(child.state)

    return False
