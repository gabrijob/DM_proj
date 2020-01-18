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
wholeFile = sc.textFile("part-00489-of-00500.csv")
numberOfElements = wholeFile.count()

print('Number of partitions: '+ str(wholeFile.getNumPartitions()))
print('Type of wholefile: '+ str(type(wholeFile)))
print('Total elements '+ str(numberOfElements))


entries = wholeFile.filter(lambda x: x)
entries = entries.map(lambda x : x.split(','))



targetJobId = '6335536474';

targetEntries = entries.filter(lambda x: targetJobId in x)

print('Results: '+str((targetEntries.count())))

schedulingClassTasks = [0,0,0,0]
schedulingClassJobs = [0,0,0,0]

jobsAlready = []
tasksAlready = []

elements = entries.collect()

for elem in elements:
	currentJobId = elem[2]
	currentTaskIndex = elem[3]
	currentSchedulingClass = int(elem[7])
	
	currentTask = currentJobId+currentTaskIndex

	if currentJobId not in jobsAlready:
		schedulingClassJobs[currentSchedulingClass] += 1;
		jobsAlready.append(currentJobId)
	
	if currentTask not in tasksAlready:
		schedulingClassTasks[currentSchedulingClass]+=1;
		tasksAlready.append(currentTask)


print(schedulingClassTasks)
print(schedulingClassJobs)
print('Size of jobs already: '+str(len(jobsAlready)))

proporcao = schedulingClassTasks[0]/schedulingClassJobs[0]
proporcao1 = schedulingClassTasks[1]/schedulingClassJobs[1]
proporcao2 = schedulingClassTasks[2]/schedulingClassJobs[2]
proporcao3 = schedulingClassTasks[3]/schedulingClassJobs[3]

print(proporcao)
print(proporcao1)
print(proporcao2)
print(proporcao3)




results = []
for elem in elements:
	currentJobId = elem[2]		
	if currentJobId == targetJobId:
		results.append(elem)

print('Results: '+str(len(results)))
targetEntries = elements.filter(lambda x: targetJob in x)

#print('Entry '+str(nb)+' : '+str((elements[nb])[0]))


#targetEvents = entries.map(lambda x: x[2]); print(type(targetEvents)); for elem in wholeFile.sortBy(lambda x: x):	print(elem)


