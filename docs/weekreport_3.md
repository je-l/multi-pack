Around 10 hours used for week 3

This week was again used for writing the lzw compression. Some refactoring was
done and unnecessary code was removed. The bitstring module is no longer
needed, as the binary reading was surprisingly straightforward to implement. I
also looked up about how linked lists and hash tables were implemented in java
and python, so i can now start to work on those. Test coverage is now included.
Htmlpreview acted weird but it works 90% of the time.

The program has now working lzw compression, which should work on all kinds of
files. At the beginning of the week the performance was really bad, but changes
to the uncompression and stream reading made it good enough. The reading
and writing also works now without any third party modules. 

Next week i work on the data structures and start making the BWT part.
