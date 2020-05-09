import random
import copy
import statistics
import sys
import time

# up, right, down, left, stay
movements = [[0, -1], [1, 0], [0, 1], [-1, 0], [0, 0]]
p_sensor = 1
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


def main():
    begin_time = time.time()
    print_option = True
    loops = 1
    if len(sys.argv) == 4:
        print_option = False
        loops = int(sys.argv[3])
    if len(sys.argv) == 3:
        loops = int(sys.argv[2])
    original_grid = []
    width, height = makeGrid(sys.argv[1], original_grid)
    steps = []
    duration = []
    for i in range(loops):
        grid = copy.deepcopy(original_grid)
        robot = grid[random.randrange(width)][random.randrange(height)]
        while robot.wall:
            robot = grid[random.randrange(width)][random.randrange(height)]
        result = localize(robot, grid, print_option)
        steps.append(result[0])
        duration.append(result[1])
    print("FINISH")
    print("Iterations: ", loops)
    print("Map size (width height): ", width, height)
    print("Mean of steps: ", statistics.mean(steps))
    print("Mean of time per iteration: ", statistics.mean(duration))
    print("Median of steps: ", statistics.median(steps))
    print("Median of time per iteration: ", statistics.median(duration))
    print("Total elapsed time: ", time.time() - begin_time)


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


def updateData(robot, grid):
    summation = 0.0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if not grid[x][y].wall:
                match = 0
                if grid[x][y] == robot:
                    match = 1
                grid[x][y].certainity = grid[x][y].certainity * (match * p_sensor + (1 - match) * ip_sensor)
            else:
                grid[x][y].certainity = 0.0
            summation += grid[x][y].certainity
    adept = grid[1][1]
    robot = grid[robot.x][robot.y]
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if not grid[x][y].wall:
                grid[x][y].certainity /= summation
                if grid[x][y].certainity > adept.certainity:
                    adept = grid[x][y]
                if grid[x][y].certainity > 0.99:
                    return robot, grid, [0, 0], True, grid[x][y]
    i = random.randrange(4)
    while adept.sides[i] == 1:
        i = random.randrange(4)
    return robot, grid, movements[i], False, grid[0][0]


def moveRobot(robot, grid, movement, printing_option):
    copy_grid = copy.deepcopy(grid)
    if printing_option:
        print("Move" + str(movement))
    for x in range(1, len(copy_grid) - 1):
        for y in range(1, len(copy_grid[0]) - 1):
            copy_grid[x + movement[0]][y + movement[1]].certainity = 0.0
            if not copy_grid[x + movement[0]][y + movement[1]].wall:
                copy_grid[x + movement[0]][y + movement[1]].certainity = grid[x][y].certainity
    robot = copy_grid[robot.x + movement[0]][robot.y + movement[1]]
    if printing_option:
        print("Robot [" + str(robot.x) + ", ", str(robot.y) + "]")
    return robot, copy_grid


def localize(robot, grid, printing_option):
    start_time = time.time()
    if printing_option:
        print("ROBOT LOCATION START:[", robot.x, ", ", robot.y, "]")
    flag = False
    steps = 0
    robot, grid, next_move, found_solution, location = updateData(robot, grid)
    while not flag:
        robot, grid = moveRobot(robot, grid, next_move, printing_option)
        robot, grid, next_move, found_solution, location = updateData(robot, grid)
        steps += 1
        if printing_option:
            printGrid(grid)
        if found_solution:
            duration = time.time() - start_time
            if printing_option:
                print("FOUND SOLUTION!!!")
                print("ROBOT location: ", str(robot))
                print("SOLUTION:       ", str(location))
                print("STEPS:          ", str(steps))
                print("TIME:           ", duration)
            else:
                print(steps, duration, str(robot), str(location))
            sys.stdout.flush()
            return steps, duration


if __name__ == '__main__':
    main()
