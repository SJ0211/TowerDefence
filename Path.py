import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement



def setGrid(matrix):
    global path
    path = []
    grid = Grid(matrix = matrix)
    return grid




def create_path(grid):
    global path
    path = []

    # start
    start_x, start_y = 1, 1
    start = grid.node(start_x, start_y)

    # end
    mouse_pos = pygame.mouse.get_pos()
    end_x, end_y = 20, 12
        #20, 12
    end = grid.node(end_x, end_y)


    # path
    finder = AStarFinder(diagonal_movement = DiagonalMovement.never)
    path,_ = finder.find_path(start, end, grid)
    grid.cleanup()



    return path


def draw_path(screen):
    global path
    if path:
        points = []
        for point in path:
            x = (point[0] * 60) + 30
            y = (point[1] * 60) + 30
            points.append((x, y))

        pygame.draw.lines(screen, '#4a4a4a', False, points, 5)

def create_collision_rects(path):
    if path:
        collision_rects = []
        for point in path:
            x = (point[0] * 60) - 30
            y = (point[1] * 60) - 30
            rect = pygame.Rect((x - 4, y - 4), (8, 8))
            collision_rects.append(rect)
        return collision_rects

def find_path(matrix):
    #for i in matrix:
        #print(str(i) + "\n")
    grid = setGrid(matrix)
    path = create_path(grid)

    collision_rects = create_collision_rects(path)

    return collision_rects

def draw_path(matrix, screen):
    grid = setGrid(matrix)
    path = create_path(grid)
    if path:
        points = []
        for point in path:
            x = (point[0] * 60) - 30
            y = (point[1] * 60) - 30
            points.append((x,y))

        pygame.draw.lines(screen,'#4a4a4a',False,points,5)










