# multi-pack

Compression algorithm implementations in python

- Lempel-Ziv-Welch
- Burrow-wheeler transform with RLE
- ...

### [Test coverage](http://htmlpreview.github.io/?https://github.com/je-l/multi-pack/blob/master/docs/coverage-report/index.html)

### Requirements
* Python >=3.5.2 - older versions not tested

### Installation
`git clone`

### Usage
`cd multi-pack/compression`

`python3 compress.py FILE`

Original file is preserved. Compressed file is `output.lzw` and decompressed file is `output`

### Running tests
Using for example [nose2](https://nose2.readthedocs.io/en/latest/) or pycharm built-in testing module.

`cd multi-pack`

`nose2 --verbose`
