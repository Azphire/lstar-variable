from typing import Tuple

from algorithm_v2.automaton import Machine, Trans
from algorithm_v2.observationTable import ObservationTable, is_same_state, no_conflict
from algorithm_v2.equivalenceQuery import EquivalenceQuery
varMax = 3
lenMax = 1000000


class Teacher:

    def __init__(self, machine: Machine):
        self.machine = machine
        self.alphabet = machine.alphabet
        self.test_machine = None

    def get_alphabet(self):
        return self.machine.alphabet

    def member_query(self, sentence):
        return self.machine.member_query(sentence)

    # 返回最后一次状态转换的参数值、运算符、运算数字
    def full_query(self, sentence):
        return self.machine.full_query(sentence)

    def find_ex_step(self, step, pre):
        for char in self.alphabet:
            test_result = self.test_machine.member_query(pre + char)[0]
            real_result = self.machine.member_query(pre + char)[0]
            if test_result != real_result:
                return pre + char
            if step < lenMax - 1:
                next_str = self.find_ex_step(step + 1, pre + char)
                if next_str:
                    return next_str
        return None

    # 返回是否等价，反例
    def eq_query(self, test_machine: Machine):
        self.test_machine = test_machine
        print("查找反例中")
        example = self.find_ex_step(0, "")
        if example:
            print("不等价，反例： " + example)
            return False, example

        else:
            print("等价")
            return True, None


class Student:

    def __init__(self, machine: Machine):
        self.teacher = Teacher(machine)
        self.obTable = ObservationTable(machine.alphabet)
        self.learning_machine = None
        self.obTable.T = [[] for x in range(len(self.obTable.S))]
        self.obTable.T[0].append(self.member_query(""))
        i = 1
        for a in machine.alphabet:
            self.obTable.T[i].append(self.member_query(a))
            i += 1

    def row(self, sentence):
        if sentence in self.obTable.S:
            return self.obTable.T[self.obTable.S.index(sentence)][:]
        if sentence in self.obTable.R:
            return self.obTable.RT[self.obTable.R.index(sentence)][:]
        result = []
        for e in self.obTable.E:
            result.append(self.member_query(sentence + e))
        print("添加R：", sentence)
        self.obTable.R.append(sentence)
        self.obTable.RT.append(result)
        return result

    # 返回该句子的接受与否和参数值
    def member_query(self, sentence):
        return self.teacher.member_query(sentence)

    def is_closed(self):
        for s in self.obTable.S:
            for char in self.obTable.alphabet:
                for s2 in range(len(self.obTable.S)):
                    if is_same_state(self.row(s + char), self.row(self.obTable.S[s2])):
                        break
                    if s2 == len(self.obTable.S) - 1:
                        return False
        for s in self.obTable.S:
            if s in self.obTable.R:
                del self.obTable.RT[self.obTable.R.index(s)]
                self.obTable.R.remove(s)

        print("已闭合")
        return True

    def is_consistent(self):
        for s1 in self.obTable.S:
            for s2 in self.obTable.S:
                if s1 == s2:
                    continue
                if is_same_state(self.row(s1), self.row(s2)):
                    for char in self.obTable.alphabet:
                        if not is_same_state(self.row(s1 + char), self.row(s2 + char)):
                            return False
        print("已完备")
        return True

    def close(self):
        print("闭合观察表")
        for s in self.obTable.S:
            for char in self.obTable.alphabet:
                for s2 in range(len(self.obTable.S)):
                    if is_same_state(self.row(s + char), self.row(self.obTable.S[s2])):
                        break
                    if s2 == len(self.obTable.S) - 1:
                        self.obTable.T.append(self.row(s + char))
                        self.obTable.S.append(s + char)
                        print("添加S：", s + char)

                        if s + char in self.obTable.R:
                            del self.obTable.RT[self.obTable.R.index(s + char)]
                            self.obTable.R.remove(s + char)

    def consist(self):
        print("完备观察表")
        for s in self.obTable.S:
            for s2 in self.obTable.S:
                if s == s2:
                    continue
                if is_same_state(self.row(s), self.row(s2)):
                    new_add_e = []
                    for char in self.obTable.alphabet:
                        for e in self.obTable.E:
                            if e in new_add_e:
                                continue
                            if not is_same_state(self.row(s + char + e), self.row(s2 + char + e)):
                                if char + e in self.obTable.E:
                                    continue
                                # print(s + char + e, " != ", s2 + char + e)
                                # print(self.row(s + char + e), self.row(s2 + char + e))
                                self.obTable.E.append(char + e)
                                print("添加E：", char + e)
                                new_add_e.append(char + e)
                                for ind in range(len(self.obTable.S)):
                                    member = self.member_query(self.obTable.S[ind] + char + e)
                                    self.obTable.T[ind].append(member)
                                for ind in range(len(self.obTable.R)):
                                    member = self.member_query(self.obTable.R[ind] + char + e)
                                    self.obTable.RT[ind].append(member)

    # 进行闭合和完备观察表的操作
    def close_and_consist(self):
        not_satisfied = True

        while not_satisfied:
            print("S:")
            print(self.obTable.S)
            print("E:")
            print(self.obTable.E)
            print("T:")
            print(self.obTable.T)
            not_satisfied = False

            if self.is_closed():
                pass
            else:
                not_satisfied = True
                self.close()

            if self.is_consistent():
                pass
            else:
                not_satisfied = True
                self.consist()

    # 状态的归纳，返回状态数量、每一列对应的状态列表和接受状态列表
    def count_state(self) -> Tuple[int, list, list]:
        counter = 1
        state_list = [0]
        accepted = []
        total = len(self.obTable.S)
        states_of_s = [[0]]
        if self.obTable.T[0][0][0] == 1:
            accepted.append(0)
        for i in range(1, total):
            new_state = True
            for j in range(len(states_of_s)):
                is_compatible = True
                for s in states_of_s[j]:
                    if no_conflict(self.row(self.obTable.S[i]), self.row(self.obTable.S[s])):
                        pass
                    else:
                        is_compatible = False
                        break
                if is_compatible:
                    state_list.append(j)
                    states_of_s[j].append(i)
                    new_state = False
                    break
            if new_state:
                state_list.append(counter)
                states_of_s.append([i])
                counter = counter + 1
                if self.obTable.T[i][0][0] == 1:
                    accepted.append(counter - 1)
        return counter, state_list, accepted

    # 构造dfa
    def build_dfa(self):
        temp_r = []
        temp_t = []
        for s in self.obTable.S:
            for char in self.obTable.alphabet:
                if s + char not in self.obTable.S:
                    temp_r.append(s + char)
                    temp_t.append(self.row(s + char))
                    # print("添加R：", s + char)

        self.obTable.S += temp_r
        self.obTable.T += temp_t

        state_num, state_list, accepted = self.count_state()

        # print("状态：")
        # print(state_list, accepted)
        dfa_states = []
        dfa_map = {}
        # 初始化dfa map
        for i in range(state_num):
            dfa_states.append(i)
            dfa_map[i] = {}
            for char in self.teacher.alphabet:
                # dfa_map[i][char] = [Trans(0, varMax, i, "#", 0)]
                dfa_map[i][char] = []
        self.learning_machine = Machine(self.teacher.alphabet, dfa_states, dfa_map, 0, accepted)
        # 遍历每一列S，更新dfa
        for i in range(len(self.obTable.S)):
            s = self.obTable.S[i]
            current_state = state_list[i]
            for char in self.obTable.alphabet:
                sentence = s + char
                if sentence not in self.obTable.S:
                    continue
                target_state = state_list[self.obTable.S.index(sentence)]
                n = self.obTable.T[self.obTable.S.index(s)][0][1]
                opt_num = self.obTable.T[self.obTable.S.index(sentence)][0][1]
                self.learning_machine.update_once(current_state, char,
                                                  Trans(n, n, target_state, "=", opt_num))
        self.obTable.S = self.obTable.S[:(len(self.obTable.S) - len(temp_r))]
        self.obTable.T = self.obTable.T[:(len(self.obTable.T) - len(temp_t))]

    def learn(self) -> Machine:
        while True:
            self.close_and_consist()
            self.build_dfa()
            # is_equal, example = self.teacher.eq_query(self.learning_machine)
            is_equal, example = EquivalenceQuery(self.teacher.machine, self.learning_machine).query()
            if is_equal:
                print("等价")
            else:
                print("不等价，反例：", example)
            # print("构建结果：")
            # print("dfa:")
            # print(self.learning_machine.dfa)
            # print("accept:")
            # print(self.learning_machine.accepted)

            if is_equal:
                return self.learning_machine
            else:
                for x in range(len(example) + 1):
                    if example[:x] in self.obTable.S:
                        continue
                    self.obTable.T.append(self.row(example[:x]))
                    self.obTable.S.append(example[:x])
                    print("添加S：", example[:x])

                    if example[:x] in self.obTable.R:
                        del self.obTable.RT[self.obTable.R.index(example[:x])]
                        self.obTable.R.remove(example[:x])
