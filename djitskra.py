# class Djitskra is a class that implements the Djitskra algorithm
class Djitskra:
    def __init__(self, graph):
        self.graph = graph
        self.start = graph.start
        self.end = graph.end

        self.openSet = []
        self.closedSet = []

        self.openSet.append(self.start)
        self.current = self.start

        self.start.cost = 0
        self.count = 0

    def displayGrid(self, listcolorpairings=None):
        if listcolorpairings == None:
            listcolorpairings = [
                (self.openSet, "lightgreen"),
                (self.closedSet, "lightcoral"),
                ([self.current], "yellow"),
                ([self.start], "blue"),
                ([self.end], "green"),
            ]
        self.graph.draw(listcolorpairings)

        self.graph.save("djitskra", self.count)
        self.count += 1

    def run(self):
        self.displayGrid()

        while len(self.openSet) > 0:
            # get the cell with the lowest cost
            current = self.openSet[0]
            for cell in self.openSet:
                if cell.cost < current.cost:
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
                newCost = current.cost + dist

                # if new cost is less than neighbor cost, update neighbor cost and set neighbor parent to current
                if newCost < neighbor.cost:
                    neighbor.cost = newCost
                    neighbor.parent = current

                    # if neighbor is not in open set, add it
                    if neighbor not in self.openSet:
                        self.openSet.append(neighbor)

            self.displayGrid()

        # if we get here, we have found the shortest path
        self.path = []
        current = self.end
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
