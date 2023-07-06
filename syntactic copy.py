from lexicon import Lexicon
from exception import SyntacticError
from error_messages import ERROR_MESSAGES
from util import TokenType


class Syntactic:

    def __init__(self, filename):
        self.lexicon = Lexicon(filename)
    
    def start(self):
        token = self.lexicon.next_token()
        if token.lexeme != 'program':
            raise SyntacticError(self.lexicon.line, ERROR_MESSAGES[1])
        
        self.check_identifier()
        self.check_terminal(';')
        self.block()
    
    def block(self):
        token = self.lexicon.next_token()
        if token == 'type':
            self.definition_types()
    
    def definition_types(self):
        self.check_identifier()
        self.check_terminal('=')
        self.check_type()
        self.check_terminal(';')

        token = self.check_identifier(raise_error=False)
        while token:
            pass

        
        self.check_identifier()
        self.check_terminal('=')
        self.check_terminal(';')

        self.check_identifier()
        self.check_terminal('=')
        self.check_terminal(';')


    def check_terminal(self, terminal):
        token = self.lexicon.next_token()
        if not token or token.lexeme != terminal:
            raise SyntacticError(
                self.lexicon.line, 
                ERROR_MESSAGES[0].format(terminal)
            )
        return token

    def check_identifier(self, raise_error=true):
        token = self.lexicon.next_token()
        if not token or token.TokenType != TokenType.IDENTIFICADOR:
            if raise_error:
                raise SyntacticError(self.lexicon.line, ERROR_MESSAGES[2])
            return None
        return token
    
    def check_type():
        keywords = ['integer', 'boolean', 'double', 'char']
        token = self.lexicon.next_token()
        if not token or (token.TokenType != TokenType.IDENTIFICADOR 
                     or token.lexeme not in keywords):
            raise SyntacticError(self.lexicon.line, ERROR_MESSAGES[2])
        return token
        


