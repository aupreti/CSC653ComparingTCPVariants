#!/usr/bin/env bash

touch "Reno_Reno.tr"
ns ex2.tcl "Reno"  "Reno" "10mb" "10000" "Reno_Reno.tr"

touch "Newreno_Reno.tr"
ns ex2.tcl "Newreno"  "Reno" "10mb" "10000" "Newreno_Reno.tr"

touch "Vegas_Vegas.tr"
ns ex2.tcl "Vegas"  "Vegas" "10mb" "10000" "Vegas_Vegas.tr"

touch "Newreno_Vegas.tr"
ns ex2.tcl "Newreno"  "Vegas" "10mb" "10000" "Newreno_Vegas.tr"

