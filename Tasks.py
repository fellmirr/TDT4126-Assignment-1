from PIL import Image
from Astar import Astar
from Map import Map_Obj

def saveGif(task, frames):
  print("Generating gif ...")

  gif = []
  for image in frames:
      gif.append(image.convert("P",palette=Image.ADAPTIVE))

  gif[0].save("results/task" + task + ".gif", 
    format="GIF", 
    append_images=gif[1:], 
    save_all=True,
    loop=0,
    duration=50,
    subrectangles=True)

##########
# Task 1 #
##########
print("-- Task 1 --")
map = Map_Obj(task=1)
astar = Astar(map)
astar.search()
saveGif("1", astar.frames)

###########
# Task 2  #
###########
print("-- Task 2 --")
map = Map_Obj(task=2)
astar = Astar(map)
result = astar.search()
saveGif("2", astar.frames)

###########
# Task 3  #
###########
print("-- Task 3 --")
map = Map_Obj(task=3)
astar = Astar(map)
result = astar.search()
saveGif("3", astar.frames)

###########
# Task 4  #
###########
print("-- Task 4 --")
map = Map_Obj(task=4)
astar = Astar(map)
result = astar.search()
saveGif("4", astar.frames)
