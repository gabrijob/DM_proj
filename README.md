

# Data Management Project - MOSIG M2 - 2019/20

In this project we will carry on several analysises on the data set available online representing 29 days worth of information on one of  _Google_'s large scale clusters, compromising about 12.5k machines. There are hundreds of files available detailing the behavior of said machines, as well as the jobs and tasks they are carrying out over this time period. To facilitate the final calculations, we have decided to not use **all** the files, instead focusing on at most **100** files for each category. That is, when that many are available. 

The data were downloaded using a custom made script, **downloads.sh**, which was written to automatically push files from google's cloud storage (using the _GSUtil_ tool) and unzip them immediately after in the desired path destination.

The structure of the submission is simple. In addition to this report there will be one _python_ (.py) file for each of the analysis or questions answered. As well as the aforementioned custom made script and images containing the graphics shown in the report. 

Each analysis will be made using _spark_ transformations on the resilient distributed dataset (RDD) created for manipulation of out data. 

## Analysis of cpu loss due to maintenance

In this step we are interested in estimating how much CPU is lost due to maintenance. To do so, we will process data on the _machine_events_ files. We will need first to set an RDD with the amount of cpu removed during the processing. This information would take a new form to look like this:

```(machine_id, (event_type, cpu, 1)) ```

The one value at the end will be used posteriously in our calculations. 

The code to reuce the original _RDD_ to this structure is a bit complex and looks like this:

```Python 
cpu_removed = entries.filter(lambda x: x[2] != u'2' and x[4] is not u'')\
	.map(lambda x:(x[1],(int(x[2]),float(x[4]),1)) if x[2]==u'1' else (x[1],(int(x[2]),0,1)))\
	.reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1], x[2]+y[2]))\
    .filter(lambda x: x[1][0] != 0);
```
Following these operations we need to compute the amount of cpu lost for all removals represented in the form:
```(nb of removals, cpu loss)```
The code to reduce our _RDD_ to this form looks like this:
```Python
cpu_loss_all = cpu_removed.map(lambda x: (x[1][0], x[1][1])).reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))
```
Finally we can extract the total number of maintenances and the amount of cpu lost by them, which finally enables us to estimate the percentages that we want:

```Python
cpu_loss_maintenance = cpu_removed.map(lambda x: (x[1][0], x[1][1]) if 2*x[1][0]+1 == x[1][2] else (x[1][0], x[1][1] - x[1][1]/x[1][0])).filter(lambda x: x[0] > 0).reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]))

tot_cpu_loss_all = cpu_loss_all[1] / cpu_loss_all[0] * 100

tot_cpu_loss_mtnc = cpu_loss_maintenance[1] / cpu_loss_maintenance[0] * 100

tot_cpu_loss_fail = tot_cpu_loss_all - tot_cpu_loss_mtnc
```
The same procedure can be repeated to extract infromation related to memory loss. And finally, the results are as follows:

```
RESULTS
```
Analysis, we can see that....


## Analysis of the distribution of machines according to CPU capacity

BLABLABLA

## Question: Do tasks with low priority have a higher probability of being evicted?

For this analysis we will use the _task events_ file. We are interested in computing the probability of a given task event to be an
**eviction event**, in relation to its _priority_. That is, in relation to the priority of the job for which this given task belongs to. 
Indeed, the priority of a job determines the priority of its tasks. In other words, all tasks related to a job will have the same priority.

In terms of transformations on our __RDD__, we intend to __map__ it into a new structure that ideally contains one entry for each different priority level that is present in the data set. 
Each entry in this new structure will in turn contain two distinct pieces of information: 

* The probability of an **eviction event** for a task with this given priority. 
* The total number of **all the events** that happened to any task with the same parent Job.

This is done because we consider the Probability of Eviction as the number of eviction events for any task belonging to a job divided by the number of the total of events for any task belonging to this same job. The task indexes individually don't have a great importance because the average would remain the same for the Job as a whole.

To achieve this organization, each entry (task event) in the inital _RDD_ will be eventually mapped to the following shape: 

```
For each task event T:
  (Priority of T, (ID of T's Job, Event Type))
```
Following, we will contruct an _Eviction Rate by Priority_ RDD, which will consist of yet a new arrangement: 

```
For each task event T:
  If Event Type is Eviction:
    (Priority of T , (1,0))
  Else:
    (Priority of T , (0,1))
```
With this new RDD we can know if any given task event was of type _eviction_ or not. This is usefull to have a final number of total evictions and of total events for any priority.
Finally we will reduce our set by priority key, which means that we will reduce the set to one single entry per priority, adding all this information together and computing the probability at the end. The command looks like this:

```Python
reduction = evictRate_byPriority.reduceByKey(lambda x, y: (x[0] + y[0], x[1]+y[1])).map(lambda x: (int(x[0]), (100*(x[1][0]/(x[1][0]+x[1][1])), x[1][0]+x[1][1])))
```

The results are as follows:

```
Probability of evict event by priority:
Priority 0: 16.54% of chances of having a task evicted. Out of 455070 events with this priority level.
Priority 1: 2.09% of having a task evicted. Out of 72411 events with this priority level.
Priority 2: 0.04% of having a task evicted. Out of 174466 events with this priority level.
Priority 4: 0.04% of having a task evicted. Out of 181678 events with this priority level.
Priority 6: 0.11% of having a task evicted. Out of 2609 events with this priority level.
Priority 7: 0.0% of having a task evicted. Out of 3 events with this priority level.
Priority 8: 0.10% of having a task evicted. Out of 8446 events with this priority level.
Priority 9: 0.05% of having a task evicted. Out of 101764 events with this priority level.
Priority 10: 0.05% of having a task evicted. Out of 2042 events with this priority level.
Priority 11: 0.0% of having a task evicted. Out of 13090 events with this priority level.
```
We can conclude that, indeed, it seems that tasks with low priorities have higher chances of being evicted. This makes sense too, because it is precisely to make available resources to other higher priority tasks that one task may be evicted.
We can see that for any given event that happens to a lowest, priority zero, task there is a AAAAAAAAAAA percent chance of it being an eviction. For the higher priority tasks, starting already from second level, the chance is less then 1% of such an event happening. Finally, out of BBBBBB events that happened to level 11 priority tasks, none of them were evictions.


## What is the distribution of the number jobs/tasks per scheduling class?

We are interested in knowing the ditribution of tasks and jobs in relation to the different scheduling classes. This analysis will be done in terms of jobs and in terms of tasks, as such, the files from _job_events_ as well as _task_events_ will be used.
The procedure will be the same for jobs and tasks, first we will map all the events in terms of Scheduling class and job_id. Following we need to eliminate any duplicates because there may be many events for the same task. Finally, we will reduce this newly obtained map by key (scheduling class). This way we can count how many tasks belong to each scheduling class. In the end we will be able to compare it to a total number of tasks to assess the distribution. The code looks something like this:
```Python
allEvents = entries.map(lambda x: (int(x[7]), x[2] )).distinct().map(lambda x: (x[0], 1))
reduction = allEvents.reduceByKey(add)  
```

The same procedure for an _RDD_ containing job_events:

```Python
allEvents = jobEntries.map(lambda x: (x[5], x[2] )).distinct().map(lambda x: (x[0], 1))
reduction2 = allEvents.reduceByKey(add)
```

The final distribution is as follows:

```
RESULTADO FINAL
```

As expected, we can see that the distributions ammount to 100% together, which is expected. It is also worthwile to mention that the distribution for jobs by scheduling class is very similar to that of the tasks by scheduling class. This is also expected because tasks have the same scheduling class as their parent jobs. Moreover, the files analyzed correspond to the same time frame which would mean that jobs and their related tasks would be activated within this window.

This analysis was computed by _spark_ in AAAAAA ms, processing over BBBBBB files which contain CCCCCCC thousand lines of data. Once again, the transformations _map_ and _reduce_ came very useful to conduct the operations necessary on the dataset in a conscise way. 

## What is the percentage of jobs/tasks that got killed or evicted depending on the scheduling class?

For this question, we will have two approaches to try and measure this relation.

* Firstly, we will split the task events into two groups. The first group contains all events that correspond to a _kill or evict_ action. The second group will be all events, including _kill or evict_. We can then organize each event by scheduling class and finally reduce them to have a final relation of _kill or evict_ events by total events for any given sheduling class. This will hopefully allow us to estimate, for any given event, what is the probabilty that it will be an eviction or a kill event, based on the scheduling class of this task.

* Secondly, we will try to change the point of view a little bit. Given that a task has a specific scheduling class, what is the chance that this task will be evicted or killed at somepoint. What is the chance that it will not be killed nor evicted? In order to do so, we'll again reduce the number of total events by scheduling class. Following, we'll do the same, except that we'll count the total number with a filtered _RDD_ containing only _kill or evict_ events. This will enable us to count distinct tasks and see how many were killed or evicted at some point at least once. 

The basic transformations are:
```Python
#First proposition
allEvents = entries.map(lambda x: (x[7], (1,1)) if (x[5] == '2' or x[5] == '5') else (x[7], (0,1))).reduceByKey(lambda x, y: (x[0] + y[0], x[1]+y[1]))
percentages = allEvents.map(lambda x: (x[0], (100*(x[1][0]/(x[1][0]+x[1][1])))))

#Second proposition
allEvents = entries.map(lambda x: (x[7], (1, (x[2], x[3])))).distinct().reduceByKey(lambda x, y: (x[0] + y[0], x[1]))
tasksThatWereEvictedOrKilled = allEvents.filter(lambda x: x[5] == u'2' or x[5] ==u'5').map(lambda x: (x[7], (1, (x[2], x[3])))).distinct().reduceByKey(lambda x, y: (x[0] + y[0], x[1]))

```
After manipulating the results to calculate averages, they are printed on the output terminal. We can then generate the following graphics:

![Step 1](https://github.com/gabrijob/DM_proj/blob/master/images/killedEvictedBySchedulingClass-1.png "Step 1 Results")
![Step 2](https://github.com/gabrijob/DM_proj/blob/master/images/killedEvictedBySchedulingClass-2.png "Step 2 Results")

```
First Step
Probability of task event being EVICT or KILL based on scheduling class:
('0', 8.422286770195647)                                                        
('1', 6.850361433152736)
('2', 22.141683206075324)
('3', 17.02527194943253)
First part finished. Time elapsed: 191.8826973438263 seconds.

Second Step
Percentage analysis
Scheduling class 0 :32.03944801867268 percent.                                  
Scheduling class 1 :18.265014034833516 percent.                                 
Scheduling class 2 :66.9128349599222 percent.                                   
Scheduling class 3 :49.67025745734469 percent.                                  
Total time elapsed: 564.0192849636078 seconds.
``` 
We can see that...
This computations, using _map_, _reduce_ and _filter_ operations, were conducted by _Spark_ in AAAAAAAAAA ms iterating around 32,959,317 lines of data, from the first 100 _task_event_ files available in the google dataset. 
