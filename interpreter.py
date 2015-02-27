import jo_db

def gets():
    return raw_input("> ")

# TODO: implement timer, implement filedumper

KEYWORDS = ['load', 'sort', 'print', 'shape', 'as', 'int', 'float', 'str', \
            'variance', 'let', 'avg', 'mod', 'filedump', 'subset' ]

TYPES = ['ints', 'strings', 'floats']

namespace = {}

while 1:
    ipt = filter(None, gets().split(' '))
    print ipt

    # FUNDAMENTAL OPERATORS FOR IO

    if ipt[0] == 'load':
        if len(ipt) == 2:
            assert ipt[1] not in namespace
            fd = open(ipt[1] + '.csv', 'r')
            namespace[ipt[1]] = jo_db.DataSheet(fd)
            fd.close()

    elif ipt[0] == 'print':
        if len(ipt) == 2:
            if ipt[1] in namespace:
                namespace[ipt[1]].pretty_print()

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
            typename = ipt[8]
            if ipt[4] in namespace:
                namespace[to_assign] = namespace[ipt[4]].add_cols(int(ipt[5]), int(ipt[6]), as_types=typename)

        elif ipt[3] == 'sub':
            assert ipt[7] == 'as'
            typename = ipt[8]
            if ipt[4] in namespace:
                namespace[to_assign] = namespace[ipt[4]].sub_cols(int(ipt[5]), int(ipt[6]), as_types=typename)

        elif ipt[3] == 'div':
            assert ipt[7] == 'as'
            typename = ipt[8]
            if ipt[4] in namespace:
                namespace[to_assign] = namespace[ipt[4]].div_cols(int(ipt[5]), int(ipt[6]), as_types=typename)

        elif ipt[3] == 'mul':
            assert ipt[7] == 'as'
            typename = ipt[8]
            if ipt[4] in namespace:
                namespace[to_assign] = namespace[ipt[4]].mul_cols(int(ipt[5]), int(ipt[6]), as_types=typename)

        # OPERATORS ON ONE COLUMN, ONE NUMBER

        elif ipt[3] == 'pow':
            assert ipt[7] == 'as'
            typename = ipt[8]
            if ipt[4] in namespace:
                if typename == 'floats':
                    namespace[to_assign] = namespace[ipt[4]].pow_col(int(ipt[5]), float(ipt[6]), as_types=typename)
                else:
                    namespace[to_assign] = namespace[ipt[4]].pow_col(int(ipt[5]), int(ipt[6]), as_types=typename)

        elif ipt[3] == 'mod':
            assert ipt[7] == 'as'
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
        typename = ipt[5]

        if ipt[3] in namespace:
            print namespace[ipt[3]].min_col(int(ipt[1]), as_type=typename)

    elif ipt[0] == 'max':
        assert ipt[2] == 'in'
        assert ipt[4] == 'as'
        typename = ipt[5]

        if ipt[3] in namespace:
            print namespace[ipt[3]].max_col(int(ipt[1]), as_type=typename)

    elif ipt[0] == 'avg':
        assert ipt[2] == 'in'
        assert ipt[4] == 'as'
        typename = ipt[5]

        if ipt[3] in namespace:
            print namespace[ipt[3]].avg_col(int(ipt[1]), as_type=typename)

    elif ipt[0] == 'sum':
        assert ipt[2] == 'in'
        assert ipt[4] == 'as'
        typename = ipt[5]

        if ipt[3] in namespace:
            print namespace[ipt[3]].sum_col(int(ipt[1]), as_type=typename)

    elif ipt[0] == 'med':
        print "NOT YET IMPLEMENTED"
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
