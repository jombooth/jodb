import jo_db

"""
A test suite for the jo_db datasheet object.
"""

print '\n\nTESTING DATASHEET LOAD.\n\n'

fd = open('test2.csv', 'r')
ds = jo_db.DataSheet(fd)

print '\n   Shape of datasheet:', ds.shape()
ds.pretty_print()

for i in range(0, ds.col_count):
    print 'Sorted datasheet, ascending, by column %d:' % i
    ds.sort_by_col(i)
    ds.pretty_print()

for i in range(0, ds.col_count):
    print 'Sorted datasheet, descending, by column %d:' % i
    ds.sort_by_col(i, order="desc")
    ds.pretty_print()

print '         ####################################\n'

print '\n\nTESTING COLUMN BINOPS.\n\n'

print '\n   Adding columns 0 and 1'
ds.add_cols(0,1,as_types='ints').pretty_print()

print '\n   Subtracting columns 0 and 1'
ds.sub_cols(0,1,as_types='ints').pretty_print()

print '\n   Multiplying columns 0 and 1'
ds.mul_cols(0,1,as_types='ints').pretty_print()

print '\n   Dividing columns 0 and 1 as floats'
ds.div_cols(0,1,as_types='floats').pretty_print()

print '\n   Dividing columns 0 and 1 as strings (nonsense)'
ds.div_cols(0,1,as_types='strings').pretty_print()

print '         ####################################\n'

print '\n\nTESTING COLUMN UNOPS.\n\n'

# # Tested, but this function doesn't do much, so commented out for brevity.
# for i in range(0, ds.col_count):
#     print 'Stringified column %d of datasheet:' % i
#     ds.stringify_col(i)

for i in range(0, ds.col_count):
    print 'Intified column %d of datasheet:' % i
    ds.intify_col(i).pretty_print()

for i in range(0, ds.col_count):
    print 'Floatified column %d of datasheet:' % i
    ds.floatify_col(i).pretty_print()

for i in range(0, ds.col_count):
    print 'Squares of column %d of datasheet:' % i
    ds.pow_col(i, 2, as_type='floats').pretty_print()

for i in range(0, ds.col_count):
    print 'Mod 2 of column %d of datasheet:' % i
    ds.modn_col(i, 2, as_type='ints').pretty_print()

print '         ####################################\n'

print '\n\nTESTING COLUMN REDUCE OPERATIONS\n\n'

for i in range(0, ds.col_count):
    print 'Summed column %d of datasheet: %.1f' % (i, ds.sum_col(i))

for i in range(0, ds.col_count):
    print 'Variance of column %d of datasheet: %.1f' % (i, ds.var_col(i))

for i in range(0, ds.col_count):
    print 'Max of column %d of datasheet: %d' % (i, ds.max_col(i, as_type='ints'))

for i in range(0, ds.col_count):
    print 'Min of column %d of datasheet: %d' % (i, ds.min_col(i, as_type='ints'))

for i in range(0, ds.col_count):
    print 'Median of column %d of datasheet: %d' % (i, ds.med_col(i, as_type='ints'))

print '\n         ####################################\n'

print '\n\nTESTING SUBSET OPERATION\n\n'

print 'Columns 0,1,3,4 from original dataframe:'
ds.subset([0,1,3,4]).pretty_print()

print 'Columns 0 and 2 from original dataframe:'
ds.subset([0,2]).pretty_print()

print 'Column 0 from original dataframe:'
ds.subset([0]).pretty_print()

print 'No columns from original dataframe:'
ds.subset([]).pretty_print()

print '         ####################################\n'
