from enum import Enum, unique


@unique
class TokenType(Enum):
    """枚举类，记录记号类型"""
    origin = "ORIGIN"
    scale = "SCALE"
    rot = "ROT"
    is_ = "IS"
    to = "TO"
    step = "STEP"
    draw = "DRAW"
    for_ = "FOR"
    from_ = "FORM"

    t = "T"

    semico = ";"
    l_bracket = "("
    r_bracket = ")"
    comma = ","

    plus = "+"
    minus = "-"
    mul = "*"
    div = "/"
    power = "**"

    func = "FUNC"
    const = "CONST_ID"
    non = "NONTOKEN"
    err = "ERRTOKEN"


if __name__ == '__main__':
    print("index", end=",")
