from graph import Grid
from djitskra import Djitskra
from astar import Astar

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
        [1, 1],
    )
    grid.setStartandEnd([0, 5], [7, 0])
    grid.draw()

    # wait for user input
    input("Press Enter to continue...")

    # dj = Djitskra(grid)
    # dj.run()

    astar = Astar(grid)
    astar.run()
