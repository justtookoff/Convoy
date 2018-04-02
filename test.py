import math

w = 320
h = 80

distanceX = abs(w)

x = math.tan(distanceX / h)
rad = math.atan(x)

degree = math.degrees(rad)

print(degree)
