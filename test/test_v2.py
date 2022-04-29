import algorithm_v2.learner
import algorithm_v0.learner
from test.randomDFA import random_dfa, fetch_dfa, store_machine
import time
import sys

if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    time0 = 0
    time2 = 0
    fn_list = []
    t0 = []
    t2 = []
    for i in range(3):
        # fn = './dfa/20220428173622'
        # m = fetch_dfa(fn + '.json')
        m, fn = random_dfa(["a", "b"], 50)
        fn_list.append(fn)

        t = time.time()
        student0 = algorithm_v0.learner.Student(m)
        result0 = student0.learn()
        time0 += time.time() - t
        t0.append(time0)

        t = time.time()
        student2 = algorithm_v2.learner.Student(m)
        result2 = student2.learn()
        time2 += time.time() - t
        t2.append(time2)

        store_machine(result0, fn + 'learn0.json')
        store_machine(result2, fn + 'learn2.json')

    for i in range(len(fn_list)):
        print(fn_list[i])
        print("time0: ", t0[i])
        print("time2: ", t2[i])

    # m, fn = random_dfa(["a", "b"], 4)
    # print(fn)
    # student = algorithm_v2.learner.Student(m)
    # result = student.learn()
    # store_machine(result, fn + 'learn.json')

    # fn = './dfa/20220408154510'
    # m = fetch_dfa(fn + '.json')
    # student = Student(m)
    # result = student.learn()
    # store_machine(result, fn + 'learn.json')
