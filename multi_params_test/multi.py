import sys
import time

from algorithm_multi.learner import Student
from algorithm_multi.automaton import Trans, Machine
from multi_params_test.randomDFA import random_dfa, fetch_dfa, store_machine

alphabet_1 = ["a", "b"]
states_1 = [1, 2]
dfa_1 = {
           1: {
               "a": [Trans((0, 0), 1, (0, 1)), Trans((0, 1), 1, (1, 1))],
               "b": [Trans((0, 1), 2, (1, 1)), Trans((1, 1), 1, (1, 1))]},
           2: {
               "a": [Trans((1, 1), 2, (1, 1))],
               "b": [Trans((1, 1), 2, (1, 1))]}
        }
machine_1 = Machine(alphabet_1, states_1, dfa_1, 1, (0, 0), [2])

if __name__ == '__main__':
    # student = Student(machine_1)
    # result = student.learn()

    sys.setrecursionlimit(100000)
    start_time = 0
    fn_list = []
    t = []

    for i in range(10):
        m, fn = random_dfa(["a", "b"], 20, 2)
        fn_list.append(fn)

        start_time = time.time()
        student = Student(m)
        result = student.learn()
        time_using = time.time() - start_time
        t.append(time_using)

        store_machine(result, time_using, fn + 'learn.json')

    for i in range(len(fn_list)):
        print(fn_list[i])
        print("time: ", t[i])

    t.sort()
    print('')

    for ti in t:
        print(ti)

    # m, fn = random_dfa(["a", "b"], 4)
    # print(fn)
    # student = algorithm_v2.learner.Student(m)
    # result = student.learn()
    # store_machine(result, fn + 'learn.json')

    # fn = './dfa/20220513191422'
    # m = fetch_dfa(fn + '.json')
    # student = Student(m)
    # result = student.learn()
    # store_machine(result, fn + 'learn.json')