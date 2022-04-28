import df_maze
import random
import numpy as np

class Binary_Tree:

    def on(maze, dir_bias = 0.5, directions=['S','E']): # southeast

        for x in range(maze.nx):
            for y in range(maze.ny):
                neighbours = []
                current_cell = maze.cell_at(x,y)
                if current_cell.south is not None:
                    neighbours.append(('S',current_cell.south))
                if current_cell.east is not None:
                    neighbours.append(('E',current_cell.east))
                if len(neighbours) > 0:
                    direction, next_cell = random.choice(neighbours)
                    current_cell.knock_down_wall(next_cell, direction)
                
class Aldous_Broder:
    
    def find_valid_neighbours(cell, maze, find_all=False):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < maze.nx) and (0 <= y2 < maze.ny):
                neighbour = maze.cell_at(x2, y2)
                if find_all or neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
                    
        return neighbours
    
    @classmethod
    def on(cls, maze):
        n = maze.nx * maze.ny
        current_cell = maze.cell_at(maze.ix, maze.iy)
        nv = 1 # total number of visited cells
        
        while nv < n:
            neighbours = cls.find_valid_neighbours(current_cell, maze, find_all=True)
            
            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            if next_cell.has_all_walls(): # cell has not been visited
                current_cell.knock_down_wall(next_cell, direction) # link cell
                nv += 1
            
            current_cell = next_cell # move to next cell
            
            
class Recursive_Backtracker:

    def find_valid_neighbours(cell, maze, find_all=False):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < maze.nx) and (0 <= y2 < maze.ny):
                neighbour = maze.cell_at(x2, y2)
                if find_all or neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
                    
        return neighbours
    
    @classmethod
    def on(cls, maze):
        # Total number of cells.
        n = maze.nx * maze.ny
        cell_stack = []
        current_cell = maze.cell_at(maze.ix, maze.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = cls.find_valid_neighbours(current_cell, maze)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1
            

class Prims:
    
    def random_cell(maze):
        """ Returns a random cell in the grid """
        
        ix = np.random.randint(0, maze.nx)
        iy = np.random.randint(0, maze.ny)
        return maze.cell_at(ix,iy)
    
    def find_valid_neighbours(cell, maze, find_all=False):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < maze.nx) and (0 <= y2 < maze.ny):
                neighbour = maze.cell_at(x2, y2)
                if find_all or neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
                    
        return neighbours
    
    @classmethod
    def simplified_prims(cls, maze, start_at_center=False):
        active_stack = []
        
        if start_at_center:
             current_cell = maze.cell_at(int(maze.nx/2),int(maze.ny/2))
        else:
            current_cell = cls.random_cell(maze)
       
        active_stack.append(current_cell)
        print('Started at: ', current_cell.x, current_cell.y)
        
        while len(active_stack) > 0:
            current_cell = random.choice(active_stack)
            neighbours = cls.find_valid_neighbours(current_cell, maze)
            
            if not neighbours:
                active_stack.remove(current_cell)
            else:
                direction,neighbour = random.choice(neighbours)
                current_cell.knock_down_wall(neighbour, direction)
                active_stack.append(neighbour)
    
    @classmethod
    def true_prims(cls, maze, start_at_center=False):
        
        # initialize stack to keep track of active cells
        active_stack = []
        
        # initialize stack to keep track of the costs of active cells
        cost_stack = []
        
        # set the starting cell location
        if start_at_center:
             current_cell = maze.cell_at(int(maze.nx/2),int(maze.ny/2))
        else:
            current_cell = cls.random_cell(maze)
       
        active_stack.append(current_cell)
        
        # assign a random between 0 and 99 to each cell
        cost = np.random.randint(0,100,(maze.nx,maze.ny))
        cost_stack.append(cost[current_cell.x, current_cell.y])
        
        while len(active_stack)>0:
            # choose the lowest cost cell from the active set
            current_cell = active_stack[np.argmin(cost_stack)]
            neighbours = cls.find_valid_neighbours(current_cell,maze)
            
            if not neighbours:
                active_stack.remove(current_cell)
                cost_stack.pop(np.argmin(cost_stack))
                
            else:
                # choose the neighbor with the lowest cost
                direction, neighbour = neighbours[0]
                cost_min = cost[neighbour.x, neighbour.y]
                for i in range(1,len(neighbours)):
                    direction_t, neighbour_t = neighbours[i]
                    if cost[neighbour_t.x, neighbour_t.y] < cost_min:
                        cost_min = cost[neighbour_t.x, neighbour_t.y]
                        neighbour = neighbour_t
                        direction = direction_t
                        
                current_cell.knock_down_wall(neighbour, direction)
                active_stack.append(neighbour)
                cost_stack.append(cost_min)
                

class Kruskals:
    
    class State:
        def __init__(self, maze):
            self.maze = maze # shallow copy
            self.neighbours = []
            self.set_for_cell = {}
            self.cells_in_set = {}

            for x in range(self.maze.nx):
                for y in range(self.maze.ny):
                    cell = maze.cell_at(x,y)
                    self.set_for_cell[cell] = x*self.maze.nx+y
                    self.cells_in_set[x*self.maze.nx+y] = [cell]

                    if cell.south is not None:
                        self.neighbours.append([cell,cell.south,'S'])
                    if cell.east is not None:
                        self.neighbours.append([cell,cell.east,'E'])

        def can_merge(self, left_cell, right_cell):
            if self.set_for_cell[left_cell] != self.set_for_cell[right_cell]:
                return True
            else:
                return False

        def merge(self, left_cell, right_cell, direction):
            #  knockdown maze wall
            left_cell.knock_down_wall(right_cell, direction)
#             self.maze.maze_map[left_cell.x][left_cell.y] = left_cell
#             self.maze.maze_map[right_cell.x][right_cell.y] = right_cell
            
            winner = self.set_for_cell[left_cell]
            loser = self.set_for_cell[right_cell]
            losers = self.cells_in_set[loser]

            for l in losers:
                self.cells_in_set[winner].append(l)
                self.set_for_cell[l] = winner

            # remove the loser set
            self.cells_in_set.pop(loser)     
    
    @classmethod
    def on(cls, maze):
        state = Kruskals.State(maze)
        np.random.shuffle(state.neighbours)
        
        while len(state.neighbours) > 0:
            left_cell, right_cell, direction = state.neighbours.pop()
            if state.can_merge(left_cell, right_cell):
                state.merge(left_cell, right_cell, direction)