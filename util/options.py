#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : options.py
# @Date    : 2018-11-13
# @Author  : qitian
import os
from optparse import OptionParser
import os, getopt
import sys


def show_usage():
    print('''
         -p    specify the project path 
         -m    only contain merge request commits or not, specify -m means only contain merge request
         -o    specify the output release note file,it can be a directory or a file with relative or absolutely path
         -v    specify the version of this release,this parameter must specify

     ''')

def parse_options():

    p = OptionParser()

    p.add_option("-p", "--project path", dest="project_path", type="string",
                 help="specify the project path"
                 )
    p.add_option("-v", "--version", dest="version", type="string",
                 help="specify the rlease note version"
                 )

    p.add_option("-m", "--merges", dest="merges", type="string",
                 help="specify get git log with merges request or not"
                 )

    p.add_option("-o", "--output", dest="output", type="string",
                 help="specify output path of release note"
                 )

    (opts, args) = p.parse_args()

    # default branch name is master
    if not opts.project_path:
        opts.project_path = os.getcwd()

    if not opts.version:
        print("请输入此次生成的rleasenote 的版本号")
        show_usage()
        exit(1)

    return opts, args

if __name__ == '__main__':

    options, args = parse_options()
    print(options.version)
    print(options.project_path)