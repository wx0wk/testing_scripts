from os import path
import sys
from subprocess import call

with open(sys.argv[1]) as diff_file:
    lines = diff_file.readlines()
    for line in lines:
        print(line, end='')
        s = line.split(' ')
        l = s[1]
        r = s[3]
        if path.isfile(l) or path.isfile(r):
            call(['vimdiff', l, r])
