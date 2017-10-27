#!/usr/bin/env bash
touch "Reno_DropTail_100.tr"
ns ex3.tcl "Reno" "DropTail" "Reno_DropTail_100.tr" "100"
touch "Reno_DropTail_300.tr"
ns ex3.tcl "Reno" "DropTail" "Reno_DropTail_300.tr" "300"

touch "Reno_Red_100.tr"
ns ex3.tcl "Reno" "RED" "Reno_Red_100.tr" "100"
touch "Reno_Red_300.tr"
ns ex3.tcl "Reno" "RED" "Reno_Red_300.tr" "300"

touch "Sack_DropTail_100.tr"
ns ex3.tcl "Sack1" "DropTail" "Sack_DropTail_100.tr" "100"
touch "Sack_DropTail_300.tr"
ns ex3.tcl "Sack1" "DropTail" "Sack_DropTail_300.tr" "300"

touch "Sack_Red_100.tr"
ns ex3.tcl "Sack1" "RED" "Sack_Red_100.tr" "100"
touch "Sack_Red_300.tr"
ns ex3.tcl "Sack1" "RED" "Sack_Red_300.tr" "300"
