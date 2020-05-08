import random
import copy

# up, right, down, left, stay
movements = [[0, -1], [1, 0], [0, 1], [-1, 0], [0, 0]]
p_sensor = 0.6
ip_sensor = 1.0 - p_sensor


class Node:
    certainity: float

    def __init__(self, x, y, wall, sides, certainity):
        self.x = x
        self.y = y
        self.wall = wall
        self.sides = sides
        self.certainity = certainity

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for i in range(4):
            if not self.sides[i] == other.sides[i]:
                return False
        return True

    def __str__(self):
        if self.wall:
            symbol = "wall"
        else:
            symbol = "free"
        return "[" + str(self.x) + "," + str(self.y) + "], " + symbol + " " + str(self.certainity)


def makeGrid(filename, grid):
    file = open(filename)
    XY = str(file.readline()).split(" ")
    width = int(XY[0])
    height = int(XY[1])
    n_free_tiles = 0
    for x in range(width):
        grid.append([])
    for y in range(height):
        for x in range(width):
            grid[x].append(Node(x, y, file.read(1) == "X", [0, 0, 0, 0], 0.0))
            if not grid[x][y].wall:
                n_free_tiles += 1
        file.readline()
    uniform_probability = 1.0 / n_free_tiles
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if not grid[x][y].wall:
                grid[x][y].certainity = uniform_probability
            grid[x][y].sides[0] = 1 if grid[x][y - 1].wall else 0
            grid[x][y].sides[1] = 1 if grid[x + 1][y].wall else 0
            grid[x][y].sides[2] = 1 if grid[x][y + 1].wall else 0
            grid[x][y].sides[3] = 1 if grid[x - 1][y].wall else 0
    return width, height


def updateData(robot, grid):
    copy_grid = copy.deepcopy(grid)
    summation = 0.0
    for x in range(len(copy_grid)):
        for y in range(len(copy_grid[0])):
            copy_grid[x][y].certainity = 0.0
            if not grid[x][y].wall:
                match = 0
                if grid[x][y] == robot:
                    match = 1
                copy_grid[x][y].certainity = grid[x][y].certainity * (match * p_sensor + (1 - match) * ip_sensor)
            summation += copy_grid[x][y].certainity

    for x in range(len(copy_grid)):
        for y in range(len(copy_grid[0])):
            if not grid[x][y].wall:
                copy_grid[x][y].certainity /= summation
    robot = copy_grid[robot.x][robot.y]
    return robot, copy_grid


def moveRobot(robot, grid, movement):
    copy_grid = copy.deepcopy(grid)
    if grid[robot.x + movement[0]][robot.y + movement[1]].wall:
        print("Staying, cant move to wall", end=" ")
        movement = [0, 0]
    print("Move" + str(movement))
    for x in range(1, len(copy_grid) - 1):
        for y in range(1, len(copy_grid[0]) - 1):
            copy_grid[x + movement[0]][y + movement[1]].certainity = 0.0
            if not copy_grid[x + movement[0]][y + movement[1]].wall:
                copy_grid[x + movement[0]][y + movement[1]].certainity = grid[x][y].certainity
    robot = copy_grid[robot.x + movement[0]][robot.y + movement[1]]
    print("Robot [" + str(robot.x) + ", ", str(robot.y) + "]")
    return robot, copy_grid


def localize(robot, grid):
    flag = False
    while not flag:
        robot, grid = moveRobot(robot, grid, movements[random.randrange(4)])
        robot, grid = updateData(robot, grid)
        printGrid(grid)
        for x in range(1, len(grid) - 1):
            for y in range(1, len(grid[0]) - 1):
                if grid[x][y].certainity == 1.0:
                    flag = True
                    print("FOUND SOLUTION!!!")
                    print("ROBOT location: ", str(robot))
                    print("SOLUTION:       ", str(grid[x][y]))


def main():
    grid = []
    width, height = makeGrid("dataset/26.txt", grid)
    robot = grid[random.randrange(width)][random.randrange(height)]
    while robot.wall:
        robot = grid[random.randrange(width)][random.randrange(height)]
    print("ROBOT LOCATION START:[", robot.x, ", ", robot.y, "]")
    localize(robot, grid)


# position [8, 4]
# move [-1, 0]


def printGrid(grid):
    y_index = 0
    print(" ", end="")
    for i in range(len(grid)):
        print("", format(i, '02d'), " ", end="")
    print()
    for y in range(len(grid[0])):
        print(format(y_index, '02d'), end="")
        y_index += 1
        for x in range(len(grid)):
            if grid[x][y].wall:
                print("....", end=" ")
            else:
                print(("%.3f" % grid[x][y].certainity).lstrip("0"), end=" ")
        print()


if __name__ == '__main__':
    main()
