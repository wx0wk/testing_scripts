from os import path
import sys
from subprocess import call

## diff -rqN -X $1/.gitignore $1 $2 | grep -Ev 'static|templates|media|\.conf' > diff_files.txt

try:
    diff = sys.argv[2]
except KeyError:
    diff = 'diff'

with open(sys.argv[1]) as diff_file:
    lines = diff_file.readlines()
    for line in lines:
        print(line, end='')
        s = line.split(' ')
        l = path.abspath(s[1])
        r = path.abspath(s[3])
        if path.isfile(l) or path.isfile(r):
            call([diff, l, r])
