#!/usr/bin/gnuplot
set terminal pdf enhanced font ",17" size 17,0.6
set key horizontal
set key width 2
set xrange [0 : -1]
set yrange [0 : -1]
unset border
unset tics
set output "legend.pdf"
plot NaN with lp title "1 (Source)" linewidth 3, \
     NaN with lp title "2" linewidth 3, \
     NaN with lp title "3" linewidth 3, \
     NaN with lp title "4" linewidth 3, \
     NaN with lp title "5 (Sink)" linewidth 3, \
     NaN with lp title "6" linewidth 3, \
     NaN with lp title "7" linewidth 3, \
     NaN with lp title "8" linewidth 3, \
     NaN with lp title "9" linewidth 3
