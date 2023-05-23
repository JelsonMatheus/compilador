from automatos import Automato
from exception import TokenException


class Lexico:

    def __init__(self, nome_arquivo):
        self.linha = 1
        self.posicao = 0
        with open(nome_arquivo) as f:
            self.entrada = f.read()
    
    def ler_token(self):
        automato = Automato(self.entrada, self.posicao, self.linha)
        try:
            token = automato.processar()
            self.linha = automato.linha
            self.posicao = automato.posicao
            return token
        except TokenException as error:
            print(error)