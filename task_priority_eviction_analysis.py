import sys
from pyspark import SparkContext
import time

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

files = [wholeFile, wholeFile2]
wholeFile = sc.union(files)

print('Number of partitions: '+ str(wholeFile.getNumPartitions()))
print('Type of wholefile: '+ str(type(wholeFile)))
print('Total elements '+ str(numberOfElements))


entries = wholeFile.filter(lambda x: x)
entries = entries.map(lambda x : x.split(','))

# keep the RDD in memory
entries.cache()

#Do tasks with low priority have a higher probability of being evicted?

all_events = entries.map(lambda x: (x[2], (x[3], x[5], x[8])))
all_events_byPriority = all_events.map(lambda x: (x[1][2], (x[0], x[1][1])))
evictRate_byPriority = all_events_byPriority.map( lambda x: ( x[0] ,(1,0)) if x[1][1] == '2' else (x[0] ,(0,1)))
reduction = evictRate_byPriority.reduceByKey(lambda x, y: (x[0] + y[0], x[1]+y[1])).map(lambda x: (int(x[0]), (100*(x[1][0]/(x[1][0]+x[1][1])), x[1][0]+x[1][1]) ))

jobWithPriorityN = all_events_byPriority.filter(lambda x: x[0] == u'11')



print("Probability of evict event by priority:")
for elem in reduction.sortByKey().collect():
	print('Priority '+str(elem[0])+ ': '+str(elem[1][0])+'% of having a task evicted. Out of '+str(elem[1][1])+' events with this priority level.')

