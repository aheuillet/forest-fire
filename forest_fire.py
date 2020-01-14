import sys
import math
import time
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
        for a, b in to_update:
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
        self._screen_size = (int(self._grid.size*61.5),
                             int(self._grid.size*60.9))
        if render:
            pygame.init()
            self._screen = pygame.display.set_mode(self._screen_size)
            self._font = pygame.font.SysFont('Arial', 25)

    def drawMe(self):
        self._screen.fill((128, 128, 128))
        for x in range(self._grid.size):
            for y in range(self._grid.size):
                pygame.draw.rect(self._screen,
                                 getColorCell(self._grid.grid.item((x, y))),
                                 (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))

    def drawText(self, text, position, color=(255, 64, 64)):
        self._screen.blit(self._font.render(text, 1, color), position)

    def update(self):
        return self._grid.step()


def compute_perco_threshold(perco_coeffs, perco_threshold_vals):
    best = 0
    index = 0
    for i in range(1, len(perco_threshold_vals)):
        diff = abs(perco_threshold_vals[i] - perco_threshold_vals[i-1])
        if diff > best:
            best = diff
            index = i
    return ((perco_coeffs[index] + perco_coeffs[index-1])/2)


def plot_result(results):
    plt.ion()
    plt.plot(results["perco_coeff"], results["tree_left"])
    plt.xlabel("Densité")
    plt.ylabel("Coefficient de percolation")
    plt.show()


def analyze_results(results):
    results["steps"] = np.mean(results["steps"])
    results["mean_tree_left"] = np.mean(results["tree_left"])
    results["perco_threshold"] = compute_perco_threshold(
        results["perco_coeff"], results["tree_left"])
    return results


def simulate(epochs=1, nb_fires=1, size=25, p_start=0, p_max=1, delta=0.05, graphical_rendering=True):
    results = {"perco_coeff": [], "tree_left": [],
               "steps": [], "mean_tree_left": 0}
    clock = pygame.time.Clock()
    results["perco_coeff"] = []
    i = 0
    p = p_start
    while p < p_max:
        results["tree_left"].append([])
        results["steps"].append([])
        for e in range(epochs):
            scene = Scene(p, nb_fires, size, render=graphical_rendering)
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
                s += 1
            results["steps"][i].append(s)
            results["tree_left"][i].append(
                scene._grid.get_trees_left()/(scene._grid.size**2))
        results["perco_coeff"].append(p)
        results["tree_left"][i] = np.mean(results["tree_left"][i])
        results["steps"][i] = np.mean(results["steps"][i])
        p += delta
        i += 1
    if graphical_rendering:
        pygame.quit()
    return analyze_results(results)
