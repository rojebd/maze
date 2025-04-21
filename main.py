# Author: rojebd@github

# Resources:
#   https://professor-l.github.io/mazes/
#   https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_implementation

# This is a reference implementation in python. Since I am most comformatable
# with it. Though you can probably just translate this to any given programming
# language.

import random

class Cell:
    # By default the connections list being empty means the cell has "walls"
    # all around it.

    # format for the items inside the connection list, tuple with 2 items.
    #    ("up|down|left|right", Cell Object)

    def __init__(self, visited, x, y):
        self.visited: bool = visited
        self.x: int = x
        self.y: int = y
        self.connections = []

    def add_connection(self, direction, cell):

        # I had a bug that meant that sometimes you had duplicate connections
        # for some reason. Instead of finding the source, I just make sure we
        # don't insert a duplicate connection. It actually does not take long
        # because for any given cell it can only have 4 connections, (up, down, left, right)

        # TODO: Determine whether this is a good fix or a hack?
        for connection in self.connections:
            if connection == (direction, cell):
                return
        
        self.connections.append((direction, cell))

    def __str__(self):
        # For print debugging
        string = f"Cell: {self.y}:{self.x}, Visited:{self.visited}, Connections: {self.dump_connections()}"
        return string

    def dump_connections(self):
        # For print debugging the connections in __str__
        connections_str = ""

        for cell in self.connections:
            connections_str += f"('{cell[0]}', {cell[1].y}:{cell[1].x}) "
        connections_str = connections_str[:-1]
        return connections_str
        
class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.__generate_starting_grid(rows, cols)
        self.start_cell = self.grid[0][0]
        # Grid starts at 0th index so we do - 1 to avoid an off by one error.
        self.end_cell = self.grid[self.rows - 1][self.cols - 1]
        
    def generate(self):
        current_cell = self.grid[0][0]
        self.__generate(current_cell)

    def __generate(self, current_cell):
        current_cell.visited = True
        while self.has_unvisited_neighbors(current_cell):
            neighbor_cell = self.choose_random_neighbor(current_cell)
            self.remove_wall(current_cell, neighbor_cell)
            self.__generate(neighbor_cell[1])

    def remove_wall(self, current_cell, neighbor_cell):
        current_cell.add_connection(neighbor_cell[0], neighbor_cell[1])

    def choose_random_neighbor(self, cell):
        up = ("up", self.grid[(cell.y - 1) % self.rows][cell.x])
        down = ("down", self.grid[(cell.y + 1) % self.rows][cell.x])
        left = ("left", self.grid[cell.y][(cell.x - 1) % self.cols])
        right = ("right", self.grid[cell.y][(cell.x + 1) % self.cols])

        return random.choice([up, down, left, right])

    def has_unvisited_neighbors(self, cell):
        # maybe just wrap it around?
        neighbors = []
        up = self.grid[(cell.y - 1) % self.rows][cell.x]
        down = self.grid[(cell.y + 1) % self.rows][cell.x]
        left = self.grid[cell.y][(cell.x - 1) % self.cols]
        right = self.grid[cell.y][(cell.x + 1) % self.cols]

        neighbors.append(up)
        neighbors.append(down)
        neighbors.append(left)
        neighbors.append(right)

        for cell in neighbors:
            if cell.visited == False:
                return True
            

    def __generate_starting_grid(self, rows, cols):
        grid = []

        for row in range(rows):
            current_row = []
            for col in range(cols):
                cell = Cell(visited = False, x=col, y=row)
                current_row.append(cell)
            grid.append(current_row)

        return grid

    def dump(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.grid[i][j])

# TODO Missing a render method for visualizing.
                
m = Maze(3, 3)
m.generate()
m.dump()
# remove duplicate connections at the end.
