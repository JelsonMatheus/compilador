class TokenError(Exception):
    """
    Classe de exceção para representar erros relacionados a tokens inválidos.
    """

    def __init__(self, line, lexeme):
        self.message = f'Token "{lexeme}" inválido, linha: {line}'
        super().__init__(self.message)

        