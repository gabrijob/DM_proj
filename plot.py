
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

totalElements = 32959317

objects = ('Scheduling Class 0','Scheduling Class 1', 'Scheduling Class 2', 'Scheduling Class 3' )
y_pos = np.arange(len(objects))
print(y_pos)

dataStep1 = [8.422286770195647, 6.850361433152736,22.141683206075324 , 17.02527194943253]
time1 = 193.78793358802795 
dataStep2 = [32.03944801867268, 18.265014034833516, 66.9128349599222, 49.67025745734469]
time2 = 568.072113990783

width = 0.15  # the width of the bars

#Step 1
#plt.bar(y_pos, dataStep1, align='center', alpha=0.5, color ='g')
#plt.xticks(y_pos, objects)
#plt.ylabel('Distribution %')
#plt.title('Probability of a given task event be EVICT or KILL')
#plt.show()


#Step 2
#plt.bar(y_pos, dataStep2, align='center', alpha=0.5)
#plt.xticks(y_pos, objects)
#plt.ylabel('Distribution %')
#plt.title('Probability of task be EVICTED or KILLED')
#plt.show()


#task_priority_eviction_analysis.py 
#objects = ('Priority 0','Priority 1', 'Priority 2', 'Priority 3','Priority 4','Priority 5','Priority 6','Priority 7','Priority 8','Priority 9','Priority 10','Priority 11','Priority 12','Priority 13' )
#y_pos = np.arange(len(objects))
#data = [7.629659465037097, 8.070885808483835, 1.0347617678510752, 8.374384236453201, 0.1140258749190515, 0.0, 0.01775301998595539, 0.5186483776835573, 0.10400923130988833, 1.1040664626147791, 0.0 , 0.0,0.0, 0.0 ]

#plt.bar(y_pos, data, align='center', alpha=0.5, color ='m')
#plt.xticks(y_pos, objects)
#plt.ylabel('Probability %')
#plt.title('Task Event Rate - EVICT by Priority')
#plt.show()

#As we can see, indeed it looks like tasks with lower priorities have a much higher chance if suffering an eviction event. Indeed, tasks of priority 0,1 and 3 seem to have around 7 or 8 times higher rates of eviction then tasks which have other levels of priority. This means that, on average, out of all events that happen to a task which has priority 0,1 or 3, around 8%  of these events will be an eviction. 



#JOBS TASKS SCHEDULING CLASS ANALYSIS

objects = ('Scheduling Class 0','Scheduling Class 1', 'Scheduling Class 2', 'Scheduling Class 3' )
y_pos = np.arange(len(objects))
print(y_pos)

data = [38.23445156426687 , 32.99811534112326 , 27.215981907274784 , 1.5514511873350922]

plt.bar(y_pos, data, align='center', alpha=0.5, color ='b')
plt.xticks(y_pos, objects)
plt.ylabel('Distribution %')
plt.title('Jobs and Scheduling Class')
plt.show()


#Segundo o google doc, jobs normalmenteconsitem de tasks identicas, que exigem a mesma quantidade de recursos e possuem as mesmas prioridades e scheduling class. lOGO, isso é esperado. 

#Spark can accomplish this 