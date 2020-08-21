#!/usr/bin/gnuplot
set terminal pdf enhanced
set ylabel font "',16'"
set xlabel font "',16'"
set pointsize 1
set nokey
set xrange [1:10]
set xtics font ',16'
set yrange [0:3]
set ytics auto
set ytics font ',16'

#set arrow from 1,6.339850002884625 to 15,6.339850002884625 nohead lc rgb 'blue' lw 3
#set label "Maximum Entropy = 6.34" at 1.1,6.6

set ylabel "H(N_{/Symbol l})"
set xlabel "{/Symbol l}"
set output "HN.pdf"
plot "HN.dat" using 1:2 with lp title "1" linewidth 3, \
     "HN.dat" using 1:3 with lp title "2" linewidth 3, \
     "HN.dat" using 1:4 with lp title "3" linewidth 3, \
     "HN.dat" using 1:5 with lp title "4" linewidth 3, \
     "HN.dat" using 1:6 with lp title "5" linewidth 3, \
     "HN.dat" using 1:7 with lp title "6" linewidth 3, \
     "HN.dat" using 1:8 with lp title "7" linewidth 3, \
     "HN.dat" using 1:9 with lp title "8" linewidth 3, \
     "HN.dat" using 1:10 with lp title "9" linewidth 3

set ylabel "H(S_{/Symbol m})"
set xlabel "{/Symbol m}"
set output "HS.pdf"
plot "HS.dat" using 1:2 with lp title "1" linewidth 3, \
     "HS.dat" using 1:3 with lp title "2" linewidth 3, \
     "HS.dat" using 1:4 with lp title "3" linewidth 3, \
     "HS.dat" using 1:5 with lp title "4" linewidth 3, \
     "HS.dat" using 1:6 with lp title "5" linewidth 3, \
     "HS.dat" using 1:7 with lp title "6" linewidth 3, \
     "HS.dat" using 1:8 with lp title "7" linewidth 3, \
     "HS.dat" using 1:9 with lp title "8" linewidth 3, \
     "HS.dat" using 1:10 with lp title "9" linewidth 3

set yrange [0:1]
set ylabel "JSD(N_{/Symbol l} || S_{/Symbol l})"
set xlabel "{/Symbol l}"
set output "JSD.pdf"
plot "JSD.dat" using 1:2 with lp title "1" linewidth 3, \
     "JSD.dat" using 1:3 with lp title "2" linewidth 3, \
     "JSD.dat" using 1:4 with lp title "3" linewidth 3, \
     "JSD.dat" using 1:5 with lp title "4" linewidth 3, \
     "JSD.dat" using 1:6 with lp title "5" linewidth 3, \
     "JSD.dat" using 1:7 with lp title "6" linewidth 3, \
     "JSD.dat" using 1:8 with lp title "7" linewidth 3, \
     "JSD.dat" using 1:9 with lp title "8" linewidth 3, \
     "JSD.dat" using 1:10 with lp title "9" linewidth 3
