import sys
from collections import deque
from PIL import Image, ImageDraw


class No:
    def __init__(self, estado, pai, acao):
        self.estado = estado
        self.pai = pai
        self.acao = acao


class Fronteira:
    def __init__(self, estrategia='pilha'):
        self.fronteira = []
        self.estrategia = estrategia

    def adicionar(self, no):
        if self.estrategia == 'pilha':
            self.fronteira.append(no)
        elif self.estrategia == 'fila':
            self.fronteira.appendleft(no)

    def contem_estado(self, estado):
        return any(no.estado == estado for no in self.fronteira)

    def vazia(self):
        return len(self.fronteira) == 0

    def remover(self):
        if self.vazia():
            raise Exception("fronteira vazia")
        if self.estrategia == 'pilha':
            no = self.fronteira.pop()
        elif self.estrategia == 'fila':
            no = self.fronteira.popleft()
        return no


class Labirinto:
    def __init__(self, arquivo):
        self.carregar_labirinto(arquivo)
        self.solucao = None

    def carregar_labirinto(self, arquivo):
        with open(arquivo) as f:
            conteudo = f.read()

        if conteudo.count("A") != 1 or conteudo.count("B") != 1:
            raise Exception("o labirinto deve ter exatamente um ponto de início (A) e um ponto de objetivo (B)")

        conteudo = conteudo.splitlines()
        self.altura = len(conteudo)
        self.largura = max(len(linha) for linha in conteudo)
        self.paredes = []

        for i, linha in enumerate(conteudo):
            linha_parede = []
            for j, char in enumerate(linha):
                if char == 'A':
                    self.inicio = (i, j)
                    linha_parede.append(False)
                elif char == 'B':
                    self.objetivo = (i, j)
                    linha_parede.append(False)
                elif char == ' ':
                    linha_parede.append(False)
                else:
                    linha_parede.append(True)
            self.paredes.append(linha_parede)

    def imprimir(self):
        solucao = self.solucao[1] if self.solucao else None
        for i, linha in enumerate(self.paredes):
            for j, coluna in enumerate(linha):
                if coluna:
                    print("█", end="")
                elif (i, j) == self.inicio:
                    print("A", end="")
                elif (i, j) == self.objetivo:
                    print("B", end="")
                elif solucao and (i, j) in solucao:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def vizinhos(self, estado):
        linha, coluna = estado
        candidatos = [
            ("cima", (linha - 1, coluna)),
            ("baixo", (linha + 1, coluna)),
            ("esquerda", (linha, coluna - 1)),
            ("direita", (linha, coluna + 1))
        ]
        resultado = [
            (acao, (r, c)) for acao, (r, c) in candidatos
            if 0 <= r < self.altura and 0 <= c < self.largura and not self.paredes[r][c]
        ]
        return resultado

    def resolver(self):
        self.qtd_explorados = 0
        no_inicio = No(estado=self.inicio, pai=None, acao=None)
        fronteira = Fronteira(estrategia='pilha')
        fronteira.adicionar(no_inicio)

        self.explorados = set()

        while True:
            if fronteira.vazia():
                raise Exception("sem solução")

            no = fronteira.remover()
            self.qtd_explorados += 1

            if no.estado == self.objetivo:
                acoes, celulas = self.reconstituir_solucao(no)
                self.solucao = (acoes, celulas)
                return

            self.explorados.add(no.estado)

            for acao, estado in self.vizinhos(no.estado):
                if not fronteira.contem_estado(estado) and estado not in self.explorados:
                    no_filho = No(estado=estado, pai=no, acao=acao)
                    fronteira.adicionar(no_filho)

    def reconstituir_solucao(self, no):
        acoes, celulas = [], []
        while no.pai is not None:
            acoes.append(no.acao)
            celulas.append(no.estado)
            no = no.pai
        acoes.reverse()
        celulas.reverse()
        return acoes, celulas

    def gerar_imagem(self, arquivo, mostrar_solucao=True, mostrar_explorados=False):
        tamanho_celula = 50
        borda_celula = 2
        img = Image.new("RGBA", (self.largura * tamanho_celula, self.altura * tamanho_celula), "black")
        draw = ImageDraw.Draw(img)

        solucao = self.solucao[1] if self.solucao else None
        for i, linha in enumerate(self.paredes):
            for j, coluna in enumerate(linha):
                if coluna:
                    preenchimento = (40, 40, 40)  # Parede
                elif (i, j) == self.inicio:
                    preenchimento = (255, 0, 0)  # Início
                elif (i, j) == self.objetivo:
                    preenchimento = (0, 171, 28)  # Objetivo
                elif solucao and mostrar_solucao and (i, j) in solucao:
                    preenchimento = (220, 235, 113)  # Caminho da solução
                elif solucao and mostrar_explorados and (i, j) in self.explorados:
                    preenchimento = (212, 97, 85)  # Caminho explorado
                else:
                    preenchimento = (237, 240, 252)  # Espaço vazio

                draw.rectangle(
                    [(j * tamanho_celula + borda_celula, i * tamanho_celula + borda_celula),
                     ((j + 1) * tamanho_celula - borda_celula, (i + 1) * tamanho_celula - borda_celula)],
                    fill=preenchimento
                )

        img.save(arquivo)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python labirinto.py labirinto.txt")

    arquivo_labirinto = sys.argv[1]
    labirinto = Labirinto(arquivo_labirinto)
    print("Labirinto:")
    labirinto.imprimir()
    print("Resolvendo...")
    labirinto.resolver()
    print(f"Estados explorados: {labirinto.qtd_explorados}")
    print("Solução:")
    labirinto.imprimir()
    labirinto.gerar_imagem("labirinto.png", mostrar_explorados=True)
