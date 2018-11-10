from math import sin, cos, tan, log, exp, sqrt

from lexical.token_type import TokenType


class Token:
    def __init__(self, type, lexeme, value=0.0, func=None):
        '''

        :param type: Token_Type
        :param lexeme: str
        :param value: float if type is const
        :param func: func if type is function
        '''
        self.type = type
        self.lexeme = lexeme
        self.value = value
        self.func = func


class Analyzer:
    table = [
        Token(TokenType.const, "PI", 3.1415926),
        Token(TokenType.const, "E", 2.71828),
        Token(TokenType.params, "T"),
        Token(TokenType.func, "SIN", func=sin),
        Token(TokenType.func, "SOC", func=cos),
        Token(TokenType.func, "TAN", func=tan),
        Token(TokenType.func, "LN", func=log),
        Token(TokenType.func, "EXP", func=exp),
        Token(TokenType.func, "SQRT", func=sqrt),
        Token(TokenType.reserved, "ORIGIN"),
        Token(TokenType.reserved, "SCALE"),
        Token(TokenType.reserved, "ROT"),
        Token(TokenType.reserved, "IS"),
        Token(TokenType.reserved, "FOR"),
        Token(TokenType.reserved, "FROM"),
        Token(TokenType.reserved, "TO"),
        Token(TokenType.reserved, "STEP"),
        Token(TokenType.reserved, "DRAW")
    ]

    def __init__(self, file):
        self.file = file

    def read_line(self):
        with open(self.file, 'r') as f:
            for line in f:
                yield line

    def get_token(self):
        tokens = []
        for line in self.read_line():
            pointer = 0

            while pointer < len(line):
                if line[pointer].isalpha():
                    mark = pointer

                    while line[pointer].isalpha():
                        pointer += 1
                        if pointer == len(line):
                            break
                    tokens.append(line[mark: pointer])

                elif line[pointer].isdigit():
                    mark = pointer

                    while line[pointer].isdigit() or line[pointer] == '.':
                        pointer += 1
                        if pointer == len(line):
                            break
                    tokens.append(line[mark: pointer])

                elif line[pointer] in [';', '(', ')', ',', '+']:
                    mark = pointer
                    pointer += 1
                    tokens.append(line[mark: pointer])

                elif line[pointer] in ['/', '*', '-']:
                    mark = pointer
                    pointer += 1
                    if pointer == len(line):
                        tokens.append(line[mark: pointer])
                        break
                    if line[pointer] in ['/', '*', '-']:
                        pointer += 1
                    tokens.append(line[mark: pointer])

                else:
                    pointer += 1
                    if pointer == len(line):
                        break
        return tokens


if __name__ == '__main__':
    analyzer = Analyzer("test.txt")
    tokens = analyzer.get_token()
    print(tokens)
