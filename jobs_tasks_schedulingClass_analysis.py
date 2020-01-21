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


files =  []



start = time.time()
for i in range(0,100):
	fileName = 'data/task_events/part-'
	second ='00000'+str(i)
	if len(second) != 5:
		second = second[-5:]
	fileName = fileName+second
	fileName = fileName + '-of-00500.csv'
	currentFile = sc.textFile(fileName)
	files.append(currentFile)

wholeFile = sc.union(files)
numberOfElements = wholeFile.count()

print('Number of partitions: '+ str(wholeFile.getNumPartitions()))
print('Type of wholefile: '+ str(type(wholeFile)))
print('Total elements '+ str(numberOfElements))

entries = wholeFile.filter(lambda x: x)
entries = entries.map(lambda x : x.split(','))

# keep the RDD in memory
entries.cache()

# What is the distribution of the number jobs/tasks per scheduling class?

#	.reduceByKey(lambda x,y: max((x, y), key=lambda x: x[1]))

#For the tasks
print('For the tasks:')
allEvents = entries.map(lambda x: (int(x[7]), x[2] )).distinct().map(lambda x: (x[0], 1))

#for element in allEvents.take(5):
#	print(element[0])
#	print(type(element[0]))

reshape = allEvents.reduceByKey(add)
total = 0
for element in reshape.collect():
	total = total + element[1]	

for element in reshape.sortByKey().collect():
	print ('Scheduling class '+str(element[0])+' : '+str(100*(float(element[1])/total))+' percent.')

print('total is '+str(total))

total = time.time()-start
print('Total time elapsed: '+str(total)+' seconds.')			









# For the jobs

files = []

start = time.time()
for i in range(0,100):
	fileName = 'data/job_events/part-'
	second ='00000'+str(i)
	if len(second) != 5:
		second = second[-5:]
	fileName = fileName+second
	fileName = fileName + '-of-00500.csv'
	currentFile = sc.textFile(fileName)
	files.append(currentFile)

wholeFile = sc.union(files)
numberOfElements = wholeFile.count()

print('Number of partitions: '+ str(wholeFile.getNumPartitions()))
print('Type of wholefile: '+ str(type(wholeFile)))
print('Total elements '+ str(numberOfElements))

entries2 = wholeFile.filter(lambda x: x)
entries2 = entries2.map(lambda x : x.split(','))

# keep the RDD in memory
entries2.cache()


#For the jobs
print('For job:')
allEvents = entries2.map(lambda x: (x[5], x[2] )).distinct().map(lambda x: (x[0], 1))

#for element in allEvents.take(5):
#	print(element)
#	print(type(element))

reshape = allEvents.reduceByKey(add)
total = 0

for element in reshape.collect():
	total = total + element[1]


for element in reshape.sortByKey().collect():
#	print element
	print ('Scheduling class '+str(element[0])+' : '+str(100*(float(element[1])/total))+' percent.')


print('total is '+str(total))
	
total = time.time()-start
print('Total time elapsed: '+str(total)+' seconds.')			


#reshape = oneEntryPerTask.map (lambda x: ((x[0][0]), (x[1])))
#reshape = reshape.reduceByKey (lambda x,y : )






