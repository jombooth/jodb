import jo_db

fd = open('test.db', 'r')
ds = jo_db.DataSheet(fd)

print ds.shape()
ds.pretty_print()
