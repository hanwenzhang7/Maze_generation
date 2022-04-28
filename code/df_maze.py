import random
import numpy as np


# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/
# Christian Hill, April 2017.

class Cell:
    """A cell in the maze.
    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.
    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        
        # attributes to acess the cell's immediate neighbours
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (ix, iy).
        """

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        
        # prepare grid
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]
        
        # configure cells
        for x in range(nx):
            for y in range(ny):
                cell = self.cell_at(x,y)
                cell.north = self.cell_at(x,y-1)
                cell.south = self.cell_at(x,y+1)
                cell.west = self.cell_at(x-1,y)
                cell.east = self.cell_at(x+1,y)

        self.add_begin_end = False
        self.add_treasure = False
        self.treasure_x = random.randint(0, self.nx-1)
        self.treasure_y = random.randint(0, self.ny-1)
        
    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""
        if (0<=x<=self.nx-1)&(0<=y<=self.ny-1):
            return self.maze_map[x][y]
        else:
            return None

    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['--' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append('   |')
                else:
                    maze_row.append('    ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('---+')
                else:
                    maze_row.append('   +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)
      
    def write_svg(self, filename):
        """Write an SVG image of the maze to filename."""

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
            """Write a single wall to the SVG image file handle f."""

            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

        def add_cell_rect(f, x, y, colour):
            pad = 5
            print(f'<rect x="{scx*x+pad}" y="{scy*y+pad}" width="{scx-2*pad}"'
                  f' height="{scy-2*pad}" style="fill:{colour}" />', file=f) 

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)

            if self.add_begin_end:
                add_cell_rect(f, 0, 0, 'green')
                add_cell_rect(f, self.nx - 1, self.ny - 1, 'red')
            if self.add_treasure:
                add_cell_rect(f, self.treasure_x, self.treasure_y, 'yellow')

            print('</svg>', file=f)