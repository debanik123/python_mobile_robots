from turtle import color
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

class DFS(object):
    def __init__(self, maze, start, goal, obs_sym):
        self.start = start
        self.goal = goal
        self.maze = maze
        self.r, self.c = len(maze), len(maze[0])
        self.visited = [[False]*self.c for _ in range(self.r)]
        self.path_cnt = 0
        self.direction_arr = [[-1,0],[1,0],[0,-1],[0,1]] # for side moves
        self.direction_arr_dia = [[-1,0],[1,0],[0,-1],[0,1], [-1,-1],[-1, 1],[1,-1],[1,1]]
        self.obs_sym = obs_sym
        
    def dfs(self):
        self.stack = []
        self.stack.append((self.start[0],self.start[1],self.path_cnt,[self.start[0]*self.c+self.start[1]]))
        
        while(len(self.stack)!=0):
            self.coor = self.stack[len(self.stack)-1]
            self.stack.remove(self.stack[len(self.stack)-1])
            self.visited[self.coor[0]][self.coor[1]] =True
            
            if (self.coor[0],self.coor[1]) == self.goal:
                return self.coor[2], [[i//self.c, i%self.c] for i in self.coor[3]]
            
            for dir_vec in self.direction_arr_dia:
                nr = self.coor[0]+dir_vec[0]
                nc = self.coor[1]+dir_vec[1]
                
                if(nr<0 or nc<0 or nr>=self.r or nc>=self.c or self.visited[nr][nc] or self.maze[nr][nc] == self.obs_sym):
                    continue
                
                self.stack.append((nr,nc, self.coor[2]+1, self.coor[3]+[nr*self.c+nc]))
        
                

grid = np.array([[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

print(len(grid))
print(grid)
r,c = len(grid), len(grid[0])
print(r,c)
# fig, ax = plt.subplot(figsize=(r,c))
try:
    start = (0,0)
    goal = (9,4)

    d = DFS(grid, start, goal,1)
    pathLen, pathItems = d.dfs()

    print("Length of path:", pathLen)
    print("Path Items:->", *pathItems)
    x,y=[],[]
    for it in pathItems:
        x.append(it[0])
        y.append(it[1])
    
    plt.imshow(grid, cmap=plt.cm.Dark2)
    plt.scatter(start[1],start[0], marker="*", color="yellow", s=200)
    plt.scatter(goal[1],goal[0], marker="*", color="red", s=200)
    plt.plot(y,x,color="black")
    plt.show()

except KeyboardInterrupt:
    print("Closed with CTRL-C")
except IOError:
    print("I/O error")