class TokenException(Exception):

    def __init__(self, linha, lexema):
        self.message = f'Token "{lexema}" inválido, linha: {linha}'
        super().__init__(self.message)

        