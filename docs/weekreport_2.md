Used about 12 hours for week 2

This week was spent mainly implementing the uncompression, and writing/reading
of the compressed files. Python seems to only support writing data byte by
byte, so i spent a lot of time converting the 12-bit indices to bytes. Later i
used a module for reading the compressed binary file, but i plan not to use it
later, just like the built-in data structures. Initially i thought the bitwise
methods worked fine, but they actually didn't. So i made lots of tests for them
since they are pretty easy to test for.

The LZW compression should be soon ready, as the most complicated parts are now
done. I need to use full-scale dictionary and fix the lost data with non-even
bytes.

Definitely the hardest part this week was the bitwise operations, which i used
to convert the 12-bit indices to bytes. Bit manipulation is totally new for me
so it took a lot of time.

Next week i should get the lzw working with real files and see how well it
performs. If all goes well i will start making the next compression algorithm.
