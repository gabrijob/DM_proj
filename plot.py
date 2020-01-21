
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
plt.bar(y_pos, dataStep1, align='center', alpha=0.5, color ='g')
plt.xticks(y_pos, objects)
plt.ylabel('Distribution %')
plt.title('Probability of a given task event be EVICT or KILL')
plt.show()


#Step 1
plt.bar(y_pos, dataStep2, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Distribution %')
plt.title('Probability of task be EVICTED or KILLED')
plt.show()