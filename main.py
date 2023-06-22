from lexicon import Lexicon


def main():
    print('**************** TOKENS: ******************\n')

    
    arquivo = 'meuprograma.txt'
    lexicon = Lexicon(arquivo)

    print(f'{"TOKEN":<20} {"TIPO":<20}')
    print(f'{"-"*20:<20} {"-"*20:<20}')
    
    token = lexicon.next_token()
    while token:
        print(f'{token.lexeme:<20} {token.TokenType.name:<20}')
        token = lexicon.next_token()
    print()

if __name__ == '__main__':
    main()