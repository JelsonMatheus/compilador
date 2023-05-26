from enum import Enum


class TypeToken(Enum):
    IDENTIFICADOR = 'Identificador'
    DIGITO = 'Digito'
    PALAVRA_RESERVADA = 'Palavra Reservada'
    SIMBOLO = 'Símbolo'


class Token:

    def __init__(self, lexeme:str, typetoken:TypeToken):
        self.lexeme = lexeme
        self.typetoken = typetoken
    
    def __str__(self):
        return f'({self.lexeme}, {self.typetoken.name})'
