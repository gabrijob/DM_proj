import sys
from pyspark import SparkContext
import time
from operator import add

#### Driver program

# start spark with 1 worker thread
sc = SparkContext("local[1]")
sc.setLogLevel("ERROR")


# read the input file into an RDD[String]
usageFile = sc.textFile("data/task_usage/part-00001-of-00500.csv")
eventFile = sc.textFile("data/task_events/part-00001-of-00500.csv")

# split each line into an array of items
usageEntries = usageFile.map(lambda x : x.split(','))
eventEntries = eventFile.map(lambda x : x.split(','))

# keep the RDD in memory
usageEntries.cache()
eventEntries.cache()

### Get total approximate cpu and memory usage for each task
task_usages = usageEntries.map(lambda x: ((x[2],x[3]), (float(x[5]),float(x[6])))).reduceByKey(lambda x,y: (x[0] + y[0], x[1] + y[1]))

### Get tasks that failed, were killed or were lost
task_failed = eventEntries.filter(lambda x: x[5] == u'3' or x[5] == u'5' or x[5] == u'6').map(lambda x: ((x[2], x[3]),x[5])).distinct()

### Join the usage values to the tasks that were identified as failed
tasks_failed_usages = task_usages.join(task_failed)

### Get the approximate total amount of loss in each resource for all failed tasks
loss_to_failures = tasks_failed_usages.map(lambda x: (x[1][0][0], x[1][0][1])).reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))

print ("Approximate CPU processing lost due to failures: " + str(loss_to_failures[0]) + " CPU-core-s/s")
print ("Approximate memory pages lost due to failures: " + str(loss_to_failures[1]) + " user accessible pages")
