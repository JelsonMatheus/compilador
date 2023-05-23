from lexico import Lexico


def main():
    print('********** TOKENS: ******************')

    arquivo = 'tests/identificadores_invalidos.txt'
    lexico = Lexico(arquivo)
    token = lexico.ler_token()
    while token:
        print(token)
        token = lexico.ler_token()

if __name__ == '__main__':
    main()