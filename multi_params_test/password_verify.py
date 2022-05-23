from algorithm_multi.learner import *
from multi_params_test.randomDFA import random_dfa, fetch_dfa, store_machine
from multi_params_test.generatePasswordVerify import generatePasswordVerify

if __name__ == '__main__':
    # fn = './dfa/PasswordVerify'
    # m = fetch_dfa(fn + '.json')
    # m.accepted = [5]
    # student = Student(m)
    # print(student.member_query("AAAAAAAA"))
    # result = student.learn()
    # store_machine(result, 0, fn + 'learn.json')

    m, fn = generatePasswordVerify()
    student = Student(m)
    result = student.learn()
    store_machine(result, 0, fn + 'learn.json')