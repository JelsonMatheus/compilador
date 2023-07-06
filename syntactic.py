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
            self.syntactic_error(token, ERROR_MESSAGES[1])
        
        self.check_identifier()
        self.check_terminal(';')
        self.block()
    
    def block(self):
        token = self.lexicon.next_token()
        if token and token.lexeme == 'type':
            token = self.definition_types()
        if token and token.lexeme == 'var':
            token = self.definition_variables()
        if token and token.lexeme in ('procedure', 'function'):
            token = self.definition_subroutines(token)
        if token and token.lexeme == 'begin':
            self.composite_command()
        else:
            self.syntactic_error(token, ERROR_MESSAGES[8])
        
    def definition_types(self):
        self.check_identifier()
        self.check_terminal('=')
        self.check_type()
        self.check_terminal(';')

        token = self.lexicon.next_token()
        while self.is_identifier(token):
            self.check_terminal('=')
            self.check_type()
            self.check_terminal(';')
            token = self.lexicon.next_token()
        return token
    
    def definition_variables(self):
        token = self.list_identifier()
        if not self.is_terminal(token, ':'):
            self.syntactic_error(token, ERROR_MESSAGES[4])

        self.check_type()
        self.check_terminal(';')

        token = self.lexicon.next_token()
        while self.is_identifier(token):
            self.list_identifier(token)
            self.check_terminal(':')
            self.check_type()
            self.check_terminal(';')
            token = self.lexicon.next_token()
        return token

    def definition_subroutines(self, token):
        while (token and token.lexeme in ('procedure', 'function')):
            if token.lexeme == 'procedure':
                self.definition_procedure()
            elif token.lexeme == 'function':
                self.definition_function()
            token = self.lexicon.next_token()
        return token

    def definition_procedure(self):
        self.check_identifier(msg=ERROR_MESSAGES[6])
        token = self.lexicon.next_token()
        if self.is_terminal(token, '('):
            self.formal_parameters()
            token = self.lexicon.next_token()
        if not self.is_terminal(token, ';'):
            msg = ERROR_MESSAGES[0].format(';')
            self.syntactic_error(token, msg)
        self.block()
    
    def definition_function(self):
        self.check_identifier()
        token = self.lexicon.next_token()
        if self.is_terminal(token, '('):
            self.formal_parameters()
        elif not self.is_terminal(token, ':'):
            msg = ERROR_MESSAGES[0].format(':')
            self.syntactic_error(token, msg)
        self.check_terminal(':')
        self.check_identifier()
        self.block()
    
    def composite_command(self):
        token = self.lexicon.next_token()
        token = self.unlabeled_command(token)
        msg = ERROR_MESSAGES[0].format(';')

        if not self.is_terminal(token, ';'):
            self.syntactic_error(token, msg)
        
        token = self.lexicon.next_token()
        while self.is_unlabeled_command(token):
            token = self.unlabeled_command(token)
            if not self.is_terminal(token, ';'):
                self.syntactic_error(token, msg)
            token = self.lexicon.next_token()
        
        if not self.is_terminal(token, 'end'):
            self.syntactic_error(token, ERROR_MESSAGES[0].format('end'))

    def unlabeled_command(self, token):
        if self.is_identifier(token):
            token = self.lexicon.next_token()
            if self.is_terminal(token, ':='):
                token = self.assignment()
            elif self.is_terminal(token, '('):
                self.procedure_call(token)
                token = self.lexicon.next_token()
        elif self.is_terminal(token, 'if'):
            token = self.conditional_command()
        elif self.is_terminal(token, 'while'):
            token = self.repetitive_command()
        else:
            self.syntactic_error(token, ERROR_MESSAGES[15])
        return token

    def procedure_call(self, token):
        token = self.list_expressions()
        if not self.is_terminal(token, ')'):
            self.syntactic_error(token, ERROR_MESSAGES[13])
    
    def conditional_command(self):
        token = self.expression()
        if not self.is_terminal(token, 'then'):
            lexeme = '' if not token else token.lexeme
            msg = ERROR_MESSAGES[14].format('then', lexeme)
            self.syntactic_error(token, msg)

        token = self.lexicon.next_token()
        token = self.unlabeled_command(token)
        if self.is_terminal(token, 'else'):
            token = self.lexicon.next_token()
            token = self.unlabeled_command(token)
        return token
    
    def repetitive_command(self):
        token = self.expression()
        if not self.is_terminal(token, 'do'):
            lexeme = '' if not token else token.lexeme
            msg = ERROR_MESSAGES[14].format('do', lexeme)
            self.syntactic_error(token, msg)

        token = self.lexicon.next_token()
        token = self.unlabeled_command(token)
        return token

    def assignment(self):
        return self.expression()
    
    def expression(self):
        token = self.simple_expression()
        if self.is_relationship(token):
            token = self.simple_expression()
        return token

    def simple_expression(self):
        token = self.lexicon.next_token()
        if token and token.lexeme in ('+, -'):
            token = self.lexicon.next_token()
            token = self.term(token)
        else:
            token = self.term(token)
        while self.is_operator1(token):
            token = self.lexicon.next_token()
            token = self.term(token)
        return token
        
    def term(self, token):
        token = self.factor(token)
        while self.is_operator2(token):
            token = self.lexicon.next_token()
            token = self.factor(token)
        return token

    def factor(self, token):
        if self.is_identifier(token):
            token = self.lexicon.next_token()
            if self.is_terminal(token, '('):
                self.function_call(token)
                token = self.lexicon.next_token()
            return token
        elif self.is_digit(token):
            return self.lexicon.next_token()
        elif self.is_terminal(token, '('):
            token = self.expression()
            if not token or not self.is_terminal(token, ')'):
                msg = ERROR_MESSAGES[11]
                self.syntactic_error(token, msg)
            return self.lexicon.next_token()
        else:
            lexeme = token.lexeme if token else ''
            msg = ERROR_MESSAGES[10].format(lexeme)
            self.syntactic_error(token, msg)
    
    def function_call(self, token):
        token = self.list_expressions()
        if not token or not self.is_terminal(token, ')'):
            self.syntactic_error(token, ERROR_MESSAGES[12])

    def list_expressions(self):
        token = self.expression()
        while self.is_terminal(token, ','):
            token = self.expression()
        return token

    def list_identifier(self, token=None, msg=None):
        if token:
            if not self.is_identifier(token):
                self.syntactic_error(token, ERROR_MESSAGES[5])
        else:
            self.check_identifier(msg)
            token = self.lexicon.next_token()

        while self.is_terminal(token, ','):
            self.check_identifier()
            token = self.lexicon.next_token()
        return token
    
    def formal_parameters(self):
        token = self.list_identifier(msg=ERROR_MESSAGES[7])
        if not self.is_terminal(token, ':'):
            self.syntactic_error(token, ERROR_MESSAGES[4])

        self.check_identifier()
        token = self.lexicon.next_token()
        while self.is_terminal(token, ';'):
            token = self.list_identifier(msg=ERROR_MESSAGES[7])
            if not self.is_terminal(token, ':'):
                self.syntactic_error(token, ERROR_MESSAGES[4])
            self.check_identifier()
            token = self.lexicon.next_token()

        if not self.is_terminal(token, ')'):
            msg = ERROR_MESSAGES[0].format(')')
            self.syntactic_error(token, msg)

    def is_terminal(self, token, terminal):
        if not token or token.lexeme != terminal:
            return False
        return True

    def is_identifier(self, token):
        if not token or token.TokenType != TokenType.IDENTIFICADOR:
            return False
        return True
    
    def is_digit(self, token):
        if not token or token.TokenType != TokenType.DIGITO:
            return False
        return True
    
    def is_operator2(self, token):
        if not token or token.lexeme not in ('*', 'div', 'and'):
            return False
        return True
    
    def is_operator1(self, token):
        if not token or token.lexeme not in ('+', '-', 'or'):
            return False
        return True
    
    def is_relationship(self, token):
        if token and token.lexeme in ('=', '<>', '<', '<=', '>', '>='):
            return True
        return False
    
    def is_unlabeled_command(self, token):
        if (self.is_identifier(token) 
            or self.is_terminal(token, 'if')
            or self.is_terminal(token, 'while')):
            return True
        return False

    def check_terminal(self, terminal):
        token = self.lexicon.next_token()
        if not self.is_terminal(token, terminal):
            msg = ERROR_MESSAGES[0].format(terminal)
            self.syntactic_error(token, msg)


    def check_identifier(self, msg=None):
        token = self.lexicon.next_token()
        msg = msg or ERROR_MESSAGES[2]
        if not token or not self.is_identifier(token):
            self.syntactic_error(token, msg)


    def check_type(self):
        keywords = ['integer', 'boolean', 'double', 'char']
        token = self.lexicon.next_token()
        if not token or not (token.TokenType == TokenType.IDENTIFICADOR 
                            or token.lexeme in keywords):
            self.syntactic_error(token, ERROR_MESSAGES[3])

    
    def syntactic_error(self, token, msg):
        line = token.line if token else self.lexicon.line
        raise SyntacticError(line, msg)
        
        


