from util import Token, TipoToken
from exception import TokenException


TERMINAIS = ['\n', ' ']
EOF = '\0'


def terminal(char):    
    return char in (TERMINAIS + [EOF])


class Automato:

    def __init__(self, entrada, posicao, linha):
        self.entrada = entrada
        self.posicao = posicao
        self.linha = linha
        self.token = None

    def processar(self):
        self.q0(lexema='')
        return self.token
    
    def q0(self, lexema):
        char = self.proximo_caractere()
        lexema += char
        if char.isalpha():
            self.q1(lexema)
        elif char in TERMINAIS:
            self.q0('')
        elif char != EOF:
           raise TokenException(self.linha, lexema)

    def q1(self, lexema):
        char = self.proximo_caractere()
        lexema += char
        if char.isalpha() or char.isdigit():
            self.q2(lexema)
        elif char == '.':
            self.q3(lexema)
        elif char == '_':
            self.q4(lexema)
        else:
            self.token = Token(lexema[:-1], TipoToken.IDENTIFICADOR)
    
    def q2(self, lexema):
        char = self.proximo_caractere()
        lexema += char
        if char.isalpha() or char.isdigit():
            self.q2(lexema)
        else:
            self.token = Token(lexema[:-1], TipoToken.IDENTIFICADOR)
    
    def _q3(self, lexema):
        char = self.proximo_caractere()
        lexema += char
        if char.isalpha() or char.isdigit():
            self.q2(lexema)
        else:
           raise TokenException(self.linha, lexema)
    
    def q4(self, lexema):
        char = self.proximo_caractere()
        lexema += char
        if char.isalpha() or char.isdigit():
            self.q5(lexema)
        else:
            raise TokenException(self.linha, lexema)
    
    def q5(self, lexema):
        char = self.proximo_caractere()
        lexema += char
        if char.isalpha() or char.isdigit():
            self.q5(lexema)
        elif char == '.':
            self.q3(lexema)
        else:
            self.token = Token(lexema[:-1], TipoToken.IDENTIFICADOR)


    def proximo_caractere(self) -> str:
        char = EOF
        if self.posicao < len(self.entrada):
            char = self.entrada[self.posicao]
            self.posicao += 1
            if char == '\n':
                self.linha += 1
        return char

