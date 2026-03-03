#!/usr/bin/env python3

from collections import namedtuple
import argparse


def get_args():
    parser = argparse.ArgumentParser(description = __doc__, formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument("dat1", default=None, help="pfam dat")
    parser.add_argument("dat2", default=None, help="activate dat")
    parser.add_argument("output", default=None, help="output. [stdout]")
    args = parser.parse_args()
    return args


#==========================================================
def parse_dat(inf, out, as_dat):

    PfamEntry = namedtuple(
            'PfamEntry', ['id', 'ac', 'de', 'ga_seq', 'ga_dom', 'type', 'clan', 'acs'])

    f2 = open(out, 'w')
    f = open(inf, 'rt')

    # entries = []
    current = {}

    f2.write(f"ACC\tTYPE\tGA_seq\tGA_domain\tactivate_site\tclan\tname\tDescription\n")
    for line in f:
        line = line.strip("\n")
        if not line or line.startswith("# "):
            continue

        if line == '//':
            if current.get("id"):

                ga = current.get('ga', '0; 0;').split(';', 1)
                ga_seq, ga_dom = [ float(x) for x in ga ]
                entry = PfamEntry(
                    id     = current.get('id'),
                    ac     = current.get('ac'),
                    de     = current.get('de'),
                    ga_seq = ga_seq,
                    ga_dom = ga_dom,
                    type   = current.get('tp'),
                    clan   = current.get('cl','No_clan'),
                    acs     = as_dat.get(current.get('id'),'')
                    )
                f2.write(f"{entry.ac}\t{entry.type}\t{entry.ga_seq}\t{entry.ga_dom}\t{entry.acs}\t{entry.clan}\t{entry.id}\t{entry.de}\n")
                # entries.append(entry)
            current = {}
        elif line.startswith('#=GF '):
            tag = line[5:7]
            value = line[10:].strip().rstrip(';')
            current[tag.lower()] = value
    f.close()
    f2.close()

    # return entries

def parse_as_dat(inf):
    f = open(inf, 'rt')
    res = {}
    for line in f:
        line = line.rstrip("\n")
        if line.startswith("ID "):
            res[line[4:]] = 'predicted_active_site'
    f.close()
    return res


if __name__ == "__main__":
    args = get_args()

    as_dat = parse_as_dat(args.dat2)

    parse_dat(args.dat1, args.output, as_dat)
    
