# multi-pack

Compression algorithm implementations in python

1. Lempel-Ziv-Welch
2. Burrow-wheeler transform with RLE

### Docs

* [Test coverage](http://htmlpreview.github.io/?https://github.com/je-l/multi-pack/blob/master/docs/coverage-report/index.html)

* [Design](docs/design.md)

* [Benchmarks / implementation](docs/implementation.md)

* [Testing](docs/testing.md)

* [Manual](docs/manual.md)

### Requirements

Python >=3.5.2 - older versions not tested

### Installation

`git clone`

### Usage
* Cd to project root

* Compress: `python3 compress.py --lzw FILE`

* Uncompress: `python3 compress.py --lzw FILE.lzw`

* To uncompress files, the selected technique must match with the suffix

### Running tests

* cd to project root

* `python3 -m unittest -v`
