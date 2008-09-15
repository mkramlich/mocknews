#!/usr/bin/env python2.5

import mocknews
#mocknews.main()

hlines = mocknews.headlines()
print str(hlines)
'''
for tock in sorted(hlines.keys()):
    for hl in hlines[tock]:
        print hl'''
