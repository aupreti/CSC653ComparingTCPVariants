set variant [lindex $argv 0]
set alg [lindex $argv 1]
set file_name [lindex $argv 2]
set ns [new Simulator]
#Open the trace file (before you start the experiment!)
set tf [open $file_name w]
$ns trace-all $tf

proc finish {} {
    global ns tf
    $ns flush-trace
    #Close the trace file
    close $tf
    exit 0
}

set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

$ns duplex-link $n1 $n2 10Mb 0ms $alg
$ns duplex-link $n2 $n3 10Mb 0ms $alg
$ns duplex-link $n3 $n4 10Mb 0ms $alg
$ns duplex-link $n3 $n6 10Mb 0ms $alg
$ns duplex-link $n5 $n2 10Mb 0ms $alg

if {$variant eq "Tahoe"} {
    set tcp [new Agent/TCP]
} else {
    set tcp [new Agent/TCP/$variant]

}
##$tcp set class_ 2
$ns attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
##$tcp set fid_ 1


set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP
##$ns connect $tcp $sink

set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set null [new Agent/Null]
$ns attach-agent $n6 $null
$ns connect $udp $null
$udp set fid_ 2

set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 4000
$cbr set rate_ 8mb
$cbr set random_ false

$ns at 0.1 "$ftp start"
$ns at 1.0 "$cbr start"
$ns at 7.0 "$cbr stop"
$ns at 7.5 "$ftp stop"
$ns at 8.0 "finish"

puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"
$ns run
# Close the trace file (after you finish the experiment!)
close $tf

