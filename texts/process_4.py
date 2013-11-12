#! /usr/bin/env python
# coding: utf8

import re
import sys


def main():
    abc = u'-йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
    dce = u',.;:!?—'
    #dce = u',;:!?—'
    ws = u' \t\n\r'

    state = 0
    words = []
    w = u''
    for c in sys.stdin.read().decode('utf8').strip():
        #print u'(%d, %s, %s)' % (state, c.lower(), w)
        if state == 0:
            if c == u'(':
                w = c
                state = 4
            elif c == u'«':
                w = c
                state = 5
            elif c in abc:
                w = c
                state = 1
            elif c in dce:
                w = c
                state = 2
            elif not c in ws:
                w = c
                state = 3
        elif state == 1:
            #print '[%s, %d]' % (c, c == '(')
            if c == u'(':
                w = c
                state = 4
            elif c == u'«':
                w = c
                state = 5
            elif c in abc: # + '.': # !!!
                w += c
            elif c in dce:
                words.append(w)
                w = c
            elif c in ws:
                words.append(w)
                w = u''
            else:
                words.append(w)
                w = c
                state = 3
        elif state == 2:
            if c in ws:
                words.append(w)
                w = u''
                state = 0
            elif c in abc:
                words.append(w)
                w = c
                state = 1
            elif c in dce:
                w += c
            else:
                words.append(w)
                w = c
                state = 3
        elif state == 3:
            if c == u'-':
                w += c
                state = 1
            elif c in abc:
                if w[-1] in dce:
                    words.append(w[:-1])
                    words.append(w[-1])
                else:
                    words.append(w)
                w = c
                state = 1
            elif not c in ws:
                w += c
        elif state == 4:
            w += c
            if c == ')':
                words.append(w)
                state = 0
        elif state == 5:
            w += c
            if c == u'»':
                words.append(w)
                state = 0
    if w[-1] in dce:
        words.append(w[:-1])
        words.append(w[-1])
    else:
        words.append(w)
    words = filter(lambda x: len(x), words)

    print u'\n'.join(words).encode('utf8')

if __name__ == '__main__':
    main()
