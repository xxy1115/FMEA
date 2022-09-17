# -*- coding: UTF-8 -*-
import random
import time

cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
print(cur_time)

# num = random.randint(1000, 9999)
# print(num)


sa = []
for i in range(32):
    sa.append(random.choice("1234567890abcde"))
salt = "".join(sa)
print(salt)
