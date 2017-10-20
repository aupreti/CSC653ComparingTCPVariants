import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import sys
import numpy as np


def graph(drop, lat, tp):
    filenames = ["Vegas/Vegas", "Reno/Reno", "Newreno/Reno", "Newreno/Vegas"]
    ylabels = ["Drop Rate", "Average Latency", "Average Throughput"]
    colors = ["red", "blue", "green", "purple"]
    data = [drop, lat, tp]
    for i, yl, c in zip(data, ylabels, colors):
        y_pos = np.arange(len(filenames))
        plt.bar(y_pos, i, align='center', color=c)
        plt.xticks(y_pos, filenames)
        plt.ylabel(yl)
        plt.title("{0} over range of Packet Sizes - 1Mbps, 1000Byte Packet Size".format(yl))
        plt.savefig("Figures/{0}_v_Variants".format(yl))
        plt.clf()

def parse(filename):
    trace = open(filename, "r").readlines()
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
        output["src_addr"] = parts[-4]
        output["dest_addr"] = parts[-3]
        outputs[p_id].append(output)
    sorted_outputs = defaultdict(list)
    for k,v in outputs.items():
        newlist = sorted(v, key=lambda k: k['time']) 
        sorted_outputs[k] = newlist

    # compute throughput and keep track of drop rate
    drop_ctr = 0
    throughputs = defaultdict(list)
    throughput_sum = 0
    num_trans = 0
    total_trans_time = 0
    for k, v in sorted_outputs.items():
        tp = -1 # if packet transmission incomplete
        trans_time = v[-1]["time"] - v[0]["time"]
        total_trans_time += trans_time
        
        #if not (v[-1]["event"] == "r" and float(v[-1]["to_node"]) == float(v[-1]["dest_addr"])):
        for value in v:
            if value["event"] == "d":
                drop_ctr += 1
        if trans_time == 0:
            continue
        tp = v[0]["p_size"] / trans_time
        num_trans += 1
        throughput_sum += tp
        throughputs[k] = tp

    avg_tp = throughput_sum/float(num_trans)/1000000
    avg_lat = total_trans_time/float(num_trans)
    drop_rate = drop_ctr/float(len(throughputs.keys()))
    print "Average Throughput = {0} Mbps".format(avg_tp)
    print "Average Latency = {0} seconds".format(avg_lat)
    print "Total Latency = {0} seconds".format(total_trans_time)
    print "Drop Rate = {0}%".format(drop_rate)

    return drop_rate, avg_lat, avg_tp
                

if __name__ == '__main__':
    size_range = [i for i in range(500, 10001, 2500)]
    rate_range = [i for i in range(1, 11)]
    filenames = ["Vegas_Vegas.tr", "Reno_Reno.tr", "Newreno_Reno.tr", "Newreno_Vegas.tr"]

    #results = defaultdict(lambda: defaultdict(list))
    dr = []
    al = []
    at = []
    
    for fname in filenames:
        variant = fname.split(".")[0]
        rate = 1
        packet_size = 1000
        print "\nVariant = {0}, Rate = {1}Mbps, Packet Size = {2}".format(variant, rate, packet_size)
        drop_rate, avg_lat, avg_tp = parse(fname)

        #results[variant][0].append(drop_rate)
        #results[variant][1].append(avg_lat)
        #results[variant][2].append(avg_tp)
        dr.append(drop_rate)
        al.append(avg_lat)
        at.append(avg_tp)

    graph(dr, al, at)



    
