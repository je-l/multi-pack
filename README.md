# multi-pack

Compression algorithm implementations in python

- Lempel-Ziw-Welch
- Burrow-wheeler transform with RLE
- ...

### Requirements
* Python >3.5.2 - older versions not tested
* [BitString module](https://pypi.python.org/pypi/bitstring) (MIT license)


### Installation
`git clone`

### Usage
`cd multi-pack/compression`

`python3 compress.py`

Currently only simple LZW encoding/decoding example is printed, as seen [here](https://www.cs.duke.edu/csed/curious/compression/lzw.html)

### Running tests
For example [nose2](https://github.com/nose-devs/nose2) or pycharm builtin testing module.

`cd multi-pack`

`nose2`
