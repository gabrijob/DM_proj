import sys
import time
import pandas as pd

fileNames = []
start = time.time()

#We will need a list of all files
for i in range(0,173):
	fileName = 'data/task_events/part-'
	second ='00000'+str(i)
	if len(second) != 5:
		second = second[-5:]
	fileName = fileName+second
	fileName = fileName + '-of-00500.csv'	
	fileNames.append(fileName)

#List of individual data frames
li = []


#Reading data into pandas data farmes and adding them to the list
for filename in fileNames:
    df = pd.read_csv(filename, header=None, usecols=[8,2,5]) 
    df.columns = [ 'JobId', 'EventType', 'Priority']   
    li.append(df)

#Concatenating all data on the files into one single data frame
frame = pd.concat(li, axis=0, ignore_index=True)
df = frame

#Rearranging column order
df = df.reindex(columns=['Priority','JobId','EventType'])

#These functions will help us to use pandas' map function and create the two new columns that interest us, EvictedEvent and AnyEvent
def evictCounter(EventType):
    if EventType == 2:
    	return 1
    else:
    	return 0

def eventCounter(EventType):
    return 1


#We create and add the new columns to the data frame
df['AnyEvent']= df['EventType'].map(eventCounter) # Total Events
df['EvictEvent'] = df['EventType'].map(evictCounter) #Evict Counter

# This data frame will contain only events of the type Eviction
dfEvictionsOnly = df.query('EvictEvent == 1')

#Finally, we obtain a pandas' series where we will have event frequency grouped by priority
nTotalEventsByPriority = df.groupby('Priority')['AnyEvent'].count()
nTotalEvicitonsByPriority = dfEvictionsOnly.groupby('Priority')['AnyEvent'].count()

# We will have a list of tuples where each value will be (Priority, Percentage of Evictions)
averages = []

#We compute the percentages
for index, val in nTotalEvicitonsByPriority.iteritems():
        averages.append((index,100* (val/nTotalEventsByPriority[index])))

print('Final Averages: ')
for element in averages:
	print(element)

#Time elapsed
total = time.time()-start
print('Total time elapsed: '+str(total)+' seconds.')			









