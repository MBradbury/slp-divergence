#!/usr/bin/gnuplot
set terminal pdf enhanced
set ylabel font "',16'"
set xlabel font "',16'"
set size square

unset key

set palette rgbformula -7,2,-7
set cbrange [0:1]
unset colorbox

set xrange [0.5:10.5]
set yrange [0.5:10.5]

set xtics 1
set ytics 1

set ylabel "N_{/Symbol l}"
set xlabel "S_{/Symbol m}"

set view map

do for [start=1:9] {

	#set title sprintf("JSD when starting at %d", start)

    outfile = sprintf("JSD3D-%d.pdf", start)
    set output outfile

    col=start+2

	plot "JSD3D.dat" using 1:2:col with image, \
	     "JSD3D.dat" using 1:2:(sprintf("%g", column(col))) with labels
}
