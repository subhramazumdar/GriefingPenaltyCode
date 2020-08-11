import matplotlib.pyplot as plt
import numpy as np
x_axis = [3000,30000,300000,3000000]
cheap = [-233558.2393,-42296.54543,-3650.963667,-343.3499943]
expensive = [3.000114375,26.85616526,234.6044855,1761.434274]





fig_size = plt.rcParams["figure.figsize"] #set chart size (longer than taller)
fig_size[0] = 39
fig_size[1] = 10
plt.rcParams["figure.figsize"] = fig_size
plt.rcParams.update({'font.size': 18}) 

plt.stackplot(x_axis, expensive, colors=['r'])
plt.stackplot(x_axis, cheap, colors=['g'])

plt.plot([],[],color='r', label='Above great case', linewidth=15)

plt.plot([],[],color='g', label='Below low case', linewidth=5)
plt.yticks(np.arange(min(expensive), max(expensive)+1, 100))
plt.legend()

plt.xlabel('Years')
plt.ylabel('Number of companies')
plt.title('Under/over valuation over time')
plt.show()
