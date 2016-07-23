import matplotlib.pyplot as plt

rm_x1 = []
rm_x2 = []
rm_y = []

edf_x1 = []
edf_x2 = []
edf_y = []

for line in  open('RM.txt', 'r').readlines():
    rm = (list(map(float, line.strip().split(' '))))
    rm_x1.append(rm[0])
    rm_x2.append(rm[1])
    rm_y.append(rm[2] == rm[3])

for line in  open('EDF.txt', 'r').readlines():
    edf = (list(map(float, line.strip().split(' '))))
    edf_x1.append(edf[0])
    edf_x2.append(edf[1])
    edf_y.append(edf[2] == edf[3])

rm_1y = [0 for x in range(0,11)]
rm_2y = [0 for x in range(0,11)]
edf_1y = [0 for x in range(0,11)]
edf_2y = [0 for x in range(0,11)]

for i in range(len(rm_y)):
    if rm_y[i]:
        rm_1y[int(rm_x1[i]//10)] += 1
        rm_2y[int(rm_x2[i]//10)] += 1

for i in range(len(edf_y)):
    if edf_y[i]:
        edf_1y[int(edf_x1[i]//10)] += 1
        edf_2y[int(edf_x2[i]//10)] += 1

x = [x for x in range(0, 101, 10)]

plt.figure(1)
plt.subplot(211)
plt.plot(x, rm_1y, 'r')
plt.plot(x, rm_2y, 'g')
plt.axis([0, 120, 0, 100])
plt.ylabel('Number of schedulable tasks')
plt.xlabel('Tasks sets')
plt.title('Rate-monotonic scheduling')
plt.text(5, 80, 'Therotical Values', color='r')
plt.text(5, 70, 'Practical Values', color='g')

plt.subplot(212)
plt.plot(x, edf_1y, 'r')
plt.plot(x, edf_2y, 'g')
plt.axis([0, 120, 0, 100])
plt.ylabel('Number of schedulable tasks')
plt.xlabel('Tasks sets')
plt.title('Earliest deadline first scheduling')
plt.text(5, 80, 'Therotical Values', color='r')
plt.text(5, 70, 'Practical Values', color='g')

plt.show()
