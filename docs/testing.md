The program has cli/wrapper module "compress.py" in the main package, which has
no tests. This is because it's used for running the compression techniques and
displaying the results, and it's also changing quite a bit.

The lzw module has serialization methods in it, which have alot of tests
because there were problems initially to make these methods work as intended.
It was quite frustrating as it seemed to be working, but then some inputs
didn't work at all.

Writing the RLE and BWT was done mostly by writing the tests first, so there is
a lot of tests, probably few excessive ones. Most of the tests follow the same
practice as the earlier tests: first is empty input case, then one character
input length, then shorter and then lastly a bit longer input. Also few tests
for the whole RLE + BWT stack which check that the input and output matches
each other.


wip
