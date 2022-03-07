varMax = 5
lenMax = 10


class Trans:

    def __init__(self, left, right, target, operator, opt_number):
        self.left = left
        self.right = right
        self.target = target
        self.operator = operator
        self.opt_number = opt_number


class Machine:

    def __init__(self, alphabet, dfa):
        self.dfa = dfa
        self.alphabet = alphabet
        self.q0 = "q0"

    def update_dfa(self, state, char, new_trans: Trans):
        print("update dfa: ", state, char, new_trans)
        update = True
        if state == self.q0:
            state = 'q0'
        while update:
            if new_trans.target == self.q0:
                new_trans.target = 'q0'
            update = False
            for trans in self.dfa[state][char]:
                if trans.target == new_trans.target and \
                        trans.operator == new_trans.operator and \
                        trans.opt_number == new_trans.opt_number:
                    if trans.left == new_trans.left and trans.right == new_trans.right:
                        return
                    if trans.left - 1 <= new_trans.right or trans.right + 1 >= new_trans.left:
                        left = min(trans.left, new_trans.left)
                        right = max(trans.right, new_trans.right)
                        self.dfa[state][char].remove(trans)
                        new_trans = Trans(left, right, new_trans.target, new_trans.operator, new_trans.opt_number)
                        update = True
                        break
                    continue
                over_lap = False
                if trans.left <= new_trans.right:
                    over_lap = True
                    self.dfa[state][char].append(Trans(new_trans.right + 1, trans.right, trans.target,
                                                       trans.operator, trans.opt_number))
                if trans.right >= new_trans.left:
                    over_lap = True
                    self.dfa[state][char].append(
                        Trans(trans.left, new_trans.left - 1, trans.target, trans.operator,
                              trans.opt_number))
                if over_lap:
                    self.dfa[state][char].remove(trans)
            self.dfa[state][char].append(new_trans)

    def transfer(self, state, char, n):
        selected_trans = None
        if state == self.q0:
            state = "q0"
        # 挑选输入字母对应的Tran
        for trans in (self.dfa[state][char]):
            # 条件判断
            if trans.right >= n >= trans.left:
                selected_trans = trans
            if selected_trans:
                cur_n = n
                # 参数运算
                if selected_trans.operator == "#":
                    pass
                elif selected_trans.operator == "+":
                    cur_n = n + selected_trans.opt_number
                elif selected_trans.operator == "-":
                    cur_n = n - selected_trans.opt_number
                elif selected_trans.operator == "=":
                    cur_n = selected_trans.opt_number
                return selected_trans.target, cur_n, selected_trans.operator, selected_trans.opt_number

    def member_query(self, test_str):
        curr_state = "q0"
        n = 0
        opt = ''
        opt_num = 0
        for char in test_str:
            curr_state, n, opt, opt_num = self.transfer(curr_state, char, n)

        if curr_state in self.dfa["f"]:
            # print(test_str, " 被接收")
            return 1, opt, opt_num
        else:
            # print(test_str, " 被拒绝")
            return 0, opt, opt_num

    def sentence_query(self, sentence) -> list:
        curr_state = "q0"
        n = 0
        result = []
        for char in sentence:
            curr_state, n, opt, opt_num = self.transfer(curr_state, char, n)
            result.append((n, opt, opt_num))

        return result

    def find_ex(self, test_dfa, step, pre):
        print("查找反例中")
        for i in range(len(self.alphabet)):
            test_result = test_dfa.member_query(pre + self.alphabet[i])[0]
            real_result = self.member_query(pre + self.alphabet[i])[0]
            if test_result != real_result:
                print("ex: " + pre + self.alphabet[i])
                return pre + self.alphabet[i]
            if step < lenMax:
                next_str = self.find_ex(test_dfa, step + 1, pre + self.alphabet[i])
                if next_str:
                    return next_str
        return None

    def equiv_query(self, test_dfa):
        example = self.find_ex(test_dfa, 0, "")
        if example:
            print("NOT EQUIVALENT! " + example)
            return 0, example

        else:
            print("EQUIVALENT")
            return 1, None


class Learner:

    def __init__(self, alphabet, mat):
        self.alphabet = alphabet
        self.mat = mat
        self.S = [""]
        self.E = [""]
        self.T = [[] for x in range(len(self.S))]
        self.T[0] += [self.member_query("")[0]]
        self.T_str = [""]

    def member_query(self, test_str):
        # print("IS MEMBER? " + "\'" + test_str + "\'")
        return self.mat.member_query(test_str)

    def row(self, s):
        return [self.member_query(s + e)[0] for e in self.E]

    def is_closed(self):
        for s in self.S:
            for a in self.alphabet:
                for s2 in range(len(self.S)):
                    if self.row(s + a) == self.row(self.S[s2]):
                        break
                    if s2 == len(self.S) - 1:
                        return 0
        print("is closed")
        return 1

    def is_consistent(self):
        for s in self.S:
            for s2 in self.S:
                if self.row(s) == self.row(s2):
                    for a in self.alphabet:
                        if self.row(s + a) != self.row(s2 + a):
                            return 0
        print("is consistent")
        return 1

    def generate_dfa(self, strs, state, dfa: Machine, pre, n):
        for char in self.alphabet:
            t_row = []
            for t in strs:
                t_row.append(self.member_query(pre + char + t)[0])
            next_state = "".join(map(str, t_row))
            r, opt, opt_num = self.member_query(pre + char)
            if state == ''.join(map(str, self.T[0])):
                state = "q0"
            try:
                dfa.update_dfa(state, char, Trans(n, n, next_state, opt, opt_num))

                if len(pre) < lenMax:
                    next_n = n
                    if opt == "#":
                        pass
                    elif opt == "+":
                        next_n = n + opt_num
                    elif opt == "-":
                        next_n = n - opt_num
                    elif opt == "=":
                        next_n = opt_num
                    dfa = self.generate_dfa(strs, next_state, dfa, pre + char, next_n)
            except:
                pass
        return dfa

    def update_dfa(self, dfa: Machine, pre_state, target_state, sentence):
        print("更新dfa：" + sentence)
        t = dfa.sentence_query(sentence)[-1]
        char = sentence[:-1]
        if char == '':
            return
        trans = Trans(t[0], t[0], target_state, t[1], t[2])
        dfa.update_dfa(pre_state, char, trans)
        pass

    def learn_dfa(self):
        while True:
            if not self.is_closed():
                for s in self.S:
                    for a in self.alphabet:
                        for s2 in range(len(self.S)):
                            if self.row(s + a) == self.row(self.S[s2]):
                                break
                            if s2 == len(self.S) - 1:
                                self.S += [s + a]
                                self.T_str.append(s + a)
                                self.T.append([self.row(s + a)])
                continue

            if not self.is_consistent():
                for s in self.S:
                    for s2 in self.S:
                        if self.row(s) == self.row(s2):
                            print(self.row(s), " = ", self.row(s2))
                            for a in self.alphabet:
                                for e in self.E:
                                    if self.member_query(s + a + e) != self.member_query(s2 + a + e):
                                        self.E += [a + e]
                                        self.T_str.append(a + e)
                                        for ind in range(len(self.S)):
                                            self.T[ind].append(self.member_query(self.S[ind] + a + e))
                continue

            # case: consistent and closed
            t_dfa = {}
            t_dfa["f"] = []
            for row in self.T:
                t_dfa[''.join(map(str, row))] = {}

                if row[0] == 1:
                    t_dfa["f"] += [''.join(map(str, row))]

            for row in range(len(self.T)):
                for a in self.alphabet:
                    t_dfa[''.join(map(str, self.T[row]))][a] = ''.join(map(str, self.row(self.S[row] + a)))

            q0 = ''.join(map(str, self.T[0]))

            t_dfa["q0"] = t_dfa[q0]
            del t_dfa[q0]

            try_dfa = {}

            for key in t_dfa.keys():
                try_dfa[key] = {}
                for a in self.alphabet:
                    if key == "f":
                        break
                    try_dfa[key][a] = []
                    try_dfa[key][a].append(Trans(0, varMax, key, '#', 0))
                    if t_dfa[key][a] == q0:
                        t_dfa[key][a] = "q0"
            try_dfa["f"] = t_dfa["f"]

            if q0 in t_dfa["f"]:
                t_dfa["f"].remove(q0)
                t_dfa["f"].append("q0")

            for key in t_dfa:
                t = list(t_dfa[key])
                pass
            print("生成dfa中")
            machine = Machine(self.alphabet, try_dfa)
            machine.q0 = q0
            updated_list = []

            for s in self.S:
                for char in self.alphabet:
                    t_row = []
                    for t in self.T_str:
                        t_row.append(self.member_query(s + char + t)[0])
                    target_state = "".join(map(str, t_row))
                    r, opt, opt_num = self.member_query(s + char)
                    pre_state = ''.join(map(str, self.row(s)))
                    if pre_state == ''.join(map(str, self.T[0])):
                        pre_state = "q0"
                    if target_state == ''.join(map(str, self.T[0])):
                        target_state = 'q0'
                    try:
                        self.update_dfa(machine, pre_state, target_state, s + char)
                    except:
                        pass
                        # machine.update_dfa(pre_state, char, Trans(n, n, next_state, opt, opt_num))
                # for t in self.S:
                #     if len(s) == len(t) - 1 and s == t[0:-1]:
                #
                #         target_state = ''.join(map(str, self.row(t)))
                #         if t in updated_list:
                #             continue
                #         updated_list.append(t)
                #         if pre_state == '0':
                #             pre_state = 'q0'
                #         if target_state == '0':
                #             target_state = 'q0'
                #         self.update_dfa(machine, pre_state, target_state, t)

            # dfa = self.generate_dfa(self.T_str, "q0", Machine(self.alphabet, try_dfa), "", 0)
            print("等价查询中")
            result = self.mat.equiv_query(machine)

            if result[0] == 1:
                print("CORRECT DFA LEARNED")
                print("STUDENT DFA")
                print(machine)
                print("TEACHER DFA")
                print(self.mat.dfa)
                break
            else:
                for x in range(len(result[1])):
                    self.S.append(result[1][x:])
                    self.T.append(self.row(result[1][x:]))


# test case dfas

alphabet1 = ["a", "b"]

mat1 = Machine(alphabet1,
               {
                   "q0": {
                       "a": [Trans(0, varMax, "q1", "#", 0)],
                       "b": [Trans(0, varMax, "q1", "#", 0)]},
                   "q1": {
                       "a": [Trans(0, 1, "q1", "+", 1), Trans(2, varMax, "q2", "#", 0)],
                       "b": [Trans(0, varMax, "q1", "#", 0)]},
                   "q2": {
                       "a": [Trans(0, varMax, "q2", "#", 0)],
                       "b": [Trans(0, varMax, "q1", "=", 0)]},
                   "f": ["q2"]
                })

mat2 = Machine(alphabet1,
               {"q0": {"a": "q1", "b": "q1"},
                "q1": {"a": "q2", "b": "q2"},
                "q2": {"a": "q3", "b": "q3"},
                "q3": {"a": "q3", "b": "q4"},
                "q4": {"a": "q1", "b": "q2"},
                "f": ["q3"]}
               )

dfa1 = {"q0": {"a": "q0", "b": "q0"},
        "f": []}

# execution

print("LEARNER\t\t\t\t\t\t\t\t\tTEACHER")
print("~~~~~~~\t\t\t\t\t\t\t\t\t~~~~~~~")

print("Test 1")
test = Learner(alphabet1, mat1)
test.learn_dfa()

# print("Test 2")
# test = Learner(alphabet1, mat2)
# test.learn_dfa()
