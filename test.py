import re

dic = {"data": 1, "mmr": 2}
str = "data+mmr/2+1"
expression = re.split("([-|+|*|/])", str)
print(expression)

a = [1, 2, 3]
print(a[::-1])
a = [
    1,
    "+",
    2,
    "",
    3,
    5,
    6,
]
