import math

a = float(input("длина первой стороны: "))
b = float(input("длина второй стороны: "))
angle = float(input("угол между ними: "))

c = math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(angle))

print("третья сторона:", c)