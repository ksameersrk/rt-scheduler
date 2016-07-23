'''
A python script to simulate EDF and RM algorithm
'''
__author__ = "Sameer Ravindra Kulkarni"
__email__ = "ksameersrk@gmail.com"
__usn__ = "1PI13CS132"

import sys
import copy

class Task:
    '''
    A Task object which has which has attributes
    like priority, period, task_number, etc.
    It has getters and setters method to make it
    convient to work with
    '''
    def __init__(self, parameters_):
        self.priority_ = 1 / parameters_[1]
        self.task_number_ = int(parameters_[0])
        self.period_ = parameters_[1]
        self.execution_time_ = parameters_[2]
        self.time_remaining = parameters_[2]
        self.deadline = 0
        if len(parameters_) == 3:
            self.phase_ = 0.0
        else:
            self.phase_ = parameters_[3]

    def get_period(self):
        return self.period_

    def get_task_number(self):
        return self.task_number_

    def get_priority(self):
        return self.priority_

    def get_execution_time(self):
        return self.execution_time_

    def get_phase(self):
        return self.phase_

    def get_deadline(self):
        return self.deadline

    def set_deadline(self, deadline):
        self.deadline = deadline

    def get_time_remaining(self):
        return self.time_remaining

    def decrement_time_remaining(self):
        self.time_remaining -= 1

    def set_priority(self, index):
        if self.get_deadline() - index:
            self.priority_ = 1/(self.get_deadline() - index)

    def __str__(self):
        string = 'Task Number : '+str(self.get_task_number())
        string += '\nPriority : '+str(self.get_priority())
        string += '\nTime remaining : '+str(self.get_time_remaining())
        string += '\nDeadline : '+str(self.get_deadline())+'\n'
        return string


def gcd(a, b):
    '''
    Finds the GCD of two numbers
    '''
    while b:
        a, b = b, a%b

    return a


def lcm(a, b):
    '''
    Finds the LCM of two numbers
    '''
    return (a * b)/gcd(a, b)


def lcm_for_list(list_periods):
    '''
    Finds the LCM of N numbers
    '''
    curr_value = list_periods[0]
    for i in list_periods[1:]:
        curr_value = lcm(curr_value, i)

    return int(curr_value)


def write_activation_trace(input_tasks, filename, hyper_period):
    '''
    Finds the activation trace, i.e the release of all
    the Tasks (taking care of tasks with non-zero phase value)
    '''
    trace = []
    release = {}
    for i in range(hyper_period+1):
        tmp = [i]
        tmp_task = []
        for task in input_tasks:
            if not i % (task.get_period()+task.get_phase()):
                tmp.append(task.get_task_number())
                tmp_task.append(task)

        if not len(tmp) == 1:
            trace.append(','.join([str(x) for x in [tmp[0]]+sorted(tmp[1:])]))
            if i != hyper_period:
                release[i] = sorted(tmp_task,
                    key=lambda x : x.get_period(),
                    reverse=True)

    trace_string = '\r\n'.join(trace)
    #with open(filename+'_activation_trace.txt', 'w') as f:
        #f.write(trace_string)

    return release


def simulate_schedule(input_tasks, release, filename, hyper_period, option):
    '''
    Simulates either EDF or RM, based on value of option field.
    value of option can take either 'EDF' or 'RM'
    '''
    filename = filename+'_'+option+'_schedule.txt'
    curr_tasks = []
    if 0 in release.keys():
        curr_tasks = copy.deepcopy(release[0])
        for task in curr_tasks:
            task.set_deadline(task.get_period())

    result = []
    removed_tasks = []
    curr_tasks.sort(key=lambda x: x.get_priority(), reverse=True)
    for index in range(1, hyper_period+1):
        tmp = [index]
        if curr_tasks:
            tmp_task = curr_tasks[0]
            tmp.append(tmp_task.get_task_number())
            tmp_task.decrement_time_remaining()
        else:
            tmp.append(-1)

        for task in curr_tasks[:]:
            if task.get_deadline() == index:
                tmp.append(str(task.get_task_number())+'*')
                curr_tasks.remove(task)
                removed_tasks.append(task.get_task_number())
            elif task.get_time_remaining() == 0:
                curr_tasks.remove(task)

        if index in release.keys():
            next_tasks = copy.deepcopy(release[index])
            for task in next_tasks:
                task.set_deadline(index+task.get_period())

            curr_tasks.extend(next_tasks)

        if option == 'EDF':
            for task in curr_tasks:
                task.set_priority(index)

        curr_tasks.sort(reverse=True,
                key=lambda x: (
                    x.get_priority(),
                    x.get_period(),
                    -1 * x.get_task_number()
                    ))
        tmp = ','.join([str(x) for x in tmp])
        result.append(tmp)

    #with open(filename, 'w') as f:
        #f.write('\r\n'.join(result))

    utilization = 0.0
    for i in input_tasks:
        utilization += i.get_execution_time()/i.get_period()

    u2 = ((len(input_tasks)-len(set(removed_tasks)))/len(input_tasks)) * 100
    u2 = int(u2)
    utilization = int(utilization * 100)
    num = len(input_tasks) - len(set(removed_tasks))
    tot = len(input_tasks)
    return [utilization, u2, num, tot]


if __name__ == '__main__':
    input_file = sys.argv[1]
    input_tasks = []
    for line in open(input_file, 'r').readlines():
        tmp_task = list(map(float, line.strip().split()))
        if len(tmp_task) >= 3:
            input_tasks.append(Task(tmp_task))

    filename = input_file.split('/')[-1].split('.')[0].strip()
    input_tasks.sort(key=lambda x: x.get_priority(), reverse=True)
    hyper_period = lcm_for_list([x.get_period() for x in input_tasks])
    release = write_activation_trace(input_tasks, filename, hyper_period)
    n1 = simulate_schedule(input_tasks, release, filename, hyper_period, 'RM')
    n2 = simulate_schedule(input_tasks, release, filename, hyper_period, 'EDF')
    with open('RM.txt', 'a') as f:
        f.write(' '.join([str(x) for x in n1])+'\r\n')
    with open('EDF.txt', 'a') as f:
        f.write(' '.join([str(x) for x in n2])+'\r\n')
