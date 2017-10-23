import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

def graph1(results):
    rate = range(1, 11)
    ylabels = ["Drop Rate", "Average Latency", "Average Throughput"]
    colors = ["red", "blue", "green", "purple"]
    for i in range(3):
        ctr = 0
        for k, v in results.items():
            plt.plot(rate, v[i], color=colors[ctr], label=k)
            ctr += 1
        plt.xlabel("Transmission Rate (Mbps)")
        plt.ylabel(ylabels[i])
        plt.title("{0} over range of Transmission Rates - 1000Bytes".format(ylabels[i]))
        plt.legend(loc="upper right")
        plt.savefig("Figures/Rate_v_{0}".format(ylabels[i]))
        plt.clf()
    

def graph2(results):
    p_size = range(500, 10001, 2500)
    ylabels = ["Drop Rate", "Average Latency", "Average Throughput"]
    colors = ["red", "blue", "green", "purple"]
    for i in range(3):
        ctr = 0
        for k, v in results.items():
            plt.plot(p_size, v[i], color=colors[ctr], label=k)
            ctr += 1
        plt.xlabel("Packet Size (Bytes)")
        plt.ylabel(ylabels[i])
        plt.title("{0} over range of Packet Sizes - 2Mbps".format(ylabels[i]))
        plt.legend(loc="upper right")
        plt.savefig("Figures/PacketSize_v_{0}".format(ylabels[i]))
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
        if output["p_type"] = "tcp":
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
    psum, smallest, biggest = 0, 100, -5
    for k, v in sorted_outputs.items():
        tp = -1 # if packet transmission incomplete
        trans_time = v[-1]["time"] - v[0]["time"]
        total_trans_time += trans_time
        
        for value in v:
            if value["event"] == "d":
                drop_ctr += 1
        if trans_time == 0:
            continue

        psum += v[0]["p_size"]
        if v[0]["time"] < smallest:
            smallest = v[0]["time"]
        if v[-1]["time"] > biggest:
            biggest = v[-1]["time"]
                                                    
        tp = v[0]["p_size"] / trans_time
        num_trans += 1
        throughput_sum += tp
        throughputs[k] = tp
    avg_tp = psum/float((biggest-smallest))/1000000
    #avg_tp = throughput_sum/float(num_trans)/1000000
    avg_lat = total_trans_time/float(num_trans)
    drop_rate = drop_ctr/float(len(throughputs.keys()))
    print "Average Throughput = {0} Mbps".format(avg_tp)
    print "Average Latency = {0} seconds".format(avg_lat)
    print "Total Latency = {0} seconds".format(total_trans_time)
    print "Drop Rate = {0}%".format(drop_rate)

    return drop_rate, avg_lat, avg_tp

def get_filenames():
    filenames = list()
    for variant in ["Tahoe", "Newreno", "Reno", "Vegas"]:
        for p_rate in range(1, 11):
            for p_size in range(500, 10001, 2500):
                filenames.append("{0}_{1}_{2}.tr".format(variant, p_rate, str(p_size)))
    return filenames
                

if __name__ == '__main__':
    size_range = [i for i in range(500, 10001, 2500)]
    rate_range = [i for i in range(1, 11)]
    filenames = get_filenames()

    vary_rate = defaultdict(lambda: defaultdict(list))
    vary_psize = defaultdict(lambda: defaultdict(list))
    
    for fname in filenames:
        print fname
        if fname.startswith("_"):
            fname = fname[1:]
        parts = fname.split("_")
        packet_size = parts[-1].split(".")[0]
        rate = parts[1]
        variant = parts[0]
        print "\nVariant = {0}, Rate = {1}Mbps, Packet Size = {2}".format(parts[0], rate, packet_size)
        drop_rate, avg_lat, avg_tp = parse(fname)

        if int(packet_size) == 3000:
            vary_rate[variant][0].append(drop_rate)
            vary_rate[variant][1].append(avg_lat)
            vary_rate[variant][2].append(avg_tp)
 
        if rate == "2":
            vary_psize[variant][0].append(drop_rate)
            vary_psize[variant][1].append(avg_lat)
            vary_psize[variant][2].append(avg_tp)

    graph1(vary_rate)
    graph2(vary_psize)



    
