class Palavra:
    def __init__(self, nome, inicio, fim):
        self.nome = nome
        self.inicio = inicio
        self.fim = fim

    def __str__(self):
        return f'{{"nome": "{self.nome}", "inicio": {self.inicio}, "fim": {self.fim}}}'

    def __repr__(self):
        return self.__str__()  # ou versão mais técnica

    def __lt__(self, other):
        return (self.inicio[0] < other.inicio[0]) or (self.inicio[0] == other.inicio[0] and self.inicio[1] < other.inicio[1])

    def __gt__(self, other):
        return (self.inicio[0] > other.inicio[0]) or (self.inicio[0] == other.inicio[0] and self.inicio[1] > other.inicio[1])

    def __eq__(self, other):
        if type(other) is str:
            return self.nome == other
        elif type(other) is tuple:
            return self.nome == other[0]
        else:
            return self.nome == other.nome