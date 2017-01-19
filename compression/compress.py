#!/usr/bin/python3
#  -*- coding: utf-8 -*-

"""Main class for """


def compress(file_input):
    """Compress input file using LZW compression algorithm.
    :param file_input:
    :return: compressed output
    """
    # TODO
    return len(file_input.read())


def main():
    """Main function"""
    with open("../LICENSE") as in_file:
        output = compress(in_file)
        print(output)

if __name__ == "__main__":
    main()
