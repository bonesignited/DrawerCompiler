from lexical.lex_analyzer import LexAnalyzer
from lexical.token_type import TokenType


class ExpressionNode:
    def __init__(self, kind, left=None, right=None, func=None, const=None, param=None):
        self.kind = kind
        self.left = left
        self.right = right
        self.func = func
        self.const = const
        self.param = param


class Tree:
    def __init__(self, file):
        lex_analyzer = LexAnalyzer(file)
        self.tokens = lex_analyzer.get_token()
        self.token_id = 0
        self.tokens_length = len(self.tokens)
        self.root = ExpressionNode()
        self.queue = []

    def make_node(self, token):
        if token.type == TokenType.const:
            return ExpressionNode(TokenType.const, const=token.value)
        elif token.type == TokenType.params:
            return ExpressionNode(TokenType.params, param=token.value)
        elif token.type == TokenType.func:
            return ExpressionNode(TokenType.func, func=token.func)

    def parser(self):
        self.program()

    def match_token(self, token, type: TokenType):
        if token.type == type:
            self.token_id += 1
        else:
            raise ValueError("Don't match!!!")

    def program(self):
        while self.token_id != self.tokens_length:
            self.statement(self.tokens[self.token_id])
            if self.match_token(self.tokens[self.token_id], TokenType.semico):
                continue

    def statement(self, token):
        if token.type == TokenType.origin:
            self.origin_statement(token)
        elif token.type == TokenType.rot:
            self.rot_statement(token)
        elif token.type == TokenType.scale:
            self.scale_statement(token)
        elif token.type == TokenType.for_:
            self.for_statement(token)
        else:
            raise ValueError("Statement fault!!!")

    def origin_statement(self, token):
        pass

    def rot_statement(self, token):
        pass

    def scale_statement(self, token):
        pass

    def for_statement(self, token):
        pass

    def expression(self):
        pass

    def term(self):
        pass

    def factor(self):
        pass

    def component(self):
        pass

    def atom(self):
        pass
