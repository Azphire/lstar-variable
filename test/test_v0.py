from algorithm_v0.learner import *
from test.randomDFA import random_dfa, fetch_dfa, store_machine


if __name__ == '__main__':
    # for i in range(10):
    #     m, fn = random_dfa(["a", "b"], 6)
    #     print(fn)
    #     student = Student(m)
    #     result = student.learn()
    #     store_machine(result, fn + 'learn.json')

    m, fn = random_dfa(["a", "b"], 4)
    print(fn)
    student = Student(m)
    result = student.learn()
    store_machine(result, fn + 'learn.json')

    # fn = './dfa/20220408154510'
    # m = fetch_dfa(fn + '.json')
    # student = Student(m)
    # result = student.learn()
    # store_machine(result, fn + 'learn.json')
