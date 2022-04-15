import algorithm_v2.learner
import algorithm_v0.learner
from test.randomDFA import random_dfa, fetch_dfa, store_machine
import time


if __name__ == '__main__':
    time0 = 0
    time2 = 0
    for i in range(1):
        m, fn = random_dfa(["a", "b", "c"], 6)
        print(fn)

        t = time.time()
        student0 = algorithm_v0.learner.Student(m)
        result0 = student0.learn()
        time0 += time.time() - t

        t = time.time()
        student2 = algorithm_v2.learner.Student(m)
        result2 = student2.learn()
        time2 += time.time() - t

        store_machine(result0, fn + 'learn0.json')
        store_machine(result0, fn + 'learn2.json')

    print("time0: ", time0)
    print("time2: ", time2)

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
