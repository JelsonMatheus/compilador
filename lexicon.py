from exception import TokenError
from util import TypeToken, Token



EOF = '\0'
TERMINALS = ['\n', '\t', ' ']


class Lexicon:

    def __init__(self, filename):
        self.position = 0
        self.line = 1
        with open(filename) as file_:
            self.source = file_.read()

    def next_token(self):
        try:
            self._token = None
            self.q0('') 
            return self._token
        except TokenError as error:
            print(error)
    
    def q0(self, lexeme):
        char = self.next_character()
        while char in TERMINALS:
            char = self.next_character()

        lexeme += char
        if char.isalpha():
            self.q1(lexeme)
        elif char.isdigit():
            self.q6(lexeme)
        elif char == '-':
            self.q9(lexeme)
        elif char != EOF:
           raise TokenError(self.line, lexeme)

    def q1(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isalpha() or char.isdigit():
            self.q2(lexeme)
        elif char == '.':
            self.q3(lexeme)
        elif char == '_':
            self.q4(lexeme)
        else:
            self.set_token(lexeme, TypeToken.IDENTIFICADOR)
    
    def q2(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isalpha() or char.isdigit():
            self.q2(lexeme)
        else:
            self.set_token(lexeme, TypeToken.IDENTIFICADOR)

    def q3(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isalpha() or char.isdigit():
            self.q2(lexeme)
        else:
           raise TokenError(self.line, lexeme)
    
    def q4(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isalpha() or char.isdigit():
            self.q5(lexeme)
        else:
            raise TokenError(self.line, lexeme)
    
    def q5(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isalpha() or char.isdigit():
            self.q5(lexeme)
        elif char == '.':
            self.q3(lexeme)
        else:
            self.set_token(lexeme, TypeToken.IDENTIFICADOR)
    
    def q6(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isdigit():
            self.q6(lexeme)
        elif char == ',':
            self.q7(lexeme)
        else:
            self.set_token(lexeme, TypeToken.DIGITO)
    
    def q7(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isdigit():
            self.q8(lexeme)
        else:
            raise TokenError(self.line, lexeme)
    
    def q8(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isdigit():
            self.q8(lexeme)
        else:
            self.set_token(lexeme, TypeToken.DIGITO)
    
    def q9(self, lexeme):
        char = self.next_character()
        lexeme += char
        if char.isdigit():
            self.q6(lexeme)
        else:
            raise TokenError(self.line, lexeme)

    def next_character(self) -> str:
        char = EOF
        if self.position < len(self.source):
            char = self.source[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
        return char
    
    def set_token(self, lexeme, tipo):
        char = lexeme[-1]
        if not (char in TERMINALS or char == EOF):
            self.position -= 1
        self._token = Token(lexeme[:-1], tipo)
        


    
