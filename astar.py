# class Astar is a class that implements the Astar algorithm
class Astar:
    def __init__(self, graph):
        self.graph = graph
        self.start = graph.start
        self.end = graph.end

        self.openSet = []
        self.closedSet = []

        self.openSet.append(self.start)
        self.current = self.start

        self.count = 0

    def getDistance(self, cell1, cell2):
        # manhattan distance
        dist = abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

        # euclidean distance
        # dist = math.sqrt((cell1.x - cell2.x) ** 2 + (cell1.y - cell2.y) ** 2)

        return dist

    def displayGrid(self, listcolorpairings=None):
        if listcolorpairings == None:
            listcolorpairings = [
                ([self.current], "yellow"),
                (self.openSet, "lightgreen"),
                (self.closedSet, "lightcoral"),
                ([self.start], "blue"),
                ([self.end], "green"),
            ]
        self.graph.draw(listcolorpairings)

        self.graph.save("astar", self.count)
        self.count += 1

    def run(self):
        # set the cost of the start cell to 0
        self.start.cost = [
            self.getDistance(self.start, self.end),
            0,
            self.getDistance(self.start, self.end),
        ]
        self.displayGrid()

        while len(self.openSet) > 0:
            # get the cell with the lowest cost
            current = self.openSet[0]
            for cell in self.openSet:
                if cell.cost[0] < current.cost[0]:
                    current = cell

            # if the current cell is the end cell, we are done
            if current == self.end:
                break

            # remove current cell from open set and add to closed set
            self.openSet.remove(current)
            self.closedSet.append(current)

            self.current = current

            # loop through neighbors of current cell
            for neighbor, dist in current.neighbors:
                # if neighbor is in closed set, skip
                if neighbor in self.closedSet:
                    continue

                # calculate new cost to neighbor
                f_cost = current.cost[1] + dist
                h_cost = self.getDistance(neighbor, self.end)
                g_cost = f_cost + h_cost
                newCost = [g_cost, f_cost, h_cost]

                if type(neighbor.cost) == list:
                    neighbor_g_cost = neighbor.cost[0]
                else:
                    neighbor_g_cost = neighbor.cost

                # if new cost is less than neighbor cost, update neighbor cost and set neighbor parent to current
                if newCost[0] < neighbor_g_cost:
                    neighbor.cost = newCost
                    neighbor.parent = current

                    # if neighbor is not in open set, add it
                    if neighbor not in self.openSet:
                        self.openSet.append(neighbor)

            self.displayGrid()

        # if we get here, we have found the shortest path
        self.path = []
        current = self.end

        if current.parent == None:
            print("No path found")
            return

        while current != None:
            self.path.append(current)
            current = current.parent

        self.path.reverse()

        # draw the path
        listcolorpairings = [
            ([self.start], "blue"),
            ([self.end], "green"),
            (self.path, "cyan"),
        ]
        self.displayGrid(listcolorpairings)
