import jo_db

"""
A test suite for the jo_db datasheet object.
"""

fd = open('test2.csv', 'r')
ds = jo_db.DataSheet(fd)

print '\n   Shape of datasheet:', ds.shape()
ds.pretty_print()

for i in range(0, ds.row_count):
    print 'Sorted datasheet by row %d:' % i
    ds.sort_by_col(i)
    ds.pretty_print()
    print '         ####################################\n'

print '\n   Adding columns 0 and 1'
ds.add_cols(0,1,as_types='ints')

print '\n   Subtracting columns 0 and 1'
ds.sub_cols(0,1,as_types='ints')

print '\n   Multiplying columns 0 and 1'
ds.mul_cols(0,1,as_types='ints')

print '\n   Dividing columns 0 and 1 as floats'
ds.div_cols(0,1,as_types='floats')

print '\n   Dividing columns 0 and 1 as strings (nonsense)'
ds.div_cols(0,1,as_types='strings')
