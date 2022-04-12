"""
# Calculating idle time
from datetime import datetime


format = "%Y/%m/%d, %H:%M:%S"
time1 = datetime.strptime("2022/04/05, 07:45:00", format)
time2 = datetime.strptime("2021/11/28, 06:59:00", format)

time3 = time1 - time2

print(time3.days)
print(time3.seconds)
"""
def get_slope(current_position, target_position):
        x = abs(target_position[0] - current_position[0])
        y = abs(target_position[1] - current_position[1])
        
        if y > x:
            sx = x / y
            sy = y / y
        else:
            sx = x / x
            sy = y / x
        
        if current_position[0] > target_position[0]:
            sx = -sx
        if current_position[1] > target_position[1]:
            sy = -sy
        
        return (sx, sy)
    

gg = [(9, 8), (2, 3)]
gl = [(7, 2), (5, 6)]
lg = [(3, 8), (6, 6)]
ll = [(8, 7), (2, 4)]
ge = [(7, 5), (2, 5)]
eg = [(6, 8), (6, 3)]
le = [(3, 5), (9, 5)]
el = [(8, 4), (8, 9)]
ee = [(5, 5), (5, 5)]

l = [gg, gl, lg, ll , ge, eg, le, el, ee]
for a in l:
    print(get_slope(a[0], a[1]))

