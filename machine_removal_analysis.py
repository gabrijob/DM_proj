import sys
from pyspark import SparkContext
import time
from operator import add

#### Driver program

# start spark with 1 worker thread
sc = SparkContext("local[1]")
sc.setLogLevel("ERROR")


# read the input file into an RDD[String]
wholeFile = sc.textFile("data/machine_events/part-00000-of-00001.csv")

# split each line into an array of items
entries = wholeFile.map(lambda x : x.split(','))

# keep the RDD in memory
entries.cache()

##### Get the percentage of cpu loss for maintenance

### First get a RDD with the amount of cpu removed during the processing (id, (event, cpu, 1))
### After reducing get pair (id, (nb of removes, cpu, nb removes + updates))
cpu_rm_ratio = entries.filter(lambda x: x[2] != u'2' and x[4] is not u'')\
	.map(lambda x:(x[1],(1,float(x[4]),0)) if x[2]==u'1' else (x[1],(0,float(x[4]),1)))\
	.reduceByKey(lambda x,y: (x[0]+y[0], x[1], x[2]+y[2]))

# Get the amount of cpu lost for all removals represented in the form (nb of removals, cpu loss)
cpu_loss_all = cpu_rm_ratio.map(lambda x: (x[1][0], x[1][0]*x[1][1])).reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))
# Get the amount of cpu added for all additions represented in the form (nb of additions, cpu added)
cpu_gain_all = cpu_rm_ratio.map(lambda x: (x[1][2], x[1][2]*x[1][1])).reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))

# Then get the total number of maintenances and the amount of cpu lost by them
cpu_loss_maintenance = cpu_rm_ratio.map(lambda x: (x[1][0], x[1][0]*x[1][1]) if x[1][0]+1 == x[1][2] else (x[1][0] -1, (x[1][0] -1)*x[1][1]))\
    .filter(lambda x: x[0] > 0).reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))

# From that we can get the percentages
tot_cpu_loss_all = cpu_loss_all[1] / cpu_gain_all[1] * 100
print("The percentage of cpu loss for all removals is {} ".format(tot_cpu_loss_all))

tot_cpu_loss_mtnc = cpu_loss_maintenance[1] / cpu_gain_all[1] * 100
print("The percentage of cpu loss for maintenance is {} ".format(tot_cpu_loss_mtnc))

tot_cpu_loss_fail = tot_cpu_loss_all - tot_cpu_loss_mtnc
print("The percentage of cpu loss for failures is {} ".format(tot_cpu_loss_fail))

##### Get the percentage of memory loss for maintenance
mem_rm_ratio = entries.filter(lambda x: x[2] != u'2' and x[5] is not u'')\
	.map(lambda x:(x[1],(1,float(x[5]),0)) if x[2]==u'1' else (x[1],(0,float(x[5]),1)))\
	.reduceByKey(lambda x,y: (x[0]+y[0], x[1], x[2]+y[2]))

# Get the amount of cpu added for all additions represented in the form (nb of additions, mem added)
mem_gain_all = mem_rm_ratio.map(lambda x: (x[1][2], x[1][2]*x[1][1])).reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))

# Then get the total number of maintenances and the amount of mem lost by them
mem_loss_maintenance = mem_rm_ratio.map(lambda x: (x[1][0], x[1][0]*x[1][1]) if x[1][0]+1 == x[1][2] else (x[1][0] - 1, (x[1][0] - 1)*x[1][1]))\
    .filter(lambda x: x[0] > 0).reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))

tot_mem_loss_mtnc = mem_loss_maintenance[1] / mem_gain_all[1] * 100
print("The percentage of memory loss for maintenance is {} ".format(tot_mem_loss_mtnc))