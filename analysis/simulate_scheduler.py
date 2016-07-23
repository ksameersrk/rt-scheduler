import subprocess
import os

for i in range(1, 101):
    p = subprocess.Popen(['python3', './scheduler.py',
        os.getcwd()+'/dataset_input/set'+str(i)+'.txt'])
    p.wait()
    print('Dataset', i, 'done!')
