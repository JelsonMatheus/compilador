from lexicon import Lexicon


def main():
    print('********** TOKENS: ******************\n')

    
    arquivo = 'tests/6 - todos.txt'
    lexicon = Lexicon(arquivo)

    print(f'{"TOKEN":<25} {"TIPO":<25}')
    print(f'{"-"*20:<25} {"-"*20:<25}')
    
    token = lexicon.next_token()
    while token:
        print(f'{token.lexeme:<25} {token.TokenType.name:<25}')
        token = lexicon.next_token()
    print()

if __name__ == '__main__':
    main()