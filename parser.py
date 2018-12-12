from math import cos, sin

from lex_analyzer import LexAnalyzer
from token_type import TokenType
import turtle

wn = turtle.Screen()
wn.screensize(1200, 1000)
wn.setup(1200, 1000)
alex = turtle.Turtle()
alex.radians()
alex.pensize(6)
alex.speed(50)
print(alex.position())
alex.dot()
alex.penup()


class ExpressionNode:
    """表达式节点对象

    Args:
        token_type (TokenType): 节点对应的记号类型

    Keyword Args:
        const_value (float): 常量值
        t (float): 参数 T
        func (object): 内置函数
        chile (ExpressionNode): 孩子节点，父节点对应的记号类型是 TokenType.func
        left (ExpressionNode): 左孩子节点
        right (ExpressionNode): 右孩子节点
    """
    def __init__(self, token_type, **kwargs):
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
        """递归打印语法树

        Args:
            indent (int): 语法树每一层对应的缩进
        """
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
            print("错误的树节点")

        if self.kind in [TokenType.const, TokenType.t]:
            return
        if self.kind == TokenType.func:
            self.child.print_tree(indent + 1)
        else:
            self.left.print_tree(indent + 1)
            self.right.print_tree(indent + 1)


def get_value(root):
    """计算表达式的值

    Args:
        root (ExpressionNode): 表达式的根节点
    """
    if not root:
        return 0.0
    if root.kind == TokenType.plus:
        return get_value(root.left) + get_value(root.right)
    elif root.kind == TokenType.minus:
        return get_value(root.left) - get_value(root.right)
    elif root.kind == TokenType.mul:
        return get_value(root.left) * get_value(root.right)
    elif root.kind == TokenType.div:
        return get_value(root.left) / get_value(root.right)
    elif root.kind == TokenType.power:
        return get_value(root.left) ** get_value(root.right)
    elif root.kind == TokenType.func:
        return root.func(get_value(root.child))
    elif root.kind == TokenType.const:
        return root.const
    elif root.kind == TokenType.t:
        return Property.parameter
    else:
        return 0.0


class Property:
    """语句属性
    """
    parameter = 0.0
    origin_x = 0.0
    origin_y = 0.0
    rot_ang = 0.0
    scale_x = 1
    scale_y = 1


def calc_coordinate(x, y):
    """计算点的坐标
    Args:
        x (ExpressionNode): x 坐标的表达式节点
        y (ExpressionNode): y 坐标的表达式节点
    """
    local_x = get_value(x)
    local_y = get_value(y)
    local_x *= Property.scale_x
    local_y *= Property.scale_y
    temp = local_x * cos(Property.rot_ang) + local_y * sin(Property.rot_ang)
    local_y = local_y * cos(Property.rot_ang) - local_x * sin(Property.rot_ang)
    local_x = temp
    local_x += Property.origin_x
    local_y += Property.origin_y
    return local_x, local_y


def draw_pixel(x: float, y: float):
    alex.goto(x, y)
    alex.dot("black")


def draw_loop(start, end, step, x_expr, y_expr):
    """for-draw 语句中，根据起点、终点、步长、x 坐标、y 坐标画出图形

    Args:
        start (float): 起点
        end (float): 终点
        step (float): 步长
        x_expr (ExpressionNode): x 坐标
        y_expr (ExpressionNode): y 坐标
    """
    Property.parameter = start
    while Property.parameter <= end:
        x_val, y_val = calc_coordinate(x_expr, y_expr)
        draw_pixel(x_val, y_val)
        Property.parameter += step
    return


def set_origin(x, y):
    Property.origin_x = x
    Property.origin_y = y


def set_rot(angle):
    Property.rot_ang = angle


def set_scale(x, y):
    Property.scale_x = x
    Property.scale_y = y


class Parser:
    """语法分析器

    Attributes:
        tokens (list): 记号流
        index (int): 遍历记号流时当前记号的索引
        tokens_length (int): 记号流长度
        current (Token): 遍历记号流时记录当前记号
    """

    def __init__(self, file):
        """初始化语法分析器，同时调用词法分析器获取记号流

        Args:
             file (file): 源程序文件
        """
        lex_analyzer = LexAnalyzer(file)
        self.tokens = lex_analyzer.get_token()
        self.index = 0
        self.tokens_length = len(self.tokens)
        self.current = None

    def fetch_token(self):
        """从记号流中获取记号，在 match_token() 中被调用"""
        try:
            self.current = self.tokens[self.index]
        except IndexError:
            print("语法分析结束")
        if self.current.type == TokenType.err:
            print("[No.{0}] 记号本身错误，请检查关键字是否拼写正确或者有非法的运算符".format(self.index))
            # exit(1)
        self.index += 1

    def match_token(self, token_type):
        """根据预期的记号类型判断当前记号是否合法，不合法则输出错误信息，反之获取下一记号

        Args:
            token_type (TokenType): 预期的记号类型
        """
        if self.current.type != token_type:
            print("[No.{0}] 该记号种类为 ".format(self.index) + str(self.current.type))
            print("期望的记号种类为 " + str(token_type))
            if token_type == TokenType.semico:
                print("缺少分号")
                # exit(1)
            print("[No.{0}] 记号类型不匹配".format(self.index))
            # exit(1)
        self.fetch_token()

    def parse(self):
        """开始语法分析"""
        self.fetch_token()
        self.program()

    def program(self):
        """遍历记号流"""
        while self.index < self.tokens_length:
            self.statement()
            self.match_token(TokenType.semico)

    def statement(self):
        """判断语句类型，调用对应语句的子程序"""
        if self.current.type == TokenType.origin:
            self.origin_statement()

        elif self.current.type == TokenType.rot:
            self.rot_statement()

        elif self.current.type == TokenType.scale:
            self.scale_statement()

        elif self.current.type == TokenType.for_:
            self.for_statement()

        else:
            print("[No.{0}] 不是合法的语句".format(self.index))
            # exit(1)

    def origin_statement(self):
        """origin 语句子程序，设置坐标原点"""
        self.match_token(TokenType.origin)
        self.match_token(TokenType.is_)
        self.match_token(TokenType.l_bracket)
        x_origin = self.expression()
        x_origin.print_tree(0)
        self.match_token(TokenType.comma)
        y_origin = self.expression()
        y_origin.print_tree(0)
        self.match_token(TokenType.r_bracket)
        set_origin(get_value(x_origin), get_value(y_origin))
        alex.setposition(Property.origin_x, Property.origin_y)
        return

    def rot_statement(self):
        """rot 语句子程序，设置图形旋转角度"""
        self.match_token(TokenType.rot)
        self.match_token(TokenType.is_)
        rot = self.expression()
        rot.print_tree(0)
        set_rot(get_value(rot))
        alex.left(Property.rot_ang)
        return

    def scale_statement(self):
        """scale 语句子程序，设置坐标轴比例"""
        self.match_token(TokenType.scale)
        self.match_token(TokenType.is_)
        self.match_token(TokenType.l_bracket)
        x_scale = self.expression()
        x_scale.print_tree(0)
        self.match_token(TokenType.comma)
        y_scale = self.expression()
        y_scale.print_tree(0)
        self.match_token(TokenType.r_bracket)
        set_scale(get_value(x_scale), get_value(y_scale))
        return

    def for_statement(self):
        """for 语句子程序，并画出图形"""
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
        draw_loop(get_value(start), get_value(end), get_value(step), x, y)
        return

    def expression(self):
        """构造表达式语法树"""
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

    def factor(self):
        if self.current.type == TokenType.plus:
            self.match_token(TokenType.plus)
            right = self.factor()

        elif self.current.type == TokenType.minus:
            self.match_token(TokenType.minus)
            right = self.factor()
            left = ExpressionNode(TokenType.const, const_value=0.0)
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
            quark = ExpressionNode(tmp_token.type, t=Property.parameter)

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
    parser = Parser("test.txt")
    parser.parse()
    turtle.done()
