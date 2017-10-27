import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import sys
import pdb
import numpy as np


def graph(d):
    filenames = ["Vegas/Vegas", "Reno/Reno", "Newreno/Reno", "Newreno/Vegas"]
    tp_14s = list()
    tp_56s = list()
    drop_14s = list()
    drop_56s = list()
    for i in filenames:
        data = d[i]
        tp_14s.append(data[0])
        tp_56s.append(data[1])
        drop_14s.append(data[2])
        drop_56s.append(data[3])

    ind = list(range(4))
    w = [.35]*4
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    plt.bar(ind, tp_14s, .35, align='center', color="red")
    plt.bar([i + .35 for i in ind], tp_56s,.35,  align='center', color="blue")
    plt.xticks([i + .20 for i in ind], [i.replace("/", " ") for i in filenames])
    plt.xlabel("Combination of TCP Variants")
    plt.ylabel("Throughput (Mbps)")
    plt.title("Throughput vs Combination of TCP Variants")
    plt.savefig("Figures/fairness_throughput")
    plt.clf()

    plt.bar(ind, drop_14s, .35, align='center', color="red")
    plt.bar([i + .35 for i in ind], drop_56s,.35,  align='center', color="blue")
    plt.xticks([i + .20 for i in ind], [i.replace("/", " ") for i in filenames])
    plt.xlabel("Combination of TCP Variants")
    plt.ylabel("Number of Dropped Segments")
    plt.title("Number of Segment Drops vs Combination of TCP Variants")
    plt.savefig("Figures/fairness_drop")
    plt.clf()

def graphb(drop, lat, tp):
    filenames = ["Vegas/Vegas", "Reno/Reno", "Newreno/Reno", "Newreno/Vegas"]
    ylabels = ["# Dropped Packets", "Average Latency", "Average Throughput"]
    colors = ["red", "blue", "green", "purple"]
    data = [drop, lat, tp]
    for i, yl, c in zip(data, ylabels, colors):
        y_pos = np.arange(len(filenames))
        plt.bar(y_pos, i, align='center', color=c)
        plt.xticks(y_pos, filenames)
        plt.ylabel(yl)
        plt.title("{0} over Range of Packet Sizes".format(yl))
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
        output["fid"] = int(parts[-5])
        output["src_addr"] = float(parts[-4])
        output["dest_addr"] = float(parts[-3])
        if output["p_type"] == "tcp":
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
    tp_1_4 = list()
    tp_5_6 = list()
    lat_14 = list()
    lat_56 = list()
    psum_14, psum_56 = 0, 0
    smallest14, smallest56 = 100, 100
    biggest14, biggest56 = -5, -5
    drop_14, drop_56 = 0, 0
    for k, v in sorted_outputs.items():
        trans_time = v[-1]["time"] - v[0]["time"]
        total_trans_time += trans_time

        next_iter = 0

        for value in v:
            if value["event"] == "d":
                drop_ctr += 1
                if value["fid"] == 5:
                    drop_14 += 1
                if value["fid"] == 10:
                    drop_56 += 1
                next_iter = 1
                break

            
        if next_iter == 1:
            continue        
            
        if v[0]["fid"] == 5:
            lat_14.append(trans_time)
            psum_14 += v[0]["p_size"]
            if v[0]["time"] < smallest14:
                smallest14 = v[0]["time"]
            if v[-1]["time"] > biggest14:
                biggest14 = v[-1]["time"]
            tp_1_4.append(v[0]["p_size"] /  (v[-1]["time"] - v[0]["time"]))
        if v[0]["fid"] == 10:
            lat_56.append(trans_time)
            psum_56 += v[0]["p_size"]
            if v[0]["time"] < smallest56:
                smallest56 = v[0]["time"]
            if v[-1]["time"] > biggest56:
                biggest56 = v[-1]["time"]
            tp_5_6.append(v[0]["p_size"] /  (v[-1]["time"] - v[0]["time"]))

        tp = v[0]["p_size"] / trans_time
        num_trans += 1
        throughput_sum += tp
        throughputs[k] = tp

    tp_14 = psum_14/(biggest14-smallest14)/1000000
    tp_56 = psum_56/(biggest56-smallest56)/1000000
    print "Avg Throughput 1-4: ", psum_14/(biggest14-smallest14)/1000000
    print "Avg Throughput 5-6: ", psum_56/(biggest56-smallest56)/1000000
    print "Avg Latency 1-4: ", sum(lat_14)/float(len(lat_14))
    print "Avg Latency 5-6: ", sum(lat_56)/float(len(lat_56))
    #avg_lat = total_trans_time/float(num_trans)
    #drop_rate = drop_ctr
    #tp_14 = sum(tp_1_4) / float(len(tp_1_4)) / 1000000
    #tp_56 = sum(tp_5_6) / float(len(tp_5_6)) / 1000000
    #print "Average Latency = {0} seconds".format(avg_lat)
    #print "Total Latency = {0} seconds".format(total_trans_time)
    print "#Drops 1-4: ", drop_14
    print "#Drops 5-6: ", drop_56
    #print "Drop Rate = {0}%".format(drop_rate)

    return tp_14, drop_14, tp_56, drop_56
                

if __name__ == '__main__':
    size_range = [i for i in range(500, 10001, 2500)]
    rate_range = [i for i in range(1, 11)]
    filenames = ["Vegas_Vegas.tr", "Reno_Reno.tr", "Newreno_Reno.tr", "Newreno_Vegas.tr"]
    d = dict()
    for fname in filenames:
        variant = fname.split(".")[0]
        rate = 10
        packet_size = 1000
        print "\nVariant = {0}, Rate = {1}Mbps, Packet Size = {2}".format(variant, rate, packet_size)
        tp_14, drop_14, tp_56, drop_56 = parse(fname)

        d[variant.replace("_", "/")] = [tp_14, tp_56, drop_14, drop_56] 

    graph(d)



    
