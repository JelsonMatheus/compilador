from lexicon import Lexicon


def main():
    print('********** TOKENS: ******************\n')

    arquivo = 'tests/5 - palavras reservadas.txt'
    lexicon = Lexicon(arquivo)
    token = lexicon.next_token()
    while token:
        print(token)
        token = lexicon.next_token()
    print()

if __name__ == '__main__':
    main()