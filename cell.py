import math
from matplotlib import pyplot as plt

Width = 100
Height = 100


# class Cell for a cell in graph
class Cell:
    def __init__(self, x, y, cellName):
        self.x = x
        self.y = y
        self.cellName = cellName
        self.isObstacle = False

        self.parent = None
        self.neighbors = []

        self.cost = math.inf

    def draw(self, fig, ax, color=None):
        if self.isObstacle:
            color_background = "black"
            color_text = "white"
        else:
            color_background = "white"
            color_text = "black"
        color_border = "black"

        if color is None:
            color = color_background

        # clear axis
        ax.cla()

        # Image from plot
        ax.axis("off")
        fig.tight_layout(pad=0)

        # To remove the huge white borders
        ax.margins(0)

        # draw cell background
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=color))

        # draw cell border
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=color_border, fill=False))

        # draw cell text
        ax.text(
            0.5,
            0.7,
            str(self.cellName),
            ha="center",
            va="center",
            color=color_text,
            fontsize=80,
        )

        # draw cell distance
        if type(self.cost) == list:
            dist_txt = f"g: {self.cost[0]}\nf: {self.cost[1]}\nh: {self.cost[2]}"
        else:
            dist_txt = f"{self.cost}"
        ax.text(
            0.5,
            0.3,
            dist_txt,
            ha="center",
            va="center",
            color=color_text,
            fontsize=40,
        )

    def setName(self, name):
        self.cellName = name

    def setObstacle(self, isObstacle):
        self.isObstacle = isObstacle

    def addNeighbor(self, neighbor, weight):
        if neighbor not in self.neighbors and not neighbor.isObstacle:
            self.neighbors.append((neighbor, weight))


if __name__ == "__main__":
    cell = Cell(0, 0, "A")
    fig, ax = plt.subplots()
    fig.set_figwidth(5)
    fig.set_figheight(5)
    cell.cost = [1, 2, 3]
    cell.draw(fig, ax)
    plt.show()
