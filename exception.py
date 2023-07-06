class TokenError(Exception):
    """
    Classe de exceção para representar erros relacionados a tokens inválidos.
    """
    def __init__(self, line, lexeme):
        self.message = f'Token "{lexeme}" inválido, linha: {line}'
        super().__init__(self.message)

        
class SyntacticError(Exception):
    """
    Classe de exceção para representar erros sintaxe.
    """
    def __init__(self, line, msg):
        self.message = f'Linha {line}, {msg}'
        super().__init__(self.message)
