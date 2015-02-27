import random

COL_COUNT = 25
ROW_COUNT = 100000
MIN = 0
MAX = 1000

fd = open('test_big.csv', 'w')

for j in range(0, ROW_COUNT):
    for i in range(0, COL_COUNT):
        if i < (COL_COUNT-1):
            fd.write(str(random.randint(MIN,MAX)) + ',')
        else:
            fd.write(str(random.randint(MIN,MAX)))
    fd.write('\n')

fd.close()
