# Design description

Multi-pack is a command line program for compressing files with various
compression techniques. First one is Lempel-Ziw-Welch, a dictionary based
algorithm which offers low compression ratio but fast execution and low memory
usage.

Other algorithms could be Burrow-Wheeler transform and run-length encoding,
which are very different techniques used in data compression. If
implementations turn out to be more difficult than expected, only two
algorithms will be included.


### Algorithms and data structures

During encoding, Lempel-Ziw-Welch (LZW) uses a dictionary to store recurring
patterns in a file, storing them as indexes in a dictionary to save space. The
dictionary is continuously checked if a specific pattern is stored, so O(1)
search time complexity is a must. Suitable data structure would be hash table
with strings as keys and integer indexes as values.

The decoder only needs to have O(1) index access, so a string array should be
sufficient for the dictionary data structure.

BWT uses a table with different rotations of a string. The table is sorted and
the last column is given as output. This would be O(n log(n)) because of the
sorting.

### Input handling

User gives the wanted compression algorithm and the file name as arguments to
the program. File is then encoded, and the file name will be changed to
represent the used algorithm. The original file is not preserved.

`python3 compress.py --lzw book.txt`

For example `book.txt` will be then changed to `book.txt.lzw`

running with `--verbose` argument would print the compression ratio etc.

### Desired time and space complexities

Time complexity for LZW encoding and decoding should be O(n), as values
are retrieved from the dictionary in constant time, only once.

Compression ratios close to the values mentioned in the original LZW paper.

BWT could be made to O(n) time complexity, but it seems to require complex
optimisation so O(n log(n)) is the goal.


### References

Very nice overview of LZW with good pseudo codes. This was used a lot.
* [https://www.cs.duke.edu/csed/curious/compression/lzw.html](https://www.cs.duke.edu/csed/curious/compression/lzw.html)

Goal compression ratios from LZW paper (page 12).
* [http://www.cs.duke.edu/courses/spring03/cps296.5/papers/welch_1984_technique_for.pdf](http://www.cs.duke.edu/courses/spring03/cps296.5/papers/welch_1984_technique_for.pdf)

* [https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform](https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform)
