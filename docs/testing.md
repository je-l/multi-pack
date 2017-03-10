The program has CLI/wrapper module "compress.py" in the main package, which has
no tests. This is because it's used for running the compression techniques and
displaying the results, and it's also changing quite a bit.

The lzw module has serialization methods in it, which have a lot of tests
because there were problems initially to make these methods work as intended.
It was quite frustrating as it seemed to be working, but then some inputs
didn't work at all.

Writing the RLE and BWT was done mostly by writing the tests at the same time,
so there is a lot of tests, probably few excessive ones. Most of the tests
follow the same practice as the earlier tests: first is empty input case, then
one character input length, then shorter and then lastly a bit longer input.
Also few tests for the whole RLE + BWT stack which check that the input and
output matches each other.

The data structures and sorting functions have similiarly the edge case tests
and few tests with different inputs. The counting_sorted() function has test
for numeric inputs and byte array inputs, so that both use cases are covered.

Additionally there was some minimal system testing with a small bash script:

```bash
#!/usr/bin/env bash

python3 compress.py --bwt kern.log.1
python3 compress.py --bwt kern.log.1.bwt
diff kern.log.1 kern.log.1.bak
python3 compress.py --lzw kern.log.1
python3 compress.py --lzw kern.log.1.lzw
diff kern.log.1 kern.log.1.bak
```

The script would print the diff if the processed file didn't match the backup.
