The program works by selecting the preferred compression technique and file.
The original file is not preserved. The compressed file has the same name plus
suffix which indicates the used compression technique. The suffix is used to
determine the file contents so do not change it. The LZW is for text and binary
files. **The BWT is only for text files.**

It is possible to compress using both BWT and LZW. But only by using BWT first.

The program is completely portable, so there is no setup script. Add an alias
to .bashrc so that the program can be run more conveniently:

`alias multi-pack="python3 ~/path/to/repo/compress.py"`

`source ~/.bashrc`

### Examples:

Compression:

`python3 compress.py --lzw manual.md`

Uncompression:

`python3 compress.py --lzw manual.md.lzw`

