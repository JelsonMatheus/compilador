from automatos import Automato
from exception import TokenException


class Lexico:

    def __init__(self, nome_arquivo):
        with open(nome_arquivo) as f:
            self.entrada = f.read()
            self.automato = Automato(self.entrada, 0, 1)

    def ler_token(self):
        try:
            token = self.automato.processar()
            return token
        except TokenException as error:
            print(error)