
class DataSheet(dict):
    def __init__(self, data_file=None):
        self.cols = {}
        self.row_map = {}
        self.row_count = 0
        self.col_count = 0

        if data_file is not None:
            data = data_file.read()
            rows = [row for row in data.split('\n') if row.strip() != ""]
            self.row_count = len(rows)

            for i in range(0, self.row_count):
                # "sorting" the database is equivalent to changing the row_map
                # int -> int mapping
                self.row_map[i] = i

                row_fields = rows[i].split(",")

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
        return (self.row_count, self.col_count)

    def pretty_print(self, field_width=15, sep="| "):

        def fill_to_width(field):
            """
            Given a field to be displayed, space-pad or truncate it to field_width.
            """
            if len(field) <= field_width:
                field += " " * (field_width - len(field))
            return field[:field_width]

        # find with of rendered database endcaps
        cap_width = ((field_width + len(sep)) * self.col_count + 1)

        print "_" * cap_width

        for i in range(0, self.row_count):
            row_buf = sep

            for j in range(0, self.col_count):

                try:
                    row_datum = self.cols[j][self.row_map[i]]

                    row_buf += fill_to_width(row_datum) + sep
                except KeyError:
                    row_buf += fill_to_width("NULL") + sep

            print row_buf + "<- row %s, maps to row %s" % (str(i), str(self.row_map[i]))

        print "*" * cap_width

    def add_cols(self, col_num_a, col_num_b, treat_as=None):
        pass

    def sort_by_col(col):
        pass
        pass # in the column,
