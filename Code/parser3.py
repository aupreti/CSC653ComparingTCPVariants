import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import sys
import numpy as np
import pdb 

def graph(average_througput_tcp_ar, average_througput_cbr_ar, latency_over_time_tcp_ar, latency_over_time_cbr_ar,drop_ctr_tcp_ar, drop_ctr_cbr_ar,tp_over_time_tcp_ar,tp_over_time_cbr_ar):
    TCP_variants = ["Reno", "Sack"]
    queue_types= ["DropTail", "Red"]
    buffer_size=["100","300"]
    colors = ["red", "blue", "green", "purple"]
    buf_indices=[0,1]
    for buf_index in buf_indices:
        for i in range(len(TCP_variants)):
            ctr=0
            for queue in queue_types:
                #pdb.set_trace()
                time_values_tcp= [time_throughput[0] for time_throughput in tp_over_time_tcp_ar[TCP_variants[i]][queue][buf_index][0]]
                tp_values_tcp= [time_throughput[1]/1000000 for time_throughput in tp_over_time_tcp_ar[TCP_variants[i]][queue][buf_index][0]]
                time_values_cbr= [time_throughput[0] for time_throughput in tp_over_time_cbr_ar[TCP_variants[i]][queue][buf_index][0]]
                tp_values_cbr= [time_throughput[1]/1000000 for time_throughput in tp_over_time_cbr_ar[TCP_variants[i]][queue][buf_index][0]]
            
                plt.plot(time_values_tcp, tp_values_tcp, color=colors[ctr], label=TCP_variants[i]+"_"+queue )
                plt.plot(time_values_cbr, tp_values_cbr, color=colors[ctr+1], label="CBR"+ "_"+ queue)
                ctr+=2
            plt.xlabel("Time (s)")
            plt.ylabel("Throughput over time (Mbps)")
            plt.legend(loc="upper right")
            plt.savefig("Figures/Queuing_{0}_{1}".format(TCP_variants[i],buffer_size[buf_index]))
            plt.clf()

def graph2(average_througput_tcp_ar, average_througput_cbr_ar, latency_over_time_tcp_ar, latency_over_time_cbr_ar,drop_ctr_tcp_ar, drop_ctr_cbr_ar,tp_over_time_tcp_ar,tp_over_time_cbr_ar):
    TCP_variants = ["Reno", "Sack"]
    queue_types= ["DropTail", "Red"]
    buffer_size=["100","300"]
    colors = ["red", "blue", "green", "purple"]
    buf_indices=[0,1]
    for buf_index in buf_indices:
        for i in range(len(TCP_variants)):
            ctr=0
            for queue in queue_types:
                #pdb.set_trace()
                time_values_tcp= [time_lat[0] for time_lat in latency_over_time_tcp_ar[TCP_variants[i]][queue][buf_index][0]]
                lat_values_tcp= [time_lat[1] for time_lat in latency_over_time_tcp_ar[TCP_variants[i]][queue][buf_index][0]]
                time_values_cbr= [time_lat[0] for time_lat in latency_over_time_cbr_ar[TCP_variants[i]][queue][buf_index][0]]
                lat_values_cbr= [time_lat[1] for time_lat in latency_over_time_cbr_ar[TCP_variants[i]][queue][buf_index][0]]
                plt.plot(time_values_tcp, lat_values_tcp, color=colors[ctr], label=TCP_variants[i]+"_"+queue )
                plt.plot(time_values_cbr, lat_values_cbr, color=colors[ctr+1], label="CBR"+ "_"+ queue)
                ctr+=2
            plt.xlabel("Time (s)")
            plt.ylabel("Latency over time (s)")
            plt.legend(loc="upper right")
            plt.savefig("Figures/Queuing_Latency_{0}_{1}".format(TCP_variants[i],buffer_size[buf_index]))
            plt.clf()



def parse(filename, start_tcp,start_cbr):
    trace = open(filename, "r").readlines()
    #store each trace in a dictionary that can be indexed by the packet id 
    outputs = defaultdict(list)
    for each in trace:
        parts = each.split(" ")
        output = dict()
        output["event"] = parts[0]
        output["time"] = float(parts[1])
        output["from_node"] = parts[2]
        output["to_node"] = parts[3]
        output["p_type"] = parts[4]
        output["p_size"] = int(parts[5])
        p_id = int(parts[-1])
        output["fid"] = int(parts[-5])
        output["src_addr"] = float(parts[-4])
        output["dest_addr"] = float(parts[-3])
        outputs[p_id].append(output)

    #sort the outputs
    sorted_outputs = defaultdict(list)
    for k,v in outputs.items():
        newlist = sorted(v, key=lambda k: k['time']) 
        sorted_outputs[k] = newlist

    # compute throughput and keep track of drop rate
    drop_ctr_tcp = 0
    drop_ctr_cbr = 0
    
    num_tcp_packets=0
    num_cbr_packets=0
    
    latency_over_time_tcp=[]
    latency_over_time_cbr=[]

    tp_over_time_tcp=[]
    tp_over_time_cbr=[]

    sum_packet_size_tcp,sum_packet_size_cbr, smallest_tcp, smallest_cbr, biggest_tcp, biggest_cbr= 0,0, 100, 100, -5, -5

    for k, v in sorted_outputs.items():
        is_tcp_packet= (v[0]["p_type"]=='tcp')
        is_cbr_packet= (v[0]["p_type"]=='cbr')
                        
        if (is_tcp_packet):
            num_tcp_packets+=1
        
        if (is_cbr_packet):
            num_cbr_packets+=1
        
        tp = -1 # if packet transmission incomplete
        trans_time = v[-1]["time"] - v[0]["time"]

        #handle packet drop
        drop_found = 0
        for value in v:
            if value["event"] == "d":
                if is_tcp_packet:
                    drop_ctr_tcp += 1
                elif is_cbr_packet:
                    drop_ctr_cbr+=1

                drop_found = 1
                break
            
        if drop_found == 1:
            continue

        #record data for both cbr and tcp
        if is_tcp_packet:
            
            latency_over_time_tcp.append([v[-1]["time"],trans_time])
            sum_packet_size_tcp+=v[0]["p_size"]
            tp_over_time_tcp.append([v[-1]["time"],sum_packet_size_tcp/(v[-1]["time"]-start_tcp)])
            if v[0]["time"] < smallest_tcp:
                smallest_tcp = v[0]["time"]
            if v[-1]["time"] > biggest_tcp:
                biggest_tcp =  v[-1]["time"]

        elif is_cbr_packet:
        
            latency_over_time_cbr.append([v[-1]["time"],trans_time])
            sum_packet_size_cbr+=v[0]["p_size"]
            tp_over_time_cbr.append([v[-1]["time"],sum_packet_size_cbr/(v[-1]["time"]-start_cbr)])
            if v[0]["time"] < smallest_cbr:
                smallest_cbr = v[0]["time"]
            if v[-1]["time"] > biggest_cbr:
                biggest_cbr =  v[-1]["time"]
        
            

    average_througput_tcp = sum_packet_size_tcp/float(biggest_tcp-smallest_tcp)/1000000#throughput_sum/float(num_trans)/1000000
    average_througput_cbr = sum_packet_size_cbr/float(biggest_cbr-smallest_cbr)/1000000
    average_latency_tcp=sum(latency for time, latency in  latency_over_time_tcp)/len(latency_over_time_tcp)
    average_latency_cbr=sum(latency for time, latency in  latency_over_time_cbr)/len(latency_over_time_cbr)
    
    print "Average Throughput TCP= {0} Mbps".format(average_througput_tcp)
    print "Average Throughput CBR= {0} Mbps".format(average_througput_cbr)
    print "Average Latency TCP= {0} seconds".format(average_latency_tcp)
    print "Average Latency CBR= {0} seconds".format(average_latency_cbr)
    print "Latency over time TCP =%s" %(latency_over_time_tcp[:20])
    print "Latency over time CBR = %s" %(latency_over_time_cbr[:20])
    print "Drop TCP= {0}".format(drop_ctr_tcp)
    print "Drop CBR= {0}".format(drop_ctr_cbr)
    print "Drop Rate TCP= {0}".format(drop_ctr_tcp/float(num_tcp_packets))
    print "Drop Rate CBR= {0}".format(drop_ctr_cbr/float(num_cbr_packets))
    print "Throughput over time TCP= %s"%(tp_over_time_tcp[:20])
    print "Throughput over time CBR = %s"%(tp_over_time_cbr[:20])
    return average_througput_tcp, average_througput_cbr, latency_over_time_tcp, latency_over_time_cbr,drop_ctr_tcp, drop_ctr_cbr,tp_over_time_tcp,tp_over_time_cbr
                

if __name__ == '__main__':
    start_tcp = 0.1
    start_cbr = 4.0
    size_range = [i for i in range(500, 10001, 2500)]
    rate_range = [i for i in range(1, 11)]
    filenames = ["Reno_DropTail_100.tr","Reno_DropTail_300.tr", "Reno_Red_100.tr","Reno_Red_300.tr", "Sack_DropTail_100.tr","Sack_DropTail_300.tr", "Sack_Red_100.tr","Sack_Red_300.tr"]
    average_througput_tcp_ar = {"Reno":{"DropTail":[[],[]], "Red":[[],[]]},"Sack":{"DropTail":[[],[]], "Red":[[],[]]}}
    average_througput_cbr_ar = {"Reno":{"DropTail":[[],[]], "Red":[[],[]]},"Sack":{"DropTail":[[],[]], "Red":[[],[]]}}
    latency_over_time_tcp_ar ={"Reno":{"DropTail":[[],[]], "Red":[[],[]]},"Sack":{"DropTail":[[],[]], "Red":[[],[]]}}
    latency_over_time_cbr_ar= {"Reno":{"DropTail":[[],[]], "Red":[[],[]]},"Sack":{"DropTail":[[],[]], "Red":[[],[]]}}
    drop_ctr_tcp_ar= {"Reno":{"DropTail":[[],[]], "Red":[[],[]]},"Sack":{"DropTail":[[],[]], "Red":[[],[]]}}
    drop_ctr_cbr_ar={"Reno":{"DropTail":[[],[]], "Red":[[],[]]},"Sack":{"DropTail":[[],[]], "Red":[[],[]]}}
    tp_over_time_tcp_ar={"Reno":{"DropTail":[[],[]], "Red":[[],[]]},"Sack":{"DropTail":[[],[]], "Red":[[],[]]}}
    tp_over_time_cbr_ar={"Reno":{"DropTail":[[],[]], "Red":[[],[]]},"Sack":{"DropTail":[[],[]], "Red":[[],[]]}}
    
    for fname in filenames:
        file_name_parts= fname.split("_")
        variant = file_name_parts[0]
        rate = 2
        packet_size = 1000
        buf_size= (file_name_parts[-1]).split(".")[0]
        queue_type= file_name_parts[1]
        #buffersize
        if buf_size =="100":
            buf_index= 0
        elif buf_size == "300":
            buf_index = 1
            
        print "\nVariant = {0}, Queue = {3}, Rate = {1}Mbps, Packet Size = {2}, Buffer Size = {3}".format(variant, rate, packet_size, buf_size, file_name_parts[1])
        average_througput_tcp, average_througput_cbr, latency_over_time_tcp, latency_over_time_cbr,drop_ctr_tcp, drop_ctr_cbr,tp_over_time_tcp,tp_over_time_cbr =parse(fname,start_tcp,start_cbr)

        average_througput_tcp_ar[variant][queue_type][buf_index].append(average_througput_tcp)
        average_througput_cbr_ar[variant][queue_type][buf_index].append(average_througput_cbr)
        latency_over_time_tcp_ar[variant][queue_type][buf_index].append(latency_over_time_tcp)
        latency_over_time_cbr_ar[variant][queue_type][buf_index].append(latency_over_time_cbr)
        drop_ctr_tcp_ar[variant][queue_type][buf_index].append(drop_ctr_tcp)
        drop_ctr_cbr_ar[variant][queue_type][buf_index].append(drop_ctr_cbr)
        tp_over_time_tcp_ar[variant][queue_type][buf_index].append(tp_over_time_tcp)
        tp_over_time_cbr_ar[variant][queue_type][buf_index].append(tp_over_time_cbr)

#    graph(average_througput_tcp_ar, average_througput_cbr_ar, latency_over_time_tcp_ar, latency_over_time_cbr_ar,drop_ctr_tcp_ar, drop_ctr_cbr_ar,tp_over_time_tcp_ar,tp_over_time_cbr_ar)
    graph2(average_througput_tcp_ar, average_througput_cbr_ar, latency_over_time_tcp_ar, latency_over_time_cbr_ar,drop_ctr_tcp_ar, drop_ctr_cbr_ar,tp_over_time_tcp_ar,tp_over_time_cbr_ar)

    
