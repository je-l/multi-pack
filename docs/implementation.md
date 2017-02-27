The program consists of a lempel-ziv-welch -module, which has the algorithm
implementation, and serialization functions required by the algorithm.

Data structure module has implementation of hash table and linked list.
Compress module has mostly io and cli functionality in it.

Python is the used project language. It was picked so the project could also be
as an opportunity for using python in more concrete project. C would have been
another interesting choice, but i only know the basics, so the project could
have been too slowed down by the lack of skill.

### LZW time complexity comparison

Files used for testing were the MIT license file, first 10% lines from the
book, and the full book.

`du -b LICENSE`

`du --apparent-size -h book.txt book.short.txt`

|                      | file A      | file B      | file C      |
| -------------------- | ----------- | ----------- | ----------- |
| file size            | 1063 B      | 42 KB       | 417 KB      |
| final dict size      | 909         | 4096        | 4096        |
| compress time        | 15 ms       | 273 ms      | 2451 ms     |
| uncompress time      | 7 ms        | 96 ms       | 930 ms      |
| compression ratio    | 1.08        | 1.92        | 1.88        |
| compressed size %    | 92.3 %      | 52.1 %      | 53.3 %      |

LZW is running in linear O(n) time. The dictionary doesn't get full on the
small file test so the compression ratio is bad.

### BWT + RLE initial time complexity comparison

Tested files were MIT license file, and the same file repeated four times.

`du -b LICENSE license_x4.txt`

|                      | file A      | file B      |
| -------------------- | ----------- | ----------- |
| file size            | 1063 B      | 4252 B      |
| compress time        | 6 ms        | 30 ms       |
| uncompress time      | 3754 ms     | 145925 ms   |
| compression ratio    | 0.72        | 2.88        |
| compressed size %    | 138.3 %     | 34.7 %      |


The comparison shows that the BWT technique is currently running in polynomial time.
The compression ratio is also below 1.0 with the smaller file, because the bwt
can't form runs of same characters long enough. RLE stores the run count as a byte
so it will take more space, when there is multiple single character runs.

The compression runs in linear O(n) time, but the uncompression runs at very slow
polynomial O(n<sup>2</sup>) time.

#### BWT decoding pseudo code

ETX control character is added to the transformed text during compression.

```
inverse-bwt(s)
    T = [s1, s2,...,sn]
    for i = 0 to s.length
        A = [s.length]
        for j = 0 to s.length 
            A.prepend(s[j] + T[j])
        sort T
        table = T
    return row of T which ends to ETX
```

The sort function is currently the python default, which is O(n log n).
Sorting is done n times, so the complexity is polynomial.

Bwt can be done in linear time if we save an index array to the file.
Counting sort is suitable algorithm for this purpose.

wip
