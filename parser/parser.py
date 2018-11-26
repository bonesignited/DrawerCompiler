from lexical.lex_analyzer import LexAnalyzer
from lexical.token_type import TokenType


class ExpressionNode:
    def __init__(self, token_type, **kwargs):
        """
        表达式节点对象
        :param kind: 记号种类
        :param left: 二元运算左边
        :param right: 二元运算右边
        :param func: 函数调用
        :param child: 函数括号里的表达式
        :param const: 常数，绑定右值
        :param param: 参数T，绑定左值
        """
        self.kind = token_type
        if token_type == TokenType.const:
            self.const = kwargs.get("const_value")
        elif token_type == TokenType.t:
            self.param = kwargs.get("t")
        elif token_type == TokenType.func:
            self.func = kwargs.get("func")
            self.child = kwargs.get("child")
        else:
            self.left = kwargs.get("left")
            self.right = kwargs.get("right")

    def print_tree(self, indent: int):
        for i in range(0, indent):
            print("\t", end="")
        print(">> ", end="")
        tmp_type = self.kind
        if tmp_type == TokenType.plus:
            print("+")
        elif tmp_type == TokenType.minus:
            print("-")
        elif tmp_type == TokenType.mul:
            print("*")
        elif tmp_type == TokenType.div:
            print("/")
        elif tmp_type == TokenType.power:
            print("**")
        elif tmp_type == TokenType.func:
            print(self.func)
        elif tmp_type == TokenType.const:
            print(self.const)
        elif tmp_type == TokenType.t:
            print("T")
        else:
            print("Error Tree Node")

        if self.kind in [TokenType.const, TokenType.t]:
            return
        if self.kind == TokenType.func:
            self.child.print_tree(indent + 1)
        else:
            self.left.print_tree(indent + 1)
            self.right.print_tree(indent + 1)


class StmtProperty:
    parameter = 0


class Parser:
    def __init__(self, file):
        lex_analyzer = LexAnalyzer(file)
        self.tokens = lex_analyzer.get_token()
        self.index = 0
        self.tokens_length = len(self.tokens)
        self.current = None

    def fetch_token(self):
        try:
            self.current = self.tokens[self.index]
        except IndexError:
            print("语法分析结束")
        if self.current.type == TokenType.err:
            raise ValueError("错误的记号！！！！！")
        self.index += 1

    def match_token(self, token_type):
        if self.current.type != token_type:
            raise ValueError("记号类型不匹配！！！！！")
        self.fetch_token()

    def parse(self):
        self.fetch_token()
        self.program()

    def program(self):
        while self.index < self.tokens_length:
            self.statement()
            self.match_token(TokenType.semico)

    def statement(self):
        if self.current.type == TokenType.origin:
            self.origin_statement()

        elif self.current.type == TokenType.rot:
            self.rot_statement()

        elif self.current.type == TokenType.scale:
            self.scale_statement()

        elif self.current.type == TokenType.for_:
            self.for_statement()

        else:
            raise ValueError("Statement fault!!!")

    def origin_statement(self):
        self.match_token(TokenType.origin)
        self.match_token(TokenType.is_)
        self.match_token(TokenType.l_bracket)
        x_origin = self.expression()
        x_origin.print_tree(0)
        self.match_token(TokenType.comma)
        y_origin = self.expression()
        y_origin.print_tree(0)
        self.match_token(TokenType.r_bracket)
        return

    def rot_statement(self):
        self.match_token(TokenType.rot)
        self.match_token(TokenType.is_)
        rot = self.expression()
        rot.print_tree(0)
        return

    def scale_statement(self):
        self.match_token(TokenType.origin)
        self.match_token(TokenType.is_)
        self.match_token(TokenType.l_bracket)
        x_scale = self.expression()
        x_scale.print_tree(0)
        self.match_token(TokenType.comma)
        y_scale = self.expression()
        y_scale.print_tree(0)
        self.match_token(TokenType.r_bracket)
        return

    def for_statement(self):
        self.match_token(TokenType.for_)
        self.match_token(TokenType.t)
        self.match_token(TokenType.from_)
        start = self.expression()
        start.print_tree(0)
        self.match_token(TokenType.to)
        end = self.expression()
        end.print_tree(0)
        self.match_token(TokenType.step)
        step = self.expression()
        step.print_tree(0)
        self.match_token(TokenType.draw)
        self.match_token(TokenType.l_bracket)
        x = self.expression()
        x.print_tree(0)
        self.match_token(TokenType.comma)
        y = self.expression()
        y.print_tree(0)
        self.match_token(TokenType.r_bracket)
        return

    def expression(self):
        left = self.term()
        while self.current.type in [TokenType.plus, TokenType.minus]:
            token_tmp = self.current.type
            self.match_token(token_tmp)
            right = self.term()
            left = ExpressionNode(token_tmp, left=left, right=right)
        return left

    def term(self):
        left = self.factor()
        while self.current.type in [TokenType.mul, TokenType.div]:
            token_tmp = self.current.type
            self.match_token(token_tmp)
            right = self.factor()
            left = ExpressionNode(token_tmp, left=left, right=right)
        return left

    def factor(self):  # 代表右结合的 +/-
        if self.current.type == TokenType.plus:
            self.match_token(TokenType.plus)
            right = self.factor()

        elif self.current.type == TokenType.minus:
            self.match_token(TokenType.minus)
            right = self.factor()
            left = ExpressionNode(TokenType.const, const=0.0)
            right = ExpressionNode(TokenType.minus, left=left, right=right)

        else:
            right = self.component()

        return right

    def component(self):
        left = self.atom()
        if self.current.type == TokenType.power:
            self.match_token(TokenType.power)
            right = self.component()
            left = ExpressionNode(TokenType.power, left=left, right=right)
        return left

    def atom(self):
        tmp_token = self.current
        if self.current.type == TokenType.const:
            self.match_token(TokenType.const)
            quark = ExpressionNode(tmp_token.type, const_value=tmp_token.value)

        elif self.current.type == TokenType.t:
            self.match_token(TokenType.t)
            quark = ExpressionNode(tmp_token.type, t=StmtProperty.parameter)

        elif self.current.type == TokenType.func:
            self.match_token(TokenType.func)
            self.match_token(TokenType.l_bracket)
            temp = self.expression()
            quark = ExpressionNode(tmp_token.type, func=tmp_token.func, child=temp)
            self.match_token(TokenType.r_bracket)

        elif self.current.type == TokenType.l_bracket:
            self.match_token(TokenType.l_bracket)
            quark = self.expression()
            self.match_token(TokenType.r_bracket)

        else:
            raise ValueError("不是预期的记号")

        return quark


if __name__ == '__main__':
    tree = Parser("test.txt")
    tree.parse()
