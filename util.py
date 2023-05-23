from enum import Enum


class TipoToken(Enum):
    IDENTIFICADOR = 'Identificador'


class Token:

    def __init__(self, valor:str, tipo:TipoToken):
        self.valor = valor
        self.tipo = tipo
    
    def __str__(self):
        return f'({self.valor}, {self.tipo.name})'
