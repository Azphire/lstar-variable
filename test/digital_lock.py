from algorithm_v2.learner import *
from algorithm_v2.automaton import *
from test.randomDFA import random_dfa, fetch_dfa, store_machine

if __name__ == '__main__':
    fn = './dfa/DigitalLock'
    m = fetch_dfa(fn + '.json')
    m.accepted = [4]
    student = Student(m)
    result = student.learn()
    store_machine(result, fn + 'learn.json')


