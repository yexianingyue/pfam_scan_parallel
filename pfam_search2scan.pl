#!/usr/bin/env perl
use strict;
use warnings;

if (@ARGV != 2) {
        die "\n\tUsage: $0  pfam.dat  merged.pfam.tmp\n";
        }

my $pfam_dat_file  = $ARGV[0];
my $input_file     = $ARGV[1];

# 第一步：读取 pfam.dat
my %pfam;

open my $fh1, '<', $pfam_dat_file or die "not found file $pfam_dat_file: $!";
while (<$fh1>) {
        chomp;
        my @fields = split /\t/;
        @{ $pfam{ $fields[0] }} = @fields;
        }
close $fh1;

# 第二步：merged.pfam.tmp
open my $fh2, '<', $input_file or die "not found file $input_file: $!";

while (<$fh2>) {
        chomp;
        my @l = split /\s+/;

        my $acc = $l[4];

        my @x = exists $pfam{$acc} ? @{ $pfam{$acc} } : ('') x 10;

        my $flag = ( $l[7] >= $x[3] || $l[14] >= $x[3] ) ? 1 : 0;

        print join("\t",
            $l[0],          # 1
            $l[17],         # 2
            $l[18],         # 3
            $l[19],         # 4
            $l[20],         # 5
            $l[4],          # 6   accession
            $l[3],          # 7
            $x[1] // '',    # 8   pfam domain
            $l[15],         # 9
            $l[16],         # 10
            $l[5],          # 11
            $l[13],         # 12 score
            $l[12],         # 13 evalue
            $flag,          # 14  1 or 0
            $x[5] // '',    # 15
            $x[4] // ''     # 16 activate site
            ) . "\n";
        }

close $fh2;
