import heapq

class Node:
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Maze:
    def __init__(self, filename):
        self.maze = []
        self.start = None
        self.end = None
        self.load_maze(filename)

    def load_maze(self, filename):
        with open(filename, 'r') as f:
            self.maze = [list(line.strip()) for line in f]
            for i in range(len(self.maze)):
                for j in range(len(self.maze[i])):
                    if self.maze[i][j] == 'A':
                        self.start = (i, j)
                    elif self.maze[i][j] == 'B':
                        self.end = (i, j)

    def heuristic(self, x, y):
        return abs(x - self.end[0]) + abs(y - self.end[1])

    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] != '█':
                neighbors.append((nx, ny))
        return neighbors

    def solve(self):
        open_list = []
        closed_list = set()

        start_x, start_y = self.start
        end_x, end_y = self.end

        start_node = Node(start_x, start_y, 0, self.heuristic(start_x, start_y))
        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)

            if (current_node.x, current_node.y) == self.end:
                self.reconstruct_path(current_node)
                return

            closed_list.add((current_node.x, current_node.y))

            for nx, ny in self.get_neighbors(current_node.x, current_node.y):
                if (nx, ny) in closed_list:
                    continue

                g = current_node.g + 1
                h = self.heuristic(nx, ny)
                neighbor_node = Node(nx, ny, g, h, current_node)

                # Verifique se o nó já está na open_list com custo menor
                if not any(neighbor_node == n and neighbor_node.f >= n.f for n in open_list):
                    heapq.heappush(open_list, neighbor_node)

        raise Exception("No solution found")

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append((node.x, node.y))
            node = node.parent
        path.reverse()

        for x, y in path:
            if self.maze[x][y] != 'A' and self.maze[x][y] != 'B':
                self.maze[x][y] = '*'

        self.print_maze()

    def print_maze(self):
        for row in self.maze:
            print(''.join(row))


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python maze.py maze.txt")
        sys.exit(1)

    m = Maze(sys.argv[1])
    print("Maze:")
    m.print_maze()
    print("\nSolving...")
    m.solve()
