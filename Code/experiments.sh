#!/usr/bin/env bash
##1st arg: variant
##2nd arg: rate
##3rd arg: packet size
##3rd arg: tracefile
## declare an array variable
#declare -a variants=("Vegas" "Reno" "NewReno" "Tahoe")
#declare -a rates=($(seq 1 10 ))
#declare -a packet_sizes=($(seq 500 500 10000 ))

declare -a variants=("Vegas" "Reno" "Newreno" "Tahoe")
declare -a rates=($(seq 1 3 ))
declare -a packet_sizes=($(seq 500 500 1000 ))

##declare -a outputfiles=("element1" "element2" "element3")

for i in "${variants[@]}"
do
    for j in "${rates[@]}"
    do
	for k in "${packet_sizes[@]}"
	do
	    ##echo "$i , $j, $k"
	    #create file in the current directory directory
	    touch "${i}_${j}_${k}.tr"
	    ns ex1.tcl "$i"  "$j" "$k" "${i}_${j}_${k}.tr"
	done
    done
done

