from enum import Enum, unique


@unique
class TokenType(Enum):
    reserved = {
        "id": 1,
        "representation": [
            "ORIGIN",
            "SCALE",
            "ROT",
            "IS",
            "TO",
            "STEP",
            "DRAW",
            "FOR",
            "FROM"
        ]
    }

    params = {
        "id": 2,
        "representation": ["T"]
    }

    separator = {
        "id": 3,
        "representation": [
            "SEMICO",
            "L_BRACKET",
            "R_BRACKET",
            "COMMA"
        ]
    }

    operator = {
        "id": 4,
        "representation": [
            "PLUS",
            "MINUS",
            "MUL",
            "DIV",
            "POWER"
        ]
    }

    func = {
        "id": 5,
        "representation": ["func"]
    }

    const = {
        "id": 6,
        "representation": ["CONST_ID"]
    }

    non = {
        "id": 7,
        "representation": ["NONTOKEN"]
    }

    err = {
        "id": 8,
        "representation": ["ERRTOKEN"]
    }


