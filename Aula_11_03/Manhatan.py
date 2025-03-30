import heapq
import sys

class Node():
    def __init__(self, state, parent, action, cost, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost  # Custo acumulado até o momento
        self.heuristic = heuristic  # Heurística (distância de Manhattan)

    def __lt__(self, other):
        # Para comparação de nós na fila de prioridade
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class AStarFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        heapq.heappush(self.frontier, (node.cost + node.heuristic, node))  # Usando custo total para priorizar

    def contains_state(self, state):
        return any(node.state == state for _, node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            _, node = heapq.heappop(self.frontier)
            return node


class Maze():

    def __init__(self, filename):
        # Ler arquivo e definir altura e largura do labirinto
        with open(filename) as f:
            contents = f.read()

        # Validar ponto de início e objetivo
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Manter controle das paredes
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    # Função de distância de Manhattan
    def distancia_manhattan(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    # Função para imprimir o labirinto
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    # Função para pegar os vizinhos de um estado
    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))  # Corrigido para (row, col + 1)
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    # Função para resolver o labirinto usando A* com distância de Manhattan
    def solve(self):
        """Finds a solution to maze using A* with Manhattan distance."""

        # Número de estados explorados
        self.num_explored = 0

        # Inicializar o nó de partida
        start = Node(state=self.start, parent=None, action=None, cost=0, heuristic=self.distancia_manhattan(self.start))
        frontier = AStarFrontier()
        frontier.add(start)

        # Inicializar conjunto de explorados
        self.explored = set()

        # Loop até encontrar a solução
        while True:
            if frontier.empty():
                print("No solution. Frontier is empty.")
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            # Imprimir o estado atual para depuração
            print(f"Exploring: {node.state}")

            # Se o nó atual for o objetivo
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            # Adicionar vizinhos à fronteira
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    cost = node.cost + 1  # Custo é 1 para cada movimento
                    heuristic = self.distancia_manhattan(state)  # Heurística
                    child = Node(state=state, parent=node, action=action, cost=cost, heuristic=heuristic)
                    frontier.add(child)

    # Gerar imagem do labirinto
    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Criar uma tela em branco
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Desenhar paredes
                if col:
                    fill = (40, 40, 40)

                # Desenhar ponto de partida
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Desenhar objetivo
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Desenhar solução
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Desenhar explorados
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Células vazias
                else:
                    fill = (237, 240, 252)

                # Desenhar célula
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

# Rodar a resolução do labirinto
m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
