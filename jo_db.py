"""
Auxilary functions
"""

def identity_map(n):
    return {i:i for i in range(0,n)}

class DataSheet(object):
    def __init__(self, data_file=None):
        self.cols = {}
        self.row_map = {}
        self.row_count = 0
        self.col_count = 0

        if data_file is not None:
            data = data_file.read()
            rows = [row for row in data.split('\n') if row.strip() != '']
            self.row_count = len(rows)
            self.row_map = identity_map(self.row_count)

            for i in range(0, self.row_count):
                row_fields = rows[i].split(',')

                num_fields_in_row = len(row_fields)
                self.col_count = max(self.col_count, num_fields_in_row)

                for j in range(0, num_fields_in_row):

                    # create a jth column if one doesn't already exist.
                    if j not in self.cols:
                        self.cols[j] = {}
                    # want the ith element of the jth column.
                    self.cols[j][i] = row_fields[j]

    def shape(self):
        """
        Return a tuple of ints representing the database's shape.
        """
        return (self.row_count, self.col_count)

    def pretty_print(self, field_width=15, sep='| ', col_subset=None):
        """
        Display the database to a terminal window.

        Optional arguments:
        field_width - int. corresponds to the number of characters of
        each field that should be displayed.

        sel - string, specify the separator that sits between columns.

        """
        def fill_to_width(field, with_sep=False):
            """
            Given a field to be displayed, space-pad or truncate it to field_width.
            Note that we copy field_width to _field_width so we can modify it
            """
            _field_width = field_width
            field = str(field)

            if with_sep:
                _field_width += (len(sep) - 1)

            if len(field) <= _field_width:
                field += ' ' * (_field_width - len(field))
            return field[:_field_width]

        # find with of rendered database endcaps
        cap_width = ((field_width + len(sep)) * self.col_count + 1)

        print "_" * cap_width

        for i in range(0, self.row_count):
            row_buf = sep

            for j in range(0, self.col_count):

                # Handle partially-filled rows. print "no data" in all
                # unfilled cells.
                try:
                    row_datum = self.cols[j][self.row_map[i]]

                    row_buf += fill_to_width(row_datum) + sep
                except KeyError:
                    row_buf += fill_to_width('NULL') + sep

            print row_buf + '<- row %s, maps to row %s' % (str(i), str(self.row_map[i]))

        print '*' * cap_width

        # TODO: add named columns?
        # Display column names/indices
        for i in range(0, self.col_count):
            print fill_to_width('  ^ Column %s' % str(i), with_sep=True),
        print '\n'

    def unop_col(self, col_num_a, f):
        pass

    def binop_cols(self, col_num_a, col_num_b, f):
        """
        Perform a binary operation f on two columns, and return
        a DataSheet containing only the modified column. This
        DataSheet will inherit its row_map from its parent.
        """
        new_col = DataSheet()
        new_col.cols[0] = {v: f(self.cols[col_num_a][v], self.cols[col_num_b][v])
                                           for (_,v) in self.row_map.iteritems()}
        new_col.col_count = 1
        new_col.row_count = self.row_count
        new_col.row_map = self.row_map
        new_col.pretty_print()


    # TODO: condense
    def add_cols(self, col_num_a, col_num_b, as_types="strings"):
        if as_types == "ints":
            def f(a,b):
                return int(a) + int(b)
        elif as_types == "floats":
            def f(a,b):
                return float(a) + float(b)
        else: # default to strings
            def f(a,b):
                return str(a) + str(b)

        self.binop_cols(col_num_a, col_num_b, f)

    def sub_cols(self, col_num_a, col_num_b, as_types="strings"):
        if as_types == "ints":
            def f(a,b):
                return int(a) - int(b)
        elif as_types == "floats":
            def f(a,b):
                return float(a) - float(b)
        else: # default to strings
            def f(a,b):
                return "TYPE_ERROR"

        self.binop_cols(col_num_a, col_num_b, f)

    def mul_cols(self, col_num_a, col_num_b, as_types="strings"):
        if as_types == "ints":
            def f(a,b):
                return int(a) * int(b)
        elif as_types == "floats":
            def f(a,b):
                return float(a) * float(b)
        else: # default to strings
            def f(a,b):
                return "TYPE_ERROR"

        self.binop_cols(col_num_a, col_num_b, f)

    def div_cols(self, col_num_a, col_num_b, as_types="strings"):
        if as_types == "ints":
            def f(a,b):
                return int(a) / int(b)
        elif as_types == "floats":
            def f(a,b):
                return float(a) / float(b)
        else: # default to strings
            def f(a,b):
                return "TYPE_ERROR"

        self.binop_cols(col_num_a, col_num_b, f)

    def sort_by_col(self, col):
        # TODO: implement a real sort, and return the sorted index mappings.
        # This implementation uses Python's built-in sort function,
        # and is also quite slow.
        items = [self.cols[col][i] for i in range(0, self.row_count)]
        newnums = [items.index(elt) for elt in sorted(items)]

        for i in range(0, self.row_count):
            self.row_map[i] = newnums[i]
