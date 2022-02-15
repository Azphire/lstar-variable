from automaton import Machine, Trans
from observationTable import ObservationTable, is_same_state
varMax = 10
lenMax = 10


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
        print("查找反例中")
        for char in self.alphabet:
            test_result = self.test_machine.member_query(pre + char)[0]
            real_result = self.machine.member_query(pre + char)[0]
            if test_result != real_result:
                print("反例: " + pre + char)
                return pre + char
            if step < lenMax:
                next_str = self.find_ex_step(step + 1, pre + char)
                if next_str:
                    return next_str
        return None

    # 返回是否等价，反例
    def eq_query(self, test_machine: Machine):
        self.test_machine = test_machine
        example = self.find_ex_step(0, "")
        if example:
            print("NOT EQUIVALENT! " + example)
            return False, example

        else:
            print("EQUIVALENT")
            return True, None


class Student:

    def __init__(self, machine: Machine):
        self.teacher = Teacher(machine)
        self.obTable = ObservationTable(machine.alphabet)
        self.learning_machine = None

    def row(self, sentence):
        result = []
        for e in self.obTable.E:
            result.append(self.member_query(sentence + e))
        print(result)
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
        print("is closed")
        return True

    def is_consistent(self):
        for s1 in self.obTable.S:
            for s2 in self.obTable.S:
                if is_same_state(self.row(s1), self.row(s2)):
                    for char in self.obTable.alphabet:
                        if not is_same_state(self.row(s1 + char), self.row(s2 + char)):
                            return False
        print("is consistent")
        return True

    def close(self):
        for s in self.obTable.S:
            for char in self.obTable.alphabet:
                for s2 in range(len(self.obTable.S)):
                    if is_same_state(self.row(s + char), self.row(self.obTable.S[s2])):
                        break
                    if s2 == len(self.obTable.S) - 1:
                        self.obTable.S.append(s + char)
                        self.obTable.T.append([self.row(s + char)])

    def consist(self):
        for s in self.obTable.S:
            for s2 in self.obTable.S:
                if is_same_state(self.row(s), self.row(s2)):
                    print(self.row(s), " = ", self.row(s2))
                    for char in self.obTable.alphabet:
                        for e in self.obTable.E:
                            if not is_same_state(self.row(s + char + e), self.row(s2 + char + e)):
                                self.obTable.E.append(char + e)
                                for ind in range(len(self.obTable.S)):
                                    self.obTable.T[ind].append(self.member_query(self.obTable.S[ind] + char + e))

    # 进行闭合和完备观察表的操作
    def close_and_consist(self):
        not_satisfied = True

        while not_satisfied:
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
    def count_state(self):
        counter = 1
        state_list = [0]
        accepted = []
        total = len(self.obTable.S)
        if self.member_query(self.obTable.S[0])[0] == 1:
            accepted.append(0)
        for i in range(1, total):
            new_state = True
            for j in range(i):
                if is_same_state(self.row(self.obTable.S[i]), self.row(self.obTable.S[j])):
                    state_list.append(state_list[j])
                    new_state = False
            if new_state:
                state_list.append(counter)
                counter = counter + 1
                if self.member_query(self.obTable.S[i])[0] == 1:
                    accepted.append(counter)
        return counter, state_list, accepted

    # 构造dfa
    def build_dfa(self):
        state_num, state_list, accepted = self.count_state()
        dfa_states = []
        dfa_map = {}
        # 初始化dfa map
        for i in range(state_num):
            dfa_states.append(i)
            dfa_map[i] = {}
            for char in self.teacher.alphabet:
                dfa_map[i][char] = [Trans(0, varMax, i, "#", 0)]
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
                n, opt, opt_num = self.teacher.full_query(sentence)
                self.learning_machine.update_once(current_state, char, Trans(n, n, target_state, opt, opt_num))

    def learn_dfa(self):
        while True:
            self.close_and_consist()
            self.build_dfa()
            is_equal, example = self.teacher.eq_query(self.learning_machine)
            if is_equal:
                print("dfa:")
                print(self.learning_machine.dfa)
                print("accept:")
                print(self.learning_machine.accepted)
                return
            else:
                for x in range(len(example)):
                    if example[x:] in self.obTable.S:
                        continue
                    self.obTable.S.append(example[x:])
                    self.obTable.T.append(self.row(example[x:]))