from exception import TokenError
from util import TokenType, Token


EOF = '\0'
TERMINALS = ['\n', '\t', ' ']


class Lexicon:

    reserved_words = [
        'program', 'if', 'then', 'else', 'while', 'do', 
        'until', 'repeat', 'int', 'double', 'char', 
        'case', 'switch', 'end', 'procedure', 
        'function', 'for', 'begin'
    ]

    def __init__(self, filename):
        self.position = 0
        self.line = 1
        self.source = open(filename)

    def next_token(self):
        try:
            self._token = None
            self.q0('') 
            return self._token
        except TokenError as error:
            self.source.close()
            print()
            print(error)
    
    def q0(self, lexeme):
        char = self.read_char()
        while char in TERMINALS:
            self.move_position()
            char = self.read_char()
        
        lexeme += char
        if char.isalpha():
            self.q1(lexeme)
        elif char.isdigit():
            self.q6(lexeme)
        elif char == '-':
            self.q9(lexeme)
        elif char == '@':
            self.q10(lexeme)
        elif char == '/':
            self.q13(lexeme)
        elif char in ';,.*()\{\}=':
            self.q17(lexeme)
        elif char == '<':
            self.q18(lexeme)
        elif char in '>:':
            self.q19(lexeme)
        elif char == '+':
            self.q20(lexeme)
        elif char != EOF:
           raise TokenError(self.line, lexeme)

    def q1(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isalpha() or char.isdigit():
            self.q2(lexeme+char)
        elif char == '.':
            self.q3(lexeme+char)
        elif char == '_':
            self.q4(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.IDENTIFICADOR)
    
    def q2(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isalpha() or char.isdigit():
            self.q2(lexeme+char)
        elif char == '.':
            self.q21(lexeme+char)
        else:
            if lexeme in self.reserved_words:
                self.set_token(char, lexeme, TokenType.PALAVRA_RESERVADA)
            else:
                self.set_token(char, lexeme, TokenType.IDENTIFICADOR)

    def q3(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isalpha() or char.isdigit():
            self.q22(lexeme+char)
        else:
           raise TokenError(self.line, lexeme+char)
    
    def q4(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isalpha() or char.isdigit():
            self.q5(lexeme+char)
        else:
            raise TokenError(self.line, lexeme+char)
    
    def q5(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isalpha() or char.isdigit():
            self.q5(lexeme+char)
        elif char == '.':
            self.q3(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.IDENTIFICADOR)
    
    def q6(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isdigit():
            self.q6(lexeme+char)
        elif char == ',':
            self.q7(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.DIGITO)
    
    def q7(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isdigit():
            self.q8(lexeme+char)
        else:
            raise TokenError(self.line, lexeme+char)
    
    def q8(self, lexeme):
        self.move_position()
        char = self.read_char()
        
        if char.isdigit():
            self.q8(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.DIGITO)
    
    def q9(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isdigit():
            self.q6(lexeme+char)
        elif char == '-':
            self.q17(lexeme+char)
        else:
            raise TokenError(self.line, lexeme+char)
    
    def q10(self, lexeme):
        self.move_position()
        char = self.read_char()
        
        if char == '@':
            self.q11(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.SIMBOLO)
    
    def q11(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char == '\n':
            self.q12(lexeme)
        else:
            self.q11(lexeme+char)
    
    def q12(self, lexeme):
        self.move_position()
        self.q0('')

    def q13(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char == '/':
            self.q14(lexeme+char)
        elif char == '*':
            self.q16(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.SIMBOLO)
    
    def q14(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char == '/':
            self.q15(lexeme+char)
        else:
            self.q14(lexeme+char)
    
    def q15(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char == '/':
            self.q12(lexeme+char)
        else:
            raise TokenError(self.line, lexeme+char)
    
    def q16(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char == '*':
            self.q15(lexeme+char)
        else:
            self.q16(lexeme+char)
    
    def q17(self, lexeme):
        self.set_token('', lexeme, TokenType.SIMBOLO)
        self.move_position()
    
    def q18(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char in '>=':
            self.q17(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.SIMBOLO)
    
    def q19(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char == '=':
            self.q17(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.SIMBOLO)
    
    def q20(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char == '+':
            self.q17(lexeme+char)
        else:
            self.set_token(char, lexeme, TokenType.SIMBOLO)

    def q21(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isalpha() or char.isdigit():
            self.q22(lexeme+char)
        else:
            raise TokenError(self.line, lexeme+char)
    
    def q22(self, lexeme):
        self.move_position()
        char = self.read_char()

        if char.isalpha() or char.isdigit():
            self.q22(lexeme+char)
        else:
            if lexeme in self.reserved_words:
                self.set_token(char, lexeme, TokenType.PALAVRA_RESERVADA)
            else:
                self.set_token(char, lexeme, TokenType.IDENTIFICADOR)

    def move_position(self):
        self.position += 1

    def read_char(self) -> str:
        if self.source.closed:
            return EOF

        self.source.seek(self.position)
        char = self.source.read(1)

        if not char:
            self.source.close()
            return EOF
        elif char == '\n':
            self.line += 1
            
        return char
    
    def set_token(self, char, lexeme, type_):
        if char in TERMINALS:
            self.move_position()
        self._token = Token(lexeme, type_)


    
