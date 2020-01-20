

# Data Project


Questão 2 --> Feita
Vou fazer mais algumas análises parecidas (perdas de memoria, perdas em geral)

Faltam questões usando os arquivos de jobs e task

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

## Are there tasks that consume significantly less resources than what they requested?
Yes.

## What is the distribution of the number jobs/tasks per scheduling class?

Jobs tasks scheduling class analysis


## What is the percentage of jobs/tasks that got killed or evicted depending on the scheduling class?
