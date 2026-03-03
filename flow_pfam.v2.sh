#!/usr/bin/bash
# set -euo pipefail

( [ $# -ne 2 ] ) && echo "$0 <fasta> <output_file>" && exit 127

inf=`realpath -s $1`
outf=`realpath -s $2`


if [ -f "${outf}.lock" ];then
    echo "${outf} is running."
    exit 127
fi



if [ -f "${outf}.ok" ];then
    echo -e "\033[32msuccess:\033[0m\t$outf."
    exit 0
fi

shopt -s expand_aliases

#-----------------------
#        software
[ -f "/usr/local/bin/pigz" ] && alias gzip="/usr/local/bin/pigz" ||  alias gzip="/usr/bin/gzip"

#-----------------------
#        database
db_list=/share/data1/Database/Pfam/test/pfam.list
db_dat=/share/data1/Database/Pfam/releases35/pfam.dat
threads=30



touch ${outf}.lock

if [ ! -f ${outf}.temp.faa.ok ];then
    if ( [[ $inf =~ .gz$ ]] )
    then
        gzip -dc  $inf > ${outf}.temp.faa || ! rm ${outf}.temp.faa || exit 127
    elif ( [[ $inf =~ .bz2$ ]] )
    then
        bunzip2 -dc $inf > ${outf}.temp.faa || ! rm ${outf}.temp.faa || exit 127
    else
        ln -s $inf  ${outf}.temp.faa
    fi
    [ $? -ne 0 ] && exit 127
    touch ${outf}.temp.faa.ok
fi



if [ ! -f ${outf}.pfam.tmp.ok ];then
    if [ ! -d ${outf}.pfam.tmp ];then
        mkdir ${outf}.pfam.tmp
    fi
    echo "run hmmsearch"
    cat ${db_list} |\
        parallel -j ${threads} --joblog ${outf}.pfam.tmp.log --retry-failed --plus \
        hmmsearch --cpu 5 --notextw --cut_ga --noali --domtblout \
        ${outf}.pfam.tmp/{/.}.out {} ${outf}.temp.faa \> /dev/null;
    stat=`echo $?`
    [ $stat -ne 0 ] && echo $stat && exit 127
    echo "merge hmmsearch output"
    find "${outf}.pfam.tmp" -type f -name "*.out" -print0 | xargs -0 cat |  grep -v "^#" > ${outf}.pfam.merge\
        && touch ${outf}.pfam.tmp.ok
fi


if [ -f ${outf}.pfam.tmp.ok ];then
    pfam_search2scan.pl ${db_dat} ${outf}.pfam.merge \
        | sort -k 1,1 -k 12,12gr -k 11,11nr \
        | pfam_format_res.py > ${outf}

    rm ${outf}.lock && touch ${outf}.ok \
        && chmod 444 ${outf} \
        && rm -rf ${outf}.pfam.tmp ${outf}.pfam.tmp.ok ${outf}.pfam.tmp.log \
            ${outf}.pfam.merge \
            ${outf}.temp.faa ${outf}.temp.faa.ok
fi
