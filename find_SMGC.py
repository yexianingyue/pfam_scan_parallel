#!/share/data1/software/miniconda3/bin/python
# -*- encoding: utf-8 -*-
"""
Author:    	夜下凝月 2019年12月4日	 星期三
Description:	寻找pfam/InterProscan注释结果中的次级代谢物簇

=================================================================================================================
CITATION:
    If you use this software, please cite:

[1] Yan, Qiulong et al.
      A genomic compendium of cultivated human gut fungi characterizes the gut mycobiome and its relevance to common diseases
      Cell, Volume 187, Issue 12, 2969 - 2989.e24 doi:10.1016/j.cell.2024.04.043

[2] Vesth, T.C., Nybo, J.L., Theobald, S. et al.
      Investigation of inter- and intraspecies variation through genome sequencing of Aspergillus section Nigri.
      Nat Genet 50, 1688–1695 (2018) doi:10.1038/s41588-018-0246-1

=================================================================================================================
"""

"""
[3] Medema MH, Blin K, Cimermancic P, et al.
      antiSMASH: rapid identification, annotation and analysis of secondary metabolite biosynthesis gene clusters
      in bacterial and fungal genome sequences.
      Nucleic Acids Res. 2011;39(Web Server issue):W339–W346. doi:10.1093/nar/gkr466
"""
from typing import Optional
import argparse
import re

def taxo_pfam(hmm_acc: list) -> Optional[str]:
    '''
    根据列表中的PF，判断它属于哪个簇，返回簇名
    '''
    hmm_acc_set = set(hmm_acc)
    # 因为杂合子是NRPS 和 PKS的并集，所以先判断这个，否则会误判为其中一个
    if hmm_acc_set & Hybrid == Hybrid:
        return 'Hybrid'  
    elif hmm_acc_set & NRPS == NRPS:
        return 'NRPS'
    elif set(hmm_acc) & PKS == PKS:
        return 'PKS'
    elif set(hmm_acc) & PKS == PKS_like:
        return 'PKS-like'
    elif set(hmm_acc) & DMAT == DMAT:
        return 'DMAT'
    elif set(hmm_acc) & Terpene != set():  # 如果没有交集，python会返回   set()   因此，不能使用  {} 作为判断标准
        return 'Terpene cyclase/synthase'
    elif len(set(hmm_acc) & NRPS_like) > 1 and ('PF00501' in set(hmm_acc) & NRPS_like):
        return 'NRPS-like'
    else:
        return 'unknow'


def parse_pfam(seq_id, hmm_acc, dict_info):
    """
    添加字典键值对
    """
    hmm_acc = hmm_acc.split(".")[0]
    if dict_info.get(seq_id) != None:
        dict_info[seq_id].append(hmm_acc)
    else:
        dict_info[seq_id] = [hmm_acc]


def read_pfam(file):
    '''
    返回字典{seq_id: hmm_acc}
    '''
    f = open(file, 'r')
    # [f.readline() for x in range(0, 29)]
    dict_info = {}
    for line in f:
        if line[0] == "#" or line.strip() == "":
            continue
        line_strip = re.split(r"\s+", line.strip())
        seq_id = line_strip[0]
        hmm_acc = line_strip[5]
        parse_pfam(seq_id, hmm_acc, dict_info)
    return dict_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=f'{__file__}', description=__doc__, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('i', metavar='<pfam result>', type=str, help='the file of pfam')

    args = parser.parse_args()

    input_file = args.i

    NRPS = {'PF00501', 'PF00550', 'PF00668'}
    PKS = {'PF00109', 'PF02801', 'PF00698'}
    Hybrid = NRPS|PKS
    DMAT = {'PF11991'}
    PKS_like = {'PF00109', 'PF02801'}  # not 'PF00698'}
    Terpene = {'PF01397', 'PF03936'}  # 因为二者选一，所以交集不为空即可
    #  Terpene = {'PF01397', 'PF03936','PF06330','PF05834','PF00494'}  # 根据antismash规则，新添加了三种规则
    NRPS_like = {'PF00501', 'PF00668', 'PF07993', 'PF01370', 'PF00550'}  # 第一个是必须的，后面的是其中之一即可

    dict_info = read_pfam(input_file)
    for k, v in dict_info.items():
        taxo = taxo_pfam(v)
        if taxo != 'unknow':
            print("{}\t{}\t{}".format(k, taxo,",".join(v)))
        else:
            print("{}\t{}".format(k, taxo))
