import sys
from pyspark import SparkContext
from operator import add
import time
from operator import itemgetter
from functools import partial

# Finds out the index of "name" in the array firstLine 
# returns -1 if it cannot find it
def findCol(firstLine, name):
	if name in firstLine:
		return firstLine.index(name)
	else:
		return -1


#### Driver program

# start spark with 1 worker thread
sc = SparkContext("local[1]")
sc.setLogLevel("ERROR")

# read the input file into an RDD[String]
wholeFile2 = sc.textFile("data/task_events/part-00190-of-00500.csv")
wholeFile = sc.textFile("data/task_events/part-00000-of-00500.csv")

numberOfElements = wholeFile.count()

files = [wholeFile2]
wholeFile = sc.union(files)

print('Number of partitions: '+ str(wholeFile.getNumPartitions()))
print('Type of wholefile: '+ str(type(wholeFile)))
print('Total elements '+ str(numberOfElements))

entries = wholeFile.filter(lambda x: x)
entries = entries.map(lambda x : x.split(','))

# keep the RDD in memory
entries.cache()

# What is the percentage of jobs/tasks that got killed or evicted depending on the scheduling class?

values = entries.map(lambda x: (x[7], (1,1)) if (x[5] == '2' or x[5] == '5') else (x[7], (0,1))).reduceByKey(lambda x, y: (x[0] + y[0], x[1]+y[1]))
percentages = values.map(lambda x: (x[0], (100*(float(x[1][0])/(x[1][0]+x[1][1])))))


print("Probability of task event being EVICT or KILL based on scheduling class:")
for elem in percentages.sortByKey().collect():
	print(elem)

print('Second part')

values = entries.map(lambda x: (x[7], (1, (x[2], x[3])))).distinct().reduceByKey(lambda x, y: (x[0] + y[0], x[1]))
tasksThatWereEvictedOrKilled = entries.filter(lambda x: x[5] == u'2' or x[5] ==u'5').map(lambda x: (x[7], (1, (x[2], x[3])))).distinct().reduceByKey(lambda x, y: (x[0] + y[0], x[1]))

print('Percentage analysis')
for elem in values.sortByKey().collect():
	for elem2 in tasksThatWereEvictedOrKilled.sortByKey().collect():
		if elem[0] == elem2[0]:
			#print(elem)
			#print(elem2)
			percentage = float(elem2[1][0])/elem[1][0]
			percentage = percentage * 100
			print('Scheduling class '+str(elem[0])+' :'+str(percentage)+' percent.')
