# -*- coding: utf8 -*-

import argparse
import os

import mclispy


parser = argparse.ArgumentParser()
parser.add_argument('lispfile', help='File path containing lisp code you want to run')

args = parser.parse_args()

if os.path.isfile(args.lispfile):
    print(mclispy.interpret(open(args.lispfile).read()))
else:
    print('file %s does not exists' % args.lispfile)