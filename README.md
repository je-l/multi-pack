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
* Cd to project root

* E.g. `python3 compress.py --lzw FILE`

* Lzw compressed files have `.lzw` suffix and bwt compressed files have `.bwt`
  suffix

* To uncompress files, the selected technique must match with the suffix

### Running tests

* cd to project root

* `python3 -m unittest -v`
