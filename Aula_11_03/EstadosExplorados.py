from collections import deque

labirinto = [
    "****************************************",
    "*A       ******  ******      ******    *",
    "*  ****  *               **           **",
    "*       *****  ******  *  *****  ****** ",
    "****  *        *       *  *             ",
    "*    ******  *****  *****  *****  ******",
    "*  *                *        *        * ",
    "*  *****  ******  *****  ** *****  *****",
    "*       *          *      *         *  B*",
    "****************************************"
]

"""

labirinto = [
    "##    #",
    "## ## #",
    "#B #  #",
    "# ## ##",
    "     ##",
    "A######"
]

"""

labirinto = [list(linha) for linha in labirinto]

def encontrar_posicao(caractere):
    for i, linha in enumerate(labirinto):
        for j, cel in enumerate(linha):
            if cel == caractere:
                return (i, j)
    return None

inicio = encontrar_posicao("A")
fim = encontrar_posicao("B")

movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def bfs(lab, inicio, fim):
    fila = deque([inicio])
    visitados = set()
    visitados.add(inicio)
    estados_explorados = 0

    while fila:
        x, y = fila.popleft()
        estados_explorados += 1
        if (x, y) == fim:
            return estados_explorados
        
        for dx, dy in movimentos:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(lab)) and (0 <= ny < len(lab[0])) and lab[nx][ny] != "*" and (nx, ny) not in visitados:
                fila.append((nx, ny))
                visitados.add((nx, ny))
    
    return estados_explorados

def dfs(lab, inicio, fim):
    pilha = [inicio]
    visitados = set()
    visitados.add(inicio)
    estados_explorados = 0

    while pilha:
        x, y = pilha.pop()
        estados_explorados += 1
        if (x, y) == fim:
            return estados_explorados
        
        for dx, dy in movimentos:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(lab)) and (0 <= ny < len(lab[0])) and lab[nx][ny] != "*" and (nx, ny) not in visitados:
                pilha.append((nx, ny))
                visitados.add((nx, ny))
    
    return estados_explorados

bfs_estados = bfs(labirinto, inicio, fim)
dfs_estados = dfs(labirinto, inicio, fim)

print(f"Estados explorados no BFS: {bfs_estados}")
print(f"Estados explorados no DFS: {dfs_estados}")


