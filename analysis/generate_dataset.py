import random
import os

os.mkdir('dataset_input')
os.chdir('dataset_input')

i=1
while i <= 100:
    file_contents = []
    tmp = []
    n = random.randint(3, 10)
    for j in range(1, n+1):
        task_number = j
        period = random.randint(1, 25)
        execution = random.randint(1, 1+period//6)
        phase = 0
        tmp.append([task_number, period, execution, phase])

    u = 0.0
    for ind in tmp:
        u += ind[2]/ind[1]
        file_contents.append(' '.join([str(x) for x in ind]))

    if u <= 1:
        with open('set'+str(i)+'.txt', 'w') as f:
            f.write('\r\n'.join(file_contents))

        i += 1
