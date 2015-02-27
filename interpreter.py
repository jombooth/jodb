import jo_db

def gets():
    return raw_input("> ")

KEYWORDS = ['load', 'sort', 'print', 'shape', 'as', 'int', 'float', 'str', \
            'variance', 'set', 'avg', 'mod', 'filedump', 'subset' ]

namespace = {}

while 1:
    ipt = filter(None, gets().split(' '))
    print ipt

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

    elif ipt[0] == 'set':
        to_assign = ipt[1]

        assert to_assign not in KEYWORDS
        assert ipt[2] == '='

        if ipt[3] == 'subset':
            if ipt[4] in namespace:
                namespace[to_assign] = namespace[ipt[4]].subset([int(x) for x in ipt[5].split(',')])

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

    elif ipt[0] == 'variance':
        pass
    elif ipt[0] == 'sum':
        pass
    elif ipt[0] == 'mean':
        pass
    elif ipt[0] == 'sort':
        pass
