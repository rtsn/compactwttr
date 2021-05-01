#!/usr/bin/env python3

""" A small script get weather infom from wttr.in via curl and remove
    colors and compact the output. """

import subprocess
import re
import sys

def split(tail):
    """ splits the tail wrt the boxes """
    chunk1 = []
    chunk2 = []

    for line in tail:
        chunk1.append(line[:63]+'\n')
        chunk2.append(line[63:])

    for i in chunk2[1:]:
        i = "│"+i+'\n'
        chunk1.append(i)
    return chunk1

def fix_formatting(chunk):
    """ fixes the quirks in the formatting """
    chunk[0] = chunk[0][:55]+"───────┐\n"
    chunk[1] = chunk[1][:55]+"       │\n"
    chunk[2] = chunk[2][:-2]+"┤\n"
    chunk[8] = "├"+chunk[8][1:31]+"┼"+chunk[8][32:-2]+"┤\n"
    chunk[9] = chunk[9][0]+"       "+chunk[9][8:]
    chunk[10] = "├"+chunk[10][1:]
    chunk[16] = "└"+chunk[16][1:]
    return chunk

def remove_colors(string):
    """removes ANSI color codes from string
       https://stackoverflow.com/a/14693789/6586742 """

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', string).split('\n')
    return result

def main():
    """ all args to string. start curl subprocess to get data, remove
    colors, compact and fix output"""
    city = ' '.join(sys.argv[1:])
    cmd = ["curl", "-s", "wttr.in/"+city]

    output = subprocess.check_output(cmd).decode('utf-8')

    output = remove_colors(output)

    head = "\n".join(output[:7])
    tail = output[8:-24]

    tail = split(tail)
    tail = fix_formatting(tail)
    tail = "".join(tail)

    print(head+'\n'+tail)

if __name__ == "__main__":
    main()
