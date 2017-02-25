# multi-pack

Compression algorithm implementations in python

- Lempel-Ziv-Welch
- Burrow-wheeler transform with RLE

### [Test coverage](http://htmlpreview.github.io/?https://github.com/je-l/multi-pack/blob/master/docs/coverage-report/index.html)

### Requirements
* Python >=3.5.2 - older versions not tested

### Installation
`git clone`

### Usage
* cd to project root

* E.g. `python3 compress.py --lzw FILE`

Original file is preserved. Compressed file is `output.lzw` and decompressed
file is `output`

### Running tests

* cd to project root

* `python3 -m unittest -v`
