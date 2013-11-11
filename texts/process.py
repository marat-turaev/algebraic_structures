#! /usr/bin/env python
#coding: utf8

import re
import sys


def main():
    text = sys.stdin.read().strip()
    text = re.sub('(?m)^.?\d+[\.\)]? ?', '', text)
    text = re.sub('-[\n\r]{1,2}', '', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub('\(cid:.*?\)', '', text)
    text = re.sub('\((?:ср|см).*?\)', '', text)
    #text = re.sub('\w', '$formula$', text)
    print text


if __name__ == '__main__':
    main()
