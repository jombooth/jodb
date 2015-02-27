"""
Auxilary functions
"""

def identity_map(n):
    return {i:i for i in range(0,n)}

def inv_map(map):
    return {v:k for (k,v) in map.iteritems()}

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

    def reduce_col(self, col_num_a, f, init):
        """
        let a0, a1, ... , an
        be the elements of col_num_a. Then return (f an ... (f a1 (f a0 init)) ... )
        """
        accum = init

        for i in range(0, self.row_count):
            accum = f(self.cols[col_num_a][self.row_map[i]], accum)

        return accum

    # TODO: dress this up a bit.
    def sum_col(self, col_num_a):
        def add(a,b):
            return int(a) + int(b)
        return self.reduce_col(col_num_a, add, 0)

    def unop_col(self, col_num_a, f):
        """
        Perform a unary operation f on one column, and display
        a DataSheet containing only the modified column. This
        DataSheet will inherit its row_map from its parent.
        """
        new_col = DataSheet()
        new_col.cols[0] = {v: f(self.cols[col_num_a][v]) for (_,v) in self.row_map.iteritems()}

        new_col.col_count = 1
        new_col.row_count = self.row_count
        new_col.row_map = self.row_map
        new_col.pretty_print()

    def intify_col(self, col_num_a):
        def f(x):
            return int(x)

        self.unop_col(col_num_a, f)

    def floatify_col(self, col_num_a):
        def f(x):
            return float(x)

        self.unop_col(col_num_a, f)

    def stringify_col(self, col_num_a):
        def f(x):
            return str(x)

        self.unop_col(col_num_a, f)

    def pow_col(self, col_num_a, n, as_type="floats"):
        if as_type=="ints":
            def f(x):
                return int(int(x)**n)
        else:
            def f(x):
                return float(x)**n

        self.unop_col(col_num_a, f)

    def modn_col(self, col_num_a, n):
        def f(x):
            return x % n

        self.unop_col(col_num_a, f)

    def binop_cols(self, col_num_a, col_num_b, f):
        """
        Perform a binary operation f on two columns, and display
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
    # TODO: consider supporting other column types.
    #       for now, treat database as a database of string literals
    #       and convert in and out of this representation as needed.
    def add_cols(self, col_num_a, col_num_b, as_types="strings"):
        if as_types == "ints":
            def f(a,b):
                return str(int(a) + int(b))
        elif as_types == "floats":
            def f(a,b):
                return str(float(a) + float(b))
        else: # default to strings
            def f(a,b):
                return str(a) + str(b)

        self.binop_cols(col_num_a, col_num_b, f)

    def sub_cols(self, col_num_a, col_num_b, as_types="strings"):
        if as_types == "ints":
            def f(a,b):
                return str(int(a) - int(b))
        elif as_types == "floats":
            def f(a,b):
                return str(float(a) - float(b))
        else: # default to strings
            def f(a,b):
                return "TYPE_ERROR"

        self.binop_cols(col_num_a, col_num_b, f)

    def mul_cols(self, col_num_a, col_num_b, as_types="strings"):
        if as_types == "ints":
            def f(a,b):
                return str(int(a) * int(b))
        elif as_types == "floats":
            def f(a,b):
                return str(float(a) * float(b))
        else: # default to strings
            def f(a,b):
                return "TYPE_ERROR"

        self.binop_cols(col_num_a, col_num_b, f)

    def div_cols(self, col_num_a, col_num_b, as_types="strings"):
        if as_types == "ints":
            def f(a,b):
                return str(int(a) / int(b))
        elif as_types == "floats":
            def f(a,b):
                return str(float(a) / float(b))
        else: # default to strings
            def f(a,b):
                return "TYPE_ERROR"

        self.binop_cols(col_num_a, col_num_b, f)

    def sort_by_col(self, col, compare_as="strings", order="asc", sort_type="quicksort"):
        # Create a tagged copy of the column such that the new column's map
        # is necessarily a bijection.

        # (remap the column so that each value is stored with its key.)
        # possibly slow, profile this later
        tagged_col = {k:(k,v) for (k,v) in self.cols[col].iteritems()}
        inv_column_mapping = inv_map(tagged_col)

        def order_flip(b):
            if order=="desc":
                return not b
            else:
                return b

        # TODO: decide where to put the detupleing
        if compare_as == "ints":
            def compare(a,b):
                return order_flip(int(a[1]) < int(b[1]))
        elif compare_as == "floats":
            def compare(a,b):
                return order_flip(float(a[1]) < float(b[1]))
        else:
            def compare(a,b):
                return order_flip(str(a[1]) < str(b[1]))

        def quicksort(lst):
            if len(lst) > 1:
                mid = len(lst)/2
                pivot = lst[mid]
                left, right = [elt for elt in lst[:mid] + lst[mid+1:] if compare(elt, pivot)], \
                              [elt for elt in lst[:mid] + lst[mid+1:] if not compare(elt, pivot)]
                return quicksort(left) + [pivot] + quicksort(right)
            else:
                return lst

        # punchline: all we really want to change is the row_map
        sorted_items = quicksort(tagged_col.values())

        self.row_map = {i:inv_column_mapping[sorted_items[i]] for i in range(0, self.row_count)}
