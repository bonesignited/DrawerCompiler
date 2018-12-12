from copy import deepcopy
from math import sin, cos, tan, log, exp, sqrt

from token_type import TokenType


class Token:
    """
    记号的数据类型

    Attributes:
        type (TokenType): 记号类型
        text (str): 记号的字符串表示
        value (float): 常量值
        func (object): 内置函数
    """
    def __init__(self, type, text, value=0.0, func=None):
        self.type = type
        self.text = text
        self.value = value
        self.func = func

    def __repr__(self):
        return "{0} -- {1} -- {2} -- {3}".format(
            self.type, self.text, self.value, self.func
        )


class LexAnalyzer:
    """词法分析器

    Attributes:
        file (str): 源程序文件
        table (list): 记号字典，用于区分id
    """

    def __init__(self, file):
        self.file = file
        self.table = [
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

    def read_line(self):
        with open(self.file, 'r', encoding="utf-8") as f:
            for line in f:
                yield line

    def match_num(self, text):
        """识别常量记号

        Args:
            text (str): 一段字符串，用于构造记号

        Returns:
            常量记号
        """
        value = float(text)
        token = Token(TokenType.const, text.upper(), value)
        return token

    def match_separator(self, text):
        """识别分隔符

        Args:
            text (str): 一段字符串，用于构造记号

        Returns:
            分隔符
        """
        if text == ';':
            return Token(TokenType.semico, text.upper())
        elif text == '(':
            return Token(TokenType.l_bracket, text.upper())
        elif text == ')':
            return Token(TokenType.r_bracket, text.upper())
        elif text == ',':
            return Token(TokenType.comma, text.upper())

    def match_operator(self, text):
        """识别操作符

        Args:
            text (str): 一段字符串，用于构造记号

        Returns:
            操作符
        """
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

    def match_id(self, text):
        """识别标识符

        Args:
            text (str): 一段字符串，用于构造记号

        Returns:
            标识符或者错误记号
        """
        for token in self.table:
            if text.upper() == token.text:
                new_token = deepcopy(token)
                return new_token
        return Token(TokenType.err, text)

    def get_token(self):
        """遍历字符串以构造记号流

        Returns:
            list: 记号流
        """
        tokens = []
        for line in self.read_line():
            pointer = 0

            while pointer < len(line):
                # 识别id
                if line[pointer].isalpha():
                    mark = pointer
                    pointer += 1
                    while line[pointer].isalpha():
                        pointer += 1
                        if pointer == len(line):
                            break
                    token = self.match_id(line[mark: pointer])
                    tokens.append(token)

                # 识别常量
                elif line[pointer].isdigit():
                    mark = pointer

                    while line[pointer].isdigit() or line[pointer] == '.':
                        pointer += 1
                        if pointer == len(line):
                            break
                    token = self.match_num(line[mark: pointer])
                    tokens.append(token)

                # 识别分隔符
                elif line[pointer] in [';', '(', ')', ',']:
                    mark = pointer
                    pointer += 1
                    token = self.match_separator(line[mark: pointer])
                    tokens.append(token)

                # 识别操作符
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

                # 遇到空格等空字符
                else:
                    pointer += 1
                    if pointer == len(line):
                        break

        # 打印记号流
        for token in tokens:
            print(token)
        return tokens


if __name__ == '__main__':
    analyzer = LexAnalyzer("test.txt")
    tokens = analyzer.get_token()
