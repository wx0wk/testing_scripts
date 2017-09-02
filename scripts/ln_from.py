from os import path
import sys
from subprocess import call

print(sys.argv)

full_f = str(sys.argv[1])
sp = full_f.rsplit('/', 1)
f = sp[-1]
try:
    d = sp[-2]
except IndexError:
    print('Cannot ln from same folder.')
    exit()

try:
    t = sys.argv[2]
except IndexError as ie:
    t = f

print(d, f)
d = path.abspath(d)
call(['ln', '-s', '{}/{}'.format(d, f), t])
