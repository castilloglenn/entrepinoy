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


