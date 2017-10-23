#!/usr/bin/env bash

touch "Reno_DropTail.tr"
ns ex3.tcl "Reno" "DropTail" "Reno_DropTail.tr"

touch "Reno_Red.tr"
ns ex3.tcl "Reno" "RED" "Reno_Red.tr"

touch "Sack_DropTail.tr"
ns ex3.tcl "Sack1" "DropTail" "Sack_DropTail.tr"

touch "Sack_Red.tr"
ns ex3.tcl "Sack1" "RED" "Sack_Red.tr"

