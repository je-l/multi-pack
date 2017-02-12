The program has cli/wrapper module "compress.py" in the main package, which has
no tests. This is because it's used for running the compression techniques and
displaying the results, and it's also changing quite a bit.

The lzw module has serialization methods in it, which have alot of tests
because there were problems initially to make these methods work as intended.
It was quite frustrating as it seemed to be working, but then some inputs
didn't work at all.

wip
