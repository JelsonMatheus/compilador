from syntactic import Syntactic
from exception import SyntacticError

def main():
    try:
        syntactic = Syntactic('tests/7 - sintatico.txt')
        syntactic.start()
    except SyntacticError as error:
        print(error)


if __name__ == '__main__':
    main()
