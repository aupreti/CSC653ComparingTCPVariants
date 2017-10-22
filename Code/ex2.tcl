set variant1 [lindex $argv 0]
set variant2 [lindex $argv 1]
set rate [lindex $argv 2]
set packet_size [lindex $argv 3]
set file_name [lindex $argv 4]
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

$ns duplex-link $n1 $n2 10Mb 0ms DropTail
$ns duplex-link $n2 $n3 10Mb 0ms DropTail
$ns duplex-link $n3 $n4 10Mb 0ms DropTail
$ns duplex-link $n3 $n6 10Mb 0ms DropTail
$ns duplex-link $n5 $n2 10Mb 0ms DropTail


if {$variant1 eq "Tahoe"} {
    set tcp1 [new Agent/TCP]
} else {
    set tcp1 [new Agent/TCP/$variant1]

}

$tcp1 set class_ 1
$ns attach-agent $n1 $tcp1
set sink1 [new Agent/TCPSink]
$ns attach-agent $n4 $sink1
$ns connect $tcp1 $sink1
$tcp1 set fid_ 1

if {$variant2 eq "Tahoe"} {
    set tcp2 [new Agent/TCP]
} else {
    set tcp2 [new Agent/TCP/$variant2]

}

$tcp2 set class_ 2
$ns attach-agent $n5 $tcp2
set sink2 [new Agent/TCPSink]
$ns attach-agent $n6 $sink2
$ns connect $tcp2 $sink2
$tcp2 set fid_ 2

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP

set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP

set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 2

set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ $packet_size
$cbr set rate_ $rate
$cbr set random_ false

$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp1 start"
$ns at 1.0 "$ftp2 start"
$ns at 4. "$ftp2 stop"
$ns at 4. "$ftp1 stop"
$ns at 4.5 "$cbr stop"
$ns at 5.0 "finish"

puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"
$ns run
# Close the trace file (after you finish the experiment!)
close $tf
