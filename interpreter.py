import jo_db, time, os

def gets():
    return raw_input("> ")

# TODO: implement timer, implement filedumper

HELP =  """
        USAGE:

        IO Operations:

        1)  load <name of file without extension>
            will load <name...>.csv into the program and bind the result to name
        2)  print <name>
            pretty_print whatever is stored in name
        3)  fieldwidth <number>
            set the pretty_print display field width to <number> characters
        4)  filedump <name> <outputname>
            pretty_print whatever is stored in name to outputname.txt
        5)  shape <name>
            print the shape of the dataframe stored in name.
            can also be used to check whether a dataframe was loaded
            as it will print nothing if not.
        6)  exit (or quit)
            quits the interpreter
        7)  time
            switch command return timing on or off

        Assignment:

            The format here depends on <op>.

            General form: (subset is an exception)
            let <newname> = <op> <name> <col1> <col2/num/nothing> as <type>

            possible types: ints, floats, strings.

        1)  On two columns: <op> = add, sub, div, mul

            let <newname> = <op> <name> <col1> <col2> as <type>

        ex: let col1_plus_col2 = add dataframe 1 2 as strings
            let col2_times_col5 = mul dataframe 2 5 as floats
            let col2_divby_col3 = div dataframe 2 3 as ints

            and the results can be accessed through print or filedump.

        2)  On one column and one number: <op> = pow, mod

            let <newname> = <op> <name> <col1> <num> as <type>

        ex: let col1_tothe_5thpower = pow dataframe 1 5.0 as floats
            let col5_mod_2 = mod dataframe 5 2 as ints

        3)  On one column only: <op> = stringify, intify, floatify

            let <newname> = <op> <name> <col1>

        ex: let col5_ints = intify dataframe 5
            let col3_floats = floatify dataframe 3

        4)  Subsetting by column

            let <subsetname> = subset <name> num_1,num_2,...,num_n

        ex: let subset_rows_1_2_and_5 = subset dataframe 1,2,5
            let subset_row_8 = subset dataframe 8

        Reductions:

            General form:
            <reduct_op> <colnum> in <name> as <type>

            <reduct_op> = var (variance), sum, avg, max, min, med (median)

        ex: var 4 in planes_data as floats
            sum 2 in dataframe as ints
            max 5 in rainfall_data as ints

        Sorting:

            sort <name> by <col> as <type> <order>

            <order> = asc, desc
            <col> = column number

        ex: sort big_table by 2 as floats desc
            sort phonebook by 6 as strings asc

            note that <type> specifies the type of comparison
            e.g. strings is lexicographical, numeric comparisons are <
        """

KEYWORDS = ['load', 'sort', 'print', 'shape', 'as', 'int', 'float', 'str', \
            'variance', 'let', 'avg', 'mod', 'filedump', 'subset' ]

TYPES = ['ints', 'strings', 'floats']

namespace = {}
time_return_wait = False
fieldwidth = 7

while 1:
    try:
        if time_return_wait:
            print "ELAPSED TIME: %f seconds." % (time.time() - start)

        ipt = filter(None, gets().split(' '))
        # print ipt

        start = time.time()

        # SWITCH COMMAND TIMING MODE ON OR OFF

        if ipt[0] == 'time':
            time_return_wait = not time_return_wait

        elif ipt[0] == 'usage' or ipt[0] == 'help':
            print HELP

        elif ipt[0] == 'exit' or ipt[0] == 'quit' or ipt[0] == 'q':
            print "good-bye."
            os._exit(1)

        # FUNDAMENTAL OPERATORS FOR IO

        elif ipt[0] == 'load':
            if len(ipt) == 2:
                assert ipt[1] not in KEYWORDS
                fd = open(ipt[1] + '.csv', 'r')
                namespace[ipt[1]] = jo_db.DataSheet(fd)
                fd.close()

        elif ipt[0] == 'print':
            if len(ipt) == 2:
                if ipt[1] in namespace:
                    namespace[ipt[1]].pretty_print(field_width=fieldwidth)

        elif ipt[0] == 'fieldwidth':
            if len(ipt) == 2:
                fieldwidth = int(ipt[1])

        elif ipt[0] == 'filedump':
            pass

        elif ipt[0] == 'shape':
            if len(ipt) == 2:
                if ipt[1] in namespace:
                    print namespace[ipt[1]].shape()

        # THE ASSIGNMENT OPERATOR

        elif ipt[0] == 'let':
            to_assign = ipt[1]

            # let's not bind over keywords
            assert to_assign not in KEYWORDS
            assert ipt[2] == '='

            # OPERATOR ON N COLUMNS

            if ipt[3] == 'subset':
                if ipt[4] in namespace:
                    namespace[to_assign] = namespace[ipt[4]].subset([int(x) for x in ipt[5].split(',')])

            # OPERATORS ON TWO COLUMNS

            elif ipt[3] == 'add':
                assert ipt[7] == 'as'
                assert ipt[8] in TYPES
                typename = ipt[8]
                if ipt[4] in namespace:
                    namespace[to_assign] = namespace[ipt[4]].add_cols(int(ipt[5]), int(ipt[6]), as_types=typename)

            elif ipt[3] == 'sub':
                assert ipt[7] == 'as'
                assert ipt[8] in TYPES
                typename = ipt[8]
                if ipt[4] in namespace:
                    namespace[to_assign] = namespace[ipt[4]].sub_cols(int(ipt[5]), int(ipt[6]), as_types=typename)

            elif ipt[3] == 'div':
                assert ipt[7] == 'as'
                assert ipt[8] in TYPES
                typename = ipt[8]
                if ipt[4] in namespace:
                    namespace[to_assign] = namespace[ipt[4]].div_cols(int(ipt[5]), int(ipt[6]), as_types=typename)

            elif ipt[3] == 'mul':
                assert ipt[7] == 'as'
                assert ipt[8] in TYPES
                typename = ipt[8]
                if ipt[4] in namespace:
                    namespace[to_assign] = namespace[ipt[4]].mul_cols(int(ipt[5]), int(ipt[6]), as_types=typename)

            # OPERATORS ON ONE COLUMN, ONE NUMBER

            elif ipt[3] == 'pow':
                assert ipt[7] == 'as'
                assert ipt[8] in TYPES
                typename = ipt[8]
                if ipt[4] in namespace:
                    if typename == 'floats':
                        namespace[to_assign] = namespace[ipt[4]].pow_col(int(ipt[5]), float(ipt[6]), as_types=typename)
                    else:
                        namespace[to_assign] = namespace[ipt[4]].pow_col(int(ipt[5]), int(ipt[6]), as_types=typename)

            elif ipt[3] == 'mod':
                assert ipt[7] == 'as'
                assert ipt[8] in TYPES
                typename = ipt[8]
                if ipt[4] in namespace:
                    if typename == 'floats':
                        namespace[to_assign] = namespace[ipt[4]].modn_col(int(ipt[5]), float(ipt[6]), as_types=typename)
                    else:
                        namespace[to_assign] = namespace[ipt[4]].modn_col(int(ipt[5]), int(ipt[6]), as_types=typename)

            # OPERATORS ON ONE COLUMN

            elif ipt[3] == 'intify':
                if ipt[4] in namespace:
                    namespace[to_assign] = namespace[ipt[4]].intify_col(int(ipt[5]))

            elif ipt[3] == 'floatify':
                if ipt[4] in namespace:
                    namespace[to_assign] = namespace[ipt[4]].floatify_col(int(ipt[5]))

            elif ipt[3] == 'stringify':
                if ipt[4] in namespace:
                    namespace[to_assign] = namespace[ipt[4]].stringify_col(int(ipt[5]))

        # REDUCTION (single-output) OPERATORS

        elif ipt[0] == 'var':
            assert ipt[2] == 'in'
            if ipt[3] in namespace:
                print namespace[ipt[3]].var_col(int(ipt[1]))

        # TYPED REDUCTION (single-output) OPERATORS
        # TODO: maybe don't insist on type specification?
        elif ipt[0] == 'min':
            assert ipt[2] == 'in'
            assert ipt[4] == 'as'
            assert ipt[5] in TYPES
            typename = ipt[5]

            if ipt[3] in namespace:
                print namespace[ipt[3]].min_col(int(ipt[1]), as_type=typename)

        elif ipt[0] == 'max':
            assert ipt[2] == 'in'
            assert ipt[4] == 'as'
            assert ipt[5] in TYPES
            typename = ipt[5]

            if ipt[3] in namespace:
                print namespace[ipt[3]].max_col(int(ipt[1]), as_type=typename)

        elif ipt[0] == 'avg':
            assert ipt[2] == 'in'
            assert ipt[4] == 'as'
            assert ipt[5] in TYPES
            typename = ipt[5]

            if ipt[3] in namespace:
                print namespace[ipt[3]].avg_col(int(ipt[1]), as_type=typename)

        elif ipt[0] == 'sum':
            assert ipt[2] == 'in'
            assert ipt[4] == 'as'
            assert ipt[5] in TYPES
            typename = ipt[5]

            if ipt[3] in namespace:
                print namespace[ipt[3]].sum_col(int(ipt[1]), as_type=typename)

        elif ipt[0] == 'med':
            assert ipt[2] == 'in'
            assert ipt[4] == 'as'
            assert ipt[5] in TYPES
            typename = ipt[5]

            if ipt[3] in namespace:
                print namespace[ipt[3]].med_col(int(ipt[1]), as_type=typename)

        # SORTING OPERATOR

        elif ipt[0] == 'sort':
            assert len(ipt) == 7
            assert ipt[2] == 'by'
            assert ipt[4] == 'as'
            assert ipt[5] in TYPES
            assert ipt[6] in ['asc', 'desc']
            typename, order = ipt[5], ipt[6]

            if ipt[1] in namespace:
                namespace[ipt[1]].sort_by_col(int(ipt[3]), compare_as=typename, order=order)

        else:
            print "Didn't understand that query."
    except:
        print "Query malformed, or interrupt sent."
