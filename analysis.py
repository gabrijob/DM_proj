import sys
from pyspark import SparkContext
import time
from operator import add

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

##### Get the percentage of cpu loss for maintenance

# First get a RDD with the amount of cpu removed during the processing
cpu_removed = entries.filter(lambda x: x[2] != u'2' and x[4] is not u'')\
	.map(lambda x:(x[1],(int(x[2]),float(x[4]),1)) if x[2]==u'1' else (x[1],(int(x[2]),0,1)))\
	.reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1], x[2]+y[2])).filter(lambda x: x[1][0] != 0)

# Then get the total number of maintenances and the amount of cpu lost by them
cpu_loss_maintenance = cpu_removed.filter(lambda x: 2*x[1][0]+1 == x[1][2]).map(lambda x: (x[1][0], x[1][1]))\
	.reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))

# And finally, the percentage of cpu lost
tot_cpu_loss_mtnc = cpu_loss_maintenance[1] / cpu_loss_maintenance[0] * 100

# Display the behavior of 10 machines where (number of removes, cpu lost, tot number of events)
print("Display the behavior of 10 machines where (number of removes, cpu lost, tot number of events):")
for elem in cpu_removed.take(10):
	print(elem)

print("Where the percentage of cpu loss for maintenance is {} ".format(tot_cpu_loss_mtnc))
