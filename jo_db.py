
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

            for i in range(0, self.row_count):
                # "sorting" the database is equivalent to changing the row_map
                # int -> int mapping
                self.row_map[i] = i

                row_fields = rows[i].split(',')

                num_fields_in_row = len(row_fields)
                self.col_count = max(self.col_count, num_fields_in_row)

                for j in range(0, num_fields_in_row):

                    # create a jth column if one doesn't already exist.
                    if j not in self.cols:
                        self.cols[j] = {}
                    # want the ith element of the jth column.
                    self.cols[j][i] = row_fields[j]

        else:
            print "No data in provided file."

    def shape(self):
        """
        Return a tuple of ints representing the database's shape.
        """
        return (self.row_count, self.col_count)

    def pretty_print(self, field_width=15, sep='| '):
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

    def add_cols(self, col_num_a, col_num_b, treat_as=None):
        for i in
        pass

    def sort_by_col(self, col):
        # TODO: implement a real sort, and return the sorted index mappings.
        # This implementation uses Python's built-in sort function,
        # and is also quite slow.
        items = [self.cols[col][i] for i in range(0, self.row_count)]
        newnums = [items.index(elt) for elt in sorted(items)]

        for i in range(0, self.row_count):
            self.row_map[i] = newnums[i]
