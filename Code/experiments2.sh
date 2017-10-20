#!/usr/bin/env bash

touch "Reno_Reno.tr"
ns ex2.tcl "Reno"  "Reno" "1mb" "1000" "Reno_Reno.tr"

touch "Newreno_Reno.tr"
ns ex2.tcl "Newreno"  "Reno" "1mb" "1000" "Newreno_Reno.tr"

touch "Vegas_Vegas.tr"
ns ex2.tcl "Vegas"  "Vegas" "1mb" "1000" "Vegas_Vegas.tr"

touch "Newreno_Vegas.tr"
ns ex2.tcl "Newreno"  "Vegas" "1mb" "1000" "Newreno_Vegas.tr"

