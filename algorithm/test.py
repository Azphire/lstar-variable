from learner import *
from automaton import *

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

# TODO: 需要完善dfa的构建
# 把所有被归为同一状态的S存到一组，需要确保每一个添加进这一组的S和其他所有列都不冲突，否则继续看是否和其他组兼容，都不兼容就新建一组
# 需要按照所有S列构建状态转移，即使S+char不在S中
alphabet_3 = ["a", "b"]
states_3 = [1, 2, 3, 4]
dfa_3 = {
           1: {
               "a": [Trans(0, 2, 1, "+", 1), Trans(3, varMax, 3, "#", 0)],
               "b": [Trans(0, varMax, 2, "#", 0)]},
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
    student = Student(machine_3)
    student.learn()
