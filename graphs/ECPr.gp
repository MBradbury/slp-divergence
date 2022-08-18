#!/usr/bin/gnuplot
set terminal pdf enhanced
set ylabel font "',16'"
set xlabel font "',16'"
set size square

unset key

#set palette negative rgbformula -7,-7,2
set palette defined (0 "turquoise", 1 "white")
set cbrange [0:1]
unset colorbox

set xrange [0.5:9.5]
set yrange [-0.5:14.5]

set xtics 1
set ytics 1

set ylabel "Safety Period"
set xlabel "Starting Node"

set view map

set output "ECPrN.pdf"

plot "ECPrN.dat" using 1:2:3 with image, \
     "ECPrN.dat" using 1:2:(sprintf("%g", column(3))) with labels

set output "ECPrS.pdf"

plot "ECPrS.dat" using 1:2:3 with image, \
     "ECPrS.dat" using 1:2:(sprintf("%g", column(3))) with labels
