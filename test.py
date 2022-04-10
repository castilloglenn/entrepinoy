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

import os
import psutil

def memory_usage_psutil():
    # return the memory usage in percentage like top
    process = psutil.Process(os.getpid())
    mem = process.memory_percent()
    return mem

consume_memory = range(20*1000*1000)

while True:
    print(memory_usage_psutil())

