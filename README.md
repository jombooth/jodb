# jodb
primitive python datasheet system.

This datasheet system was developed to enable the rapid manipulation of csv files. It is capable
of performing high-speed lexicographic and numeric sorting (via the quicksort algorithm) of very large
files, and comes with an interpreter to process instructions on these datasheets via the command line.
Subsets of manipulated and/or sorted databases can then be written to disk through the interpreter via
the "filedump" instruction. All operations accessible via the interpreter can also be timed simply by
toggling time mode by entering "time".

Data in the datasheet is stored as strings, but its values can be manipulated as integers, floats,
or strings, conditional on what operation is being performed.

A general testing script, test.py, is provided, along with a performance testing script (test_big.py)
which demonstrates the sort performance (consistently under 5 seconds on the author's machine for a
10mb file).

Notable features:

Higher-order functions (map, reduce, two-column map (or BINOP)) implemented on columns.

Column operations for manipulating data, particularly in a statistical context, were then
implemented in terms of these higher-order functions.

Currently implemented:

    mean of column
    median of column
    variance of column
    maximum of column
    minimum of column

    exponentiation by n of a column
    mod by n of a column
    intification of a column
    floatification of a column
    stringification of a column

    addition of two columns (as strings, floats, or ints)
    subtraction of two columns (as floats or ints)
    multiplication of two columns (as floats or ints)
    division of two columns (as floats or ints)

And many more functions could readily be added simply by inserting additional higher-order
functions into the jo_db.py module and adding accessibility through the interpreter.


FILES:

jo_db.py             : Module containing the code for datasheets. Not directly accessed.

interpreter.py       : Loads the jo_db module. Then presents the user with a command-line interpreter
                       for manipulating, displaying, and timing operations on datasheets, as well as
                       loading them from files.

                       USAGE: python interpreter.py
                       Also possible: rlwrap python interpreter.py
                       (use rlwrap if you want to be able to press)
                       send 'help' for instructions.

test.csv             : A small csv file of integers used by the test.py script to verify basic functionality.

test.py              : Runs a battery of small tests on test.csv, and displays the results to the terminal.
                       visual inspection provides insight into the behavior of the system.

                       USAGE: python test.py

gen_100k_line_csv.py : Constructs a CSV file with 25 columns and 100000 rows of random integers.
                       Can be tweaked as needed to further profile the datasheet system's performance.

                       USAGE: python gen_100k_line_csv.py
                       and note that it outputs a file called 'big_table.csv'

test_big.py          : Loads big_table.csv and profiles the performance of repeatedly sorting the table
                       by its columns, printing this output to the terminal.

                       USAGE: python test_big.py
                       IMPORTANT: run gen_100k_line_csv.py before running this script.

The HELP string from interpreter.py is reproduced below:

        IO Operations:

        1)  load <name of file without extension>
            will load <name...>.csv into the program and bind the result to name
        2)  print <name>
            pretty_print whatever is stored in name
        3)  fieldwidth <number>
            set the pretty_print display field width to <number> characters
        4)  filedump <name> as <outputname>
            pretty_print whatever is stored in name to outputname.csv
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
            e.g. string comparisons are lexicographical, numeric comparisons are <
