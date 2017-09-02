import os
import re
import sys
import getopt

from typing import List

# example:
# python rename.py . "([^\.]+)\.log\.(.+)" "\1.\2.log"


def rename_regex(filenames: List[str], patt: str, rep: str):
    for filename in filenames:
        # print(filename)
        matched = re.match(patt, filename)
        if matched:
            new_name = re.sub(patt, rep, filename)
            print('rename {} to: {}'.format(filename, new_name))
            try:
                os.rename(filename, new_name)
            except FileExistsError as e:
                print(e)
                os.remove(filename)
                print('{} removed.'.format(filename))
                pass


if __name__ == '__main__':
    s_opt = 'i:o:r'
    l_opt = ['input-format=', 'output-format=', 'regex']
    optlist, args = getopt.getopt(sys.argv, s_opt, l_opt)
    argv = sys.argv
    print(argv)
    print((optlist, args))

    path_arg = argv[1]
    patt = argv[2]
    rep = argv[3]

    file_path = os.path.abspath(path_arg)
    filenames = os.listdir(file_path)

    # print(filenames)
    os.chdir(file_path)
    rename_regex(filenames, patt, rep)
