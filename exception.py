class TokenError(Exception):

    def __init__(self, line, lexeme):
        self.message = f'Token "{lexeme}" inválido, linha: {line}'
        super().__init__(self.message)

        