from cell import Cell

from matplotlib import pyplot as plt
import numpy as np
import io

CellWidth = 3
CellHeight = 3

GridWidth = 20
GridHeight = 20

plt.ion()


# class Grid for the graph data structure
class Grid:
    def __init__(self, width, height):
        self.cells = []
        self.width = width
        self.height = height

        self.start = None
        self.end = None

        self.fig = plt.figure()
        self.fig.set_figwidth(GridWidth)
        self.fig.set_figheight(GridHeight)
        self.ax = self.fig.gca()
        self.fig.show()

        self.tempfig = plt.figure()
        self.tempfig.set_figwidth(CellWidth)
        self.tempfig.set_figheight(CellHeight)
        self.tempaxis = self.tempfig.gca()
        self.tempfig.show()

        self.resolution = self.tempfig.canvas.get_width_height()
        self.grid = np.zeros(
            (self.height * self.resolution[1], self.width * self.resolution[0], 3),
            dtype=np.uint8,
        )

    def createGraph(self, inputGraph, weights):
        if len(inputGraph) != self.height or len(inputGraph[0]) != self.width:
            raise Exception("Input graph dimensions do not match grid dimensions")

        # loop through the 2d array of cells
        for r, row in enumerate(inputGraph):
            for c, cell in enumerate(row):
                # create cell
                newCell = Cell(c, r, f"{c+r*len(row)}")

                # set cell as obstacle if cell == 1
                if cell == 1:
                    newCell.setObstacle(True)

                # add cell to graph
                self.cells.append(newCell)

        # set weights
        straight = weights[0]
        diagonal = weights[1]

        # add the neighbours to each cell
        for itr, cell in enumerate(self.cells):
            # add 8 connected neighbours
            # top left
            if itr - self.width - 1 >= 0 and itr % self.width != 0:
                cell.addNeighbor(self.cells[itr - self.width - 1], diagonal)
            # top
            if itr - self.width >= 0:
                cell.addNeighbor(self.cells[itr - self.width], straight)
            # top right
            if itr - self.width + 1 >= 0 and itr % self.width != self.width - 1:
                cell.addNeighbor(self.cells[itr - self.width + 1], diagonal)
            # left
            if itr - 1 >= 0 and itr % self.width != 0:
                cell.addNeighbor(self.cells[itr - 1], straight)
            # right
            if itr + 1 < len(self.cells) and itr % self.width != self.width - 1:
                cell.addNeighbor(self.cells[itr + 1], straight)
            # bottom left
            if itr + self.width - 1 < len(self.cells) and itr % self.width != 0:
                cell.addNeighbor(self.cells[itr + self.width - 1], diagonal)
            # bottom
            if itr + self.width < len(self.cells):
                cell.addNeighbor(self.cells[itr + self.width], straight)
            # bottom right
            if (
                itr + self.width + 1 < len(self.cells)
                and itr % self.width != self.width - 1
            ):
                cell.addNeighbor(self.cells[itr + self.width + 1], diagonal)

    def draw(self, listcolorpairings=[]):
        # draw cells
        for cell in self.cells:
            bg_color = None
            # set the color of the cell
            for cellList, color in listcolorpairings:
                if cell in cellList:
                    bg_color = color
                    break

            cell.draw(self.tempfig, self.tempaxis, bg_color)

            # convert the plot to an image
            self.tempfig.canvas.draw()
            image_from_plot = np.frombuffer(
                self.tempfig.canvas.tostring_rgb(), dtype=np.uint8
            )
            image_from_plot = image_from_plot.reshape(
                self.tempfig.canvas.get_width_height()[::-1] + (3,)
            )

            # get the pixel coordinates of the cell
            x = cell.x * self.resolution[1]
            y = cell.y * self.resolution[0]

            # draw the cell on the grid
            self.grid[
                y : y + self.resolution[0], x : x + self.resolution[1]
            ] = image_from_plot

        # draw grid lines
        for x in range(0, self.width * self.resolution[1], self.resolution[1]):
            self.grid[:, x : x + 1] = 0
        for y in range(0, self.height * self.resolution[0], self.resolution[0]):
            self.grid[y : y + 1, :] = 0

        # draw the grid borders
        self.grid[0, :] = 0
        self.grid[:, 0] = 0
        self.grid[-1, :] = 0
        self.grid[:, -1] = 0

        self.ax.clear()
        self.ax.imshow(self.grid)
        self.ax.axis("off")
        self.fig.tight_layout(pad=0)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def getCell(self, x, y):
        return self.cells[x + y * self.width]

    def setStartandEnd(self, start, end):
        self.start = self.getCell(start[0], start[1])
        self.end = self.getCell(end[0], end[1])

        self.start.setName("Start")
        self.end.setName("End")

    def save(self, algorithmName, count):
        self.fig.savefig(f"{algorithmName}/{algorithmName}_{count}.jpg")


if __name__ == "__main__":
    grid = Grid(8, 6)
    grid.createGraph(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        [1, 1.5],
    )
    grid.draw()

    # wait for user input
    input("Press Enter to continue...")
