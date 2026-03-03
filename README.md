## pfam_scan_parallel
**pfam_scan_parallel** is a practical speedup wrapper for Pfam domain annotation.  
It is **not** a complete rewrite of the official [`pfam_scan.pl`](http://ftp.ebi.ac.uk/pub/databases/Pfam/Tools/), but an optimized version inspired by the parallel strategy used in tools like [`kofam_scan`](https://github.com/takaram/kofam_scan).

**Advantages**:
- Significantly faster wall-clock time (especially on multi-core machines)
- Output is highly compatible with standard `pfam_scan.pl` (minor numerical/ordering differences may occur, but biological interpretation remains consistent)
- On the author's machine with 30 threads, a typical dataset (with 11,312 proteins) finishes in **under 2 minutes** real time
- 
### Requirements ()
- HMMER3 (with `hmmsearch`)
- GNU parallel
- Perl
- Python3

### Build Database:
1、download
If you already have a prepared Pfam database, you can skip the download step.
```bash
pfamversion="Pfam38.2"
database_dir=/path/to/database/pfam/${pfamversion}  # ← Edit this path!!!
mkdir -p ${database_dir}
cd ${database_dir}

# Download files
wget http://ftp.ebi.ac.uk/pub/databases/Pfam/releases/${pfamversion}/Pfam-A.hmm.gz
wget http://ftp.ebi.ac.uk/pub/databases/Pfam/releases/${pfamversion}/Pfam-A.hmm.dat.gz
wget http://ftp.ebi.ac.uk/pub/databases/Pfam/releases/${pfamversion}/active_site.dat.gz

## Uncompress
gunzip2 *.gz
```
2、Build
```bash
## split hmm models
mkdir models
cat Pfam-A.hmm | perl -e '$c=""; while(<>){chomp; $c.="$_\n";if(/^\/\//){open O,">models/$acc.hmm"; print O "$c"; $c=""; close(O)}; $acc=$1 if $_=~/^ACC\s+(.*)/}'
find models -name "*.hmm" -exec realpath {} + > models.list

## interget dat 
pfam_format_dat.py Pfam-A.hmm.dat active_site.dat pfam.dat
```

### Run
修改`flow_pfam.v2.sh`第30-32行之后，就可以运行了。
```bash
flow_pfam.v2.sh input.faa output.pfam
```
