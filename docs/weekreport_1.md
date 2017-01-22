**About 10 hours used during week one**

The project started with choosing the topic. I wanted to create a command line
program for algorithms with good resources available, so compression algorithms
seemed like a good choice. Python was chosen for the language mainly for having
a change from java, which was used in previous project. My previous experience
in python is mainly short one-file programs made without IDE, so setting up the
IDE and project structure took some time. Also there were some clumsy errors
with relative imports, but they are now solved. Lot of time was spent looking
for material and examples of the algorithms, so very little actual programming
was done.

The program now consists of LZW encoding example, which does not write the
output into any file yet. The example is the same as here:

[https://www.cs.duke.edu/csed/curious/compression/lzw.html](https://www.cs.duke.edu/csed/curious/compression/lzw.html)

The dictionary is small-scale version of the full 256 character dictionary,
currently having 5 chars initially, and no upper bound for stored strings. The
program prints encoded output and final dictionary for the string "banana
bandana". The dictionary and encoded output is the same as in the link above.
All of the data structures are currently built-in versions.

This week i mainly learned some basic techniques used in compression algorithms
and details about python development. Two common techniques for compression
seem to be dictionary-, and entropy-based algorithms. Both aim for removing
repeated information from the data so that space is saved. Python documentation
conventions and testing modules are now a bit more familiar.

### Difficulties

Deciding about class structure and instance variables. Also some details about
BWT algorithm.

### Questions

Mutation testing and line coverage reports are not a requirement during this
course right?

### Next week

Implementing the full-scale LZW encoder with output into a file, and also begin
writing the decoder. Also planning of the BWT algorithm.
