#!/usr/bin/env python3
import re
import sys,gzip,bz2
import fileinput
import argparse
from collections import namedtuple


def get_args():
    parser = argparse.ArgumentParser(description = __doc__, formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument("input", nargs="?", default=None, help="hmmsearch output. [stdin]")
    args = parser.parse_args()
    return args


## 不同的压缩格式
def myread(inf):
    return open(inf, 'rt')

def get_input(inf):

    if inf:
        try:
            myread(inf)
        except FileNotFoundError:
            sys.stderr.write(f"ERROR: can't open file: {inf}")
            sys.exit(1)
    else:
        return sys.stdin


def is_overlap(query:tuple, ranges:tuple):
    '''
        query = (q_start, q_end, q_type, q_clan)
        ranges = ((start, end, type, clan), (start, end, type, clan))
    '''
    q_start, q_end, q_type, q_clan = query
    if q_type in ['Domain', 'Family']:
        q_type = "Domain/Family"
    for (ref_start, ref_end, ref_type, ref_clan) in ranges:
        if q_start <= ref_end and q_end >= ref_start:
            if ref_type in ['Domain', 'Family']:
                ref_type = "Domain/Family"
            if ( q_clan != ref_clan ) or (q_type != ref_type):
            # 1、就算重叠了，
            #   1.1 如果不是同一个clu
            #   1.2 或者不是相同的类型(Domain/Family, Motif) ## Family和Domain冲突
            #   那也不算重叠
                continue
            return True
    return False


def parse_line(text):
    split = text.rstrip("\n").split("\t")
    name, start, end, type_, clan = split[0], split[1], split[2], split[7], split[-2]
    return (name, start, end, type_, clan)
    

def main(args):

    f = get_input(args.input)
    ranges = []

    ## 先解析第一个结果
    first_line = f.readline()
    last_name, start, end, type_, clan = parse_line(first_line)
    ranges.append((int(start), int(end), type_, clan))
    sys.stdout.write(first_line)

    ## 然后解析剩下的结果
    for line in f:
        name, start, end, type_, clan = parse_line(line.rstrip("\n"))
        start, end = int(start), int(end)
        q_cont = (start, end, type_, clan)
        ## 如果名字不一样，直接打印
        if name != last_name:
            sys.stdout.write(line)
            ranges = [(start, end, type_, clan)]

        elif not is_overlap( q_cont, ranges):
            ## 如果不重叠,就添加新的已经打印的区间
            ranges.append(q_cont)
            sys.stdout.write(line)
        last_name = name


if __name__ == "__main__":
    args = get_args()
    main(args)
