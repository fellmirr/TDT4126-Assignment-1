from SearchNode import SearchNode
from Map import Map_Obj

from queue import PriorityQueue

class Astar():
  def __init__(self, map):
    self.map = map
    self.map_array = map.get_maps()[0]
    self.goal = (map.get_end_goal_pos()[0], map.get_end_goal_pos()[1])
    self.start = (map.get_start_pos()[0], map.get_start_pos()[1])
    self.counter = 0
    self.open = PriorityQueue()
    self.open_map = set()
    self.closed_dict = {}
    self.frames = []

    startNode = SearchNode(self.start, self.get_heuristic_distance)
    startNode.g = 0
    self.open.put((0, startNode))
    self.open_map.add(startNode.pos)

  def legal_coordinate(self, x,y):
    map_size = len(self.map_array)
    if (x < 0 or x > map_size-1):
      return False
    if (y < 0 or y > map_size-1):
      return False
    if (self.map.get_cell_value([x,y]) == -1):
      return False
    return True

  def get_distance(self, target):
    return self.map.get_cell_value(target.pos)

  def get_heuristic_distance(self, pos):
    return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

  def get_children(self, parent):
    x = parent.pos[0]
    y = parent.pos[1]
    explore_positions = [(x-1, y), (x+1, y), (x,y+1), (x, y-1)]

    #Construct nodes for legal coordinates
    children = [SearchNode(pos, self.get_heuristic_distance, parent) 
                  for pos in explore_positions 
                  if self.legal_coordinate(pos[0],pos[1])]

    return children

  def set_node_ispath(self, node):
    self.map.set_cell_value([node.pos[0], node.pos[1]], ' x ')

  def set_node_expanded(self, node):
    self.map.set_cell_value([node.pos[0], node.pos[1]], ' y ')

  def set_node_generated(self, node):
    if self.map.get_cell_value(node.pos) == 1:
      self.map.set_cell_value([node.pos[0], node.pos[1]], ' f ')

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

  def search(self):
    while not self.open.empty():
      # Pop top priority node and add to closed set
      self.counter = self.counter + 1
      node = self.open.get()[1]
      self.open_map.remove(node.pos)
      self.closed_dict[node.pos] = node

      # Render the current best path and add to frame
      self.render_path(node)
      self.render_frame()
      self.reset_render_path(node)

      print("Exploring ", node.pos, " - Iteration ", self.counter, "  ", end="\r", flush=True)

      # If node is goal position, return
      if node.pos == self.goal:
        print("\nFinished in", self.counter, "iterations")
        return True

      # Get node children and explore them
      children = self.get_children(node)
      while (any(children)):
        child = children.pop()

        # Node already explored, use that one
        if child.pos in self.closed_dict:
          child = self.closed_dict[child.pos]
        else:
          self.set_node_generated(child)

        # Distance from start to child through parent
        g = node.g + self.get_distance(child)
        
        # Is path through this parent node a bettar path to child?
        # If yes, update child node
        if g < child.g:
          child.g = g
          
          # Better path found to child node, propagate to all children
          if child.pos not in self.open_map:
            self.open.put((child.f(), child))
            self.open_map.add(child.pos)

    return False
