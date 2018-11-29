from copy import deepcopy
from math import sin, cos, tan, log, exp, sqrt

from lexical.token_type import TokenType


class Token:
    def __init__(self, type, text, value=0.0, func=None):
        """

        :param type: Token_Type
        :param text: str
        :param value: float if type is const
        :param func: func if type is function
        """
        self.type = type
        self.text = text
        self.value = value
        self.func = func

    def __repr__(self):
        return "{0} -- {1} -- {2} -- {3}".format(
            self.type, self.text, self.value, self.func
        )


class LexAnalyzer:
    table = [
        Token(TokenType.const, "PI", 3.1415926),
        Token(TokenType.const, "E", 2.71828),
        Token(TokenType.t, "T"),
        Token(TokenType.func, "SIN", func=sin),
        Token(TokenType.func, "COS", func=cos),
        Token(TokenType.func, "TAN", func=tan),
        Token(TokenType.func, "LN", func=log),
        Token(TokenType.func, "EXP", func=exp),
        Token(TokenType.func, "SQRT", func=sqrt),
        Token(TokenType.origin, "ORIGIN"),
        Token(TokenType.scale, "SCALE"),
        Token(TokenType.rot, "ROT"),
        Token(TokenType.is_, "IS"),
        Token(TokenType.for_, "FOR"),
        Token(TokenType.from_, "FROM"),
        Token(TokenType.to, "TO"),
        Token(TokenType.step, "STEP"),
        Token(TokenType.draw, "DRAW")
    ]

    def __init__(self, file):
        self.file = file

    def read_line(self):
        with open(self.file, 'r', encoding="utf-8") as f:
            for line in f:
                yield line

    def match_num(self, text: str):
        value = float(text)
        token = Token(TokenType.const, text.upper(), value)
        return token

    def match_separator(self, text: str):
        if text == ';':
            return Token(TokenType.semico, text.upper())
        elif text == '(':
            return Token(TokenType.l_bracket, text.upper())
        elif text == ')':
            return Token(TokenType.r_bracket, text.upper())
        elif text == ',':
            return Token(TokenType.comma, text.upper())

    def match_operator(self, text: str):
        if text == '+':
            return Token(TokenType.plus, text.upper())
        elif text == '-':
            return Token(TokenType.minus, text.upper())
        elif text == '*':
            return Token(TokenType.mul, text.upper())
        elif text == '/':
            return Token(TokenType.div, text.upper())
        elif text == '**':
            return Token(TokenType.power, text.upper())

    def match_id(self, text: str):
        for token in self.table:
            if text.upper() == token.text:
                new_token = deepcopy(token)
                return new_token
        return Token(TokenType.err, text)

    def get_token(self):
        tokens = []
        for line in self.read_line():
            pointer = 0

            while pointer < len(line):
                if line[pointer].isalpha():
                    mark = pointer
                    pointer += 1
                    while line[pointer].isalpha():
                        pointer += 1
                        if pointer == len(line):
                            break
                    token = self.match_id(line[mark: pointer])
                    tokens.append(token)

                elif line[pointer].isdigit():
                    mark = pointer

                    while line[pointer].isdigit() or line[pointer] == '.':
                        pointer += 1
                        if pointer == len(line):
                            break
                    token = self.match_num(line[mark: pointer])
                    tokens.append(token)

                elif line[pointer] in [';', '(', ')', ',']:
                    mark = pointer
                    pointer += 1
                    token = self.match_separator(line[mark: pointer])
                    tokens.append(token)

                elif line[pointer] in ['+', '/', '*', '-']:
                    mark = pointer
                    pointer += 1
                    if pointer == len(line):
                        token = self.match_operator(line[mark: pointer])
                        tokens.append(token)
                        break
                    if line[pointer] in ['/', '-']:  # 连续两个 / 或 - , 即碰到注释，退出
                        break
                    elif line[pointer] == '*':  # 乘方符号
                        pointer += 1
                        token = self.match_operator(line[mark: pointer])
                        tokens.append(token)
                    else:  # 正常情况
                        token = self.match_operator(line[mark: pointer])
                        tokens.append(token)

                else:
                    pointer += 1
                    if pointer == len(line):
                        break
        return tokens


if __name__ == '__main__':
    analyzer = LexAnalyzer("test.txt")
    tokens = analyzer.get_token()
    for token in tokens:
        print(token)
