import jo_db

"""
A test suite for the jo_db datasheet object.
"""

fd = open('test2.csv', 'r')
ds = jo_db.DataSheet(fd)

print '\n   Shape of datasheet:', ds.shape()
ds.pretty_print()

for i in range(0, ds.col_count):
    print 'Sorted datasheet by column %d:' % i
    ds.sort_by_col(i)
    ds.pretty_print()
    print '         ####################################\n'

print '\n\nTESTING COLUMN BINOPS.\n\n'

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

print '\n\nTESTING COLUMN UNOPS.\n\n'

# Tested, but this function doesn't do much, so commented out for brevity.
# for i in range(0, ds.col_count):
#     print 'Stringified column %d of datasheet:' % i
#     ds.stringify_col(i)
#     print '         ####################################\n'

for i in range(0, ds.col_count):
    print 'Intified column %d of datasheet:' % i
    ds.intify_col(i)
    print '         ####################################\n'

for i in range(0, ds.col_count):
    print 'Floatified column %d of datasheet:' % i
    ds.floatify_col(i)
    print '         ####################################\n'

for i in range(0, ds.col_count):
    print 'Squares of column %d of datasheet:' % i
    ds.pow_col(i, 2, as_type='floats')
    print '         ####################################\n'

for i in range(0, ds.col_count):
    print 'Mod 2 of column %d of datasheet:' % i
    ds.modn_col(i, 2, as_type='ints')
    print '         ####################################\n'

print '\n\nTESTING COLUMN REDUCE OPERATIONS\n\n'

for i in range(0, ds.col_count):
    print 'Summed column %d of datasheet:' % i
    print ds.sum_col(i)

for i in range(0, ds.col_count):
    print 'Variance of column %d of datasheet:' % i
    print ds.var_col(i)

for i in range(0, ds.col_count):
    print 'Max of column %d of datasheet:' % i
    print ds.max_col(i, as_type='ints')

for i in range(0, ds.col_count):
    print 'Min of column %d of datasheet:' % i
    print ds.min_col(i, as_type='ints')
