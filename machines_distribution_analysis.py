from pyspark import SparkContext
from operator import add
import matplotlib.pyplot as plt
import numpy as np

#### Driver program

# start spark with 1 worker thread
sc = SparkContext("local[1]")
sc.setLogLevel("ERROR")


# read the input file into an RDD[String]
wholeFile = sc.textFile("./data/machine_events/part-00000-of-00001.csv")

# split each line into an array of items
entries = wholeFile.map(lambda x : x.split(','))

# keep the RDD in memory
entries.cache()

### Get pairs (machine id, cpu, memory)
machines = entries.map(lambda x: (x[1],(x[4],x[5]))).distinct().filter(lambda x: x[1][0] != u'' and x[1][0] != u'')

"""for elem in machines.collect():
    print elem"""

machine_nb = machines.count()
#print machine_nb

# Get distribution for cpu
dist_cpu = machines.map(lambda x: (float(x[1][0]),1)).reduceByKey(add).map(lambda x: (x[0], float(x[1])*100/machine_nb))


print("\nDistribution of machines according to cpu capacity:\n")
for elem in dist_cpu.collect():
    print("CPU capacity: " + str(elem[0]) + "; Distribution: " + str(elem[1]) + "%")


cpu_labels = []
cpu_prob_h = []
for elem in dist_cpu.collect():
    cpu_labels.append(str(elem[0]))
    cpu_prob_h.append(elem[1])

y_pos = np.arange(len(cpu_labels))

plt.bar(y_pos, cpu_prob_h)
plt.xticks(y_pos, cpu_labels)
plt.show()

# Get distribution for memory
dist_mem = machines.map(lambda x: (float(x[1][1]),1)).reduceByKey(add).map(lambda x: (x[0], float(x[1])*100/machine_nb))

print("\nDistribution of machines according to memory capacity:\n")
for elem in dist_mem.collect():
    print("Memory capacity: " + str(elem[0]) + "; Distibution: " + str(elem[1]) + "%")

mem_labels = []
mem_prob_h = []
for elem in dist_mem.collect():
    mem_labels.append(str(elem[0]))
    mem_prob_h.append(elem[1])

y_pos = np.arange(len(mem_labels))

plt.bar(y_pos, mem_prob_h)
plt.xticks(y_pos, mem_labels)
plt.show()