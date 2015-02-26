import jo_db

"""
A test suite for the jo_db datasheet object.
"""

fd = open('test.db', 'r')
ds = jo_db.DataSheet(fd)

print '\n   Shape of datasheet:', ds.shape()
ds.pretty_print()

for i in range(0, ds.row_count):
    print 'Sorted datasheet by row %d:' % i
    ds.sort_by_col(i)
    ds.pretty_print()
    print '         ####################################\n'
