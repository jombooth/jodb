import jo_db, time

"""
A test suite for sorting a large jo_db datasheet object.
"""

print '\n\nTESTING DATASHEET LOAD.\n\n'

fd = open('big_table.csv', 'r')
ds = jo_db.DataSheet(fd)

print '\n   Shape of datasheet:', ds.shape()

print '\n\nTESTING SORT SPEEDS.\n\n'

for i in range(0, min(10, ds.col_count)):
    start = time.time()
    print 'Time to sort datasheet by column %d:' % i
    ds.sort_by_col(i, compare_as="ints")
    print time.time() - start
