import sys
import math
import time
import pygame
import pygame.draw
import numpy as np
from random import random
import matplotlib.pyplot as plt

__cellSize__ = 7

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


def getCellNeighbors(c):
    (i, j) = c
    return [(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i+1, j+1),
            (i-1, j-1), (i-1, j+1), (i+1, j-1)]


class Forest:
    def __init__(self, size, p=0.5):
        self.grid = np.zeros((size, size))
        self.size = size
        self.propagated = False
        self.burning_trees = []
        self.p = p
        self.grid[int(self.size/2), int(self.size/2)] = 1
        self.burning_trees.append((int(self.size/2), int(self.size/2)))

    def step(self):
        to_update = []
        for b in self.burning_trees:
            neighbors = getCellNeighbors(b)
            (xb, yb) = b
            self.grid[xb, yb] = 2
            for n in neighbors:
                r = random()
                if (r < self.p):
                    (xn, yn) = n
                    if self.is_valid(xn, yn) and self.grid[xn, yn] == 0:
                        self.grid[xn, yn] = 1
                        to_update.append(n)
        self.burning_trees = to_update
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

    def __init__(self, perco, size, render=True):
        self._grid = Forest(size, perco)
        self._screen_size = (int(self._grid.size*7),
                             int(self._grid.size*7))
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
    plt.plot(results["perco_coeff"], results["tree_left"])
    plt.xlabel("Densité")
    plt.ylabel("Probabilité qu'un arbre brûle")
    plt.show(block=False)
    plt.pause(0.05)


def analyze_results(results):
    results["steps"] = np.mean(results["steps"])
    results["mean_tree_left"] = np.mean(results["tree_left"])
    results["perco_threshold"] = compute_perco_threshold(
        results["perco_coeff"], results["tree_left"])
    return results


def simulate(epochs=1, size=25, p_start=0, p_max=1, delta=0.05, gui=None, graphical_rendering=True):
    results = {"perco_coeff": [], "tree_left": [],
               "steps": [], "mean_tree_left": 0}
    clock = pygame.time.Clock()
    results["perco_coeff"] = []
    i = 0
    p = p_start
    max_iterations = epochs*((p_max - p_start)/delta)
    while p < p_max:
        results["tree_left"].append([])
        results["steps"].append([])
        for e in range(epochs):
            scene = Scene(p, size, render=graphical_rendering)
            done = False
            s = 0
            while done == False:
                if graphical_rendering:
                    clock.tick(10)
                    scene.drawMe()
                    pygame.display.flip()
                done = scene.update()
                s += 1
            results["steps"][i].append(s)
            results["tree_left"][i].append(
                scene._grid.get_trees_left()/(scene._grid.size**2))
            if gui is not None:
                if gui.OneLineProgressMeter('Simulation', i*epochs + e, max_iterations, 'key', 'Simulation in progress...') == False:
                    break
        results["perco_coeff"].append(p)
        results["tree_left"][i] = np.mean(results["tree_left"][i])
        results["steps"][i] = np.mean(results["steps"][i])
        p += delta
        i += 1
    if graphical_rendering:
        pygame.quit()
    return analyze_results(results)
