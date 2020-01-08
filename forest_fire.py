import sys, math, random
import pygame
import pygame.draw
import numpy as np
import matplotlib.pyplot as plt

__cellSize__ = 40
__gridDim__ = (35, 35) 
__screenSize__ = (int(__gridDim__[0]*61.5),int(__gridDim__[1]*60.9))

__firecolor__ = (255, 0, 0)
__treecolor__ = (0, 255, 0)
__burntcolor__ = (255, 255, 255)

def getColorCell(n):
    if n == 0:
        return __treecolor__
    elif n == 1:
        return __firecolor__
    else:
        return __burntcolor__

class Forest:
    def __init__(self, fire_number, p=0.5):
        print("Creating a grid of dimensions " + str(__gridDim__))
        self.grid = np.zeros(__gridDim__)
        self.size = __gridDim__[0]
        self.p = p
        for i in range(fire_number):
            a = np.random.randint(0, self.size-1)
            b = np.random.randint(0, self.size-1)
            self.grid[a, b] = 1

    def step(self):
        to_update = []
        for i in range(self.size):
            for j in range(self.size):
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i+1, j+1),
                             (i-1, j-1), (i-1, j+1), (i+1, j-1)]
                if self.grid[i, j] == 0:
                    prob = np.random.randint(0, 10)
                    if (prob <= self.p * 10):
                        for vi, vj in neighbors:
                            if self.is_valid(vi, vj) and self.grid[vi, vj] == 1:
                                to_update.append((i, j))
                                break
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == 1:
                    self.grid[i, j] = 2
        for a,b in to_update:
            self.grid[a, b] = 1
        return (len(to_update) == 0)
        

    def is_valid(self, vi, vj):
        if vi < 0 or vj < 0 or vi >= self.size or vj >= self.size:
            return False
        else:
            return True

    def get_trees_left(self):
        nb_tree = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == 0:
                    nb_tree += 1
        return nb_tree

class Scene:
    _grid = None
    _font = None

    def __init__(self, perco, render=True):
        if render:
            pygame.init()
            self._screen = pygame.display.set_mode(__screenSize__)
            self._font = pygame.font.SysFont('Arial',25)
        self._grid = Forest(1, perco)

    def drawMe(self):
        self._screen.fill((128,128,128))
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(self._screen, 
                        getColorCell(self._grid.grid.item((x,y))),
                        (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))


    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,1,color),position)

    def update(self):
        return self._grid.step()

def plot_result(results):
    plt.plot(results["perco_coeff"], results["tree_left"])
    plt.xlabel("Densité")
    plt.ylabel("Coefficient de percolation")
    plt.show()

def fast_simulation(epochs=1):
    results = {"perco_coeff": [], "tree_left": []}
    pmax = 1
    delta = 0.05
    for e in range(epochs):
        results["perco_coeff"] = []
        results["tree_left"].append([])
        p = 0
        while p < pmax:
            scene = Scene(perco=p, render=False)
            done = False
            while done == False:
                #clock.tick(30)
                #scene.drawMe()
                done = scene.update()
                #pygame.display.flip()
            results["perco_coeff"].append(p)
            results["tree_left"][e].append(scene._grid.get_trees_left()/(scene._grid.size**2))
            p += delta
            #pygame.quit()
    plot_result(results)

def sim_with_grid():
    clock = pygame.time.Clock()
    scene = Scene(perco=p)
    done = False
    while done == False:
        clock.tick(30)
        scene.drawMe()
        done = scene.update()
        pygame.display.flip()
    pygame.quit()