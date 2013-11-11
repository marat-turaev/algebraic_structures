#! /usr/bin/env python
# coding: utf8

import re
import sys


def main():
    raw = sys.stdin.read().strip()
    raw = re.sub('(?m)^.?\d+[\.\)]? ?', '', raw)
    raw = re.sub('-[\n\r]{1,2}', '', raw)
    raw = re.sub('([,:;\.\?])', ' \g<1> ', raw)
    raw = re.sub('\s+', ' ', raw)
    #raw = re.sub('\(cid:.*?\)', '', raw)
    raw = re.sub('\(.*?\)', '', raw)

    tokens = ['$f$' if re.match('(?i)[^\?\.,:;а-яё]|[·ϕα\d]', t) else t
              for t in raw.split()]
    text = ' '.join(tokens)
    text = re.sub('[,:; \.\?]{4,}', '$f$', text)
    text = re.sub('\$f\$(?:[,:; \.\?]|(?:\$f\$))+\$f\$', '$f$', text)

    print text


if __name__ == '__main__':
    main()
