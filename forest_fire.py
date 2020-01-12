import sys, math, time
import pygame
import pygame.draw
import numpy as np
import matplotlib.pyplot as plt

__cellSize__ = 40

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
    def __init__(self, fire_number, size, p=0.5):
        print(f"Creating a grid of dimensions ({size},{size})")
        self.grid = np.zeros((size, size))
        self.size = size
        self.propagated = False
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
            if a == self.size-1:
                self.propagated = True
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
    
    def get_stats(self):
        pass

class Scene:
    _grid = None
    _font = None

    def __init__(self, perco, nb_fires, size, render=True):
        self._grid = Forest(nb_fires, size, perco)
        self._screen_size = (int(self._grid.size*61.5),int(self._grid.size*60.9))
        if render:
            pygame.init()
            self._screen = pygame.display.set_mode(self._screen_size)
            self._font = pygame.font.SysFont('Arial',25)

    def drawMe(self):
        self._screen.fill((128,128,128))
        for x in range(self._grid.size):
            for y in range(self._grid.size):
                pygame.draw.rect(self._screen, 
                        getColorCell(self._grid.grid.item((x,y))),
                        (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))


    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,1,color),position)

    def update(self):
        return self._grid.step()

def compute_perco_threshold(perco_coeffs, tree_left):


def plot_result(results):
    plt.plot(results["perco_coeff"], results["tree_left"])
    plt.xlabel("Densité")
    plt.ylabel("Coefficient de percolation")
    results["perco_threshold"] = compute_perco_threshold()
    plt.show()

def fast_simulation(epochs=1, nb_fires=1, size=25):
    results = {"perco_coeff": [], "tree_left": [], "time_to_complete": []}
    pmax = 1
    delta = 0.05
    for e in range(epochs):
        results["perco_coeff"] = []
        results["tree_left"].append([])
        p = 0
        while p < pmax:
            scene = Scene(p, nbfires, size, render=False)
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

def sim_with_grid(size=25, nb_fires=1, perco=0.5):
    clock = pygame.time.Clock()
    scene = Scene(p, nb_fires, size)
    done = False
    while done == False:
        clock.tick(30)
        scene.drawMe()
        done = scene.update()
        pygame.display.flip()
    pygame.quit()

#merge both functions into one
def simulate(epochs=1, nb_fires=1, size=25, p_start=0, pmax=1, delta=0.05, graphical_rendering=True):
    results = {"perco_coeff": [], "tree_left": [], "time_to_complete": [], "steps": [], "perco_threshold": []}
    clock = pygame.time.Clock()
    for e in range(epochs):
        results["perco_coeff"] = []
        results["tree_left"].append([])
        p = p_start
        while p < pmax:
            scene = Scene(p, nbfires, size, render=graphical_rendering)
            done = False
            reached_propagation = False
            t1 = time.time()
            s = 0
            while done == False:
                if graphical_rendering:
                    clock.tick(30)
                    scene.drawMe()
                    pygame.display.flip()
                done = scene.update()
                if scene._grid.propagated and !reached_propagation:
                    results["perco_threshold"].append(time.time() - t1)
                    reached_propagation = True
                s += 1
            results["time_to_complete"].append(time.time() - t1)
            results["steps"].append(s)
            results["perco_coeff"].append(p)
            results["tree_left"][e].append(scene._grid.get_trees_left()/(scene._grid.size**2))
            p += delta
            if graphical_rendering:
                pygame.quit()
    return plot_result(results)