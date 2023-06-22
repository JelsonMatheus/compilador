from enum import Enum


class TokenType(Enum):
    IDENTIFICADOR = 'Identificador'
    DIGITO = 'Digito'
    PALAVRA_RESERVADA = 'Palavra Reservada'
    SIMBOLO = 'Símbolo'


class Token:
    """
    Classe para representar um token.
    """

    def __init__(self, lexeme:str, TokenType:TokenType):
        self.lexeme = lexeme
        self.TokenType = TokenType
    
    def __str__(self):
        return f'({self.lexeme}, {self.TokenType.name})'
