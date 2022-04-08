from algorithm_v1.learner import *
from algorithm_v1.automaton import *
from test.randomDFA import random_dfa, fetch_dfa, store_machine

# 最简单的成功例子
alphabet_1 = ["a", "b"]
states_1 = [1, 2]
dfa_1 = {
           1: {
               "a": [Trans(0, 0, 1, "+", 1), Trans(1, varMax, 2, "+", 1)],
               "b": [Trans(0, varMax, 1, "#", 0)]},
           2: {
               "a": [Trans(0, varMax, 2, "#", 0)],
               "b": [Trans(0, varMax, 2, "#", 0)]}
        }
machine_1 = Machine(alphabet_1, states_1, dfa_1, 1, [2])

# 暂时不成功，需要解决：相同的变量值，不同状态
# 思路：S列变量值不同的列不可比较
# 已解决

alphabet_2 = ["a", "b"]
states_2 = [1, 2]
dfa_2 = {
           1: {
               "a": [Trans(0, 0, 1, "+", 1), Trans(1, varMax, 2, "#", 0)],
               "b": [Trans(0, varMax, 1, "#", 0)]},
           2: {
               "a": [Trans(0, varMax, 2, "#", 0)],
               "b": [Trans(0, varMax, 2, "#", 0)]}
        }
machine_2 = Machine(alphabet_2, states_2, dfa_2, 1, [2])


alphabet_3 = ["a", "b"]
states_3 = [1, 2, 3, 4]
dfa_3 = {
           1: {
               "a": [Trans(0, 2, 1, "+", 1), Trans(3, varMax, 3, "#", 0)],
               "b": [Trans(0, 1, 1, "+", 1), Trans(2, varMax, 2, "#", 0)]},
           2: {
               "a": [Trans(0, varMax, 4, "#", 0)],
               "b": [Trans(0, 2, 1, "+", 1), Trans(3, varMax, 3, "#", 0)]},
           3: {
               "a": [Trans(0, varMax, 3, "#", 0)],
               "b": [Trans(0, varMax, 3, "#", 0)]},
           4: {
               "a": [Trans(0, varMax, 3, "#", 0)],
               "b": [Trans(0, varMax, 3, "#", 0)]}
        }
machine_3 = Machine(alphabet_3, states_3, dfa_3, 1, [4])

if __name__ == '__main__':
    # student = Student(machine_3)
    # result = student.learn()

    # for i in range(10):
    #     m, fn = random_dfa(["a", "b"], 4)
    #     print(fn)
    #     student = Student(m)
    #     result = student.learn()
    #     store_machine(result, fn + 'learn.json')

    # m, fn = random_dfa(["a", "b"], 4)
    # print(fn)
    # student = Student(m)
    # result = student.learn()
    # store_machine(result, fn + 'learn.json')

    fn = './dfa/20220408135937'
    m = fetch_dfa(fn + '.json')
    student = Student(m)
    result = student.learn()
    store_machine(result, fn + 'learn.json')

