class Trans:

    def __init__(self, left, right, target, operator, opt_number):
        self.left = left
        self.right = right
        self.target = target
        self.operator = operator
        self.opt_number = opt_number

    def __repr__(self):
        result = {
            "l": self.left,
            "r": self.right,
            "target": self.target,
            "opt": self.operator,
            "num": self.opt_number
        }
        return str(result)


class Machine:

    def __init__(self, alphabet: list, states: list, dfa: map, start, accepted: list):
        self.alphabet = alphabet
        self.states = states
        self.dfa = dfa
        self.start = start
        self.accepted = accepted

    # update传入的Trans左右区间为同一个数
    def update_once(self, state, char, new_trans: Trans):
        # print("update dfa: ", state, char, new_trans)
        trans_region = new_trans.left
        covered = False
        for trans in self.dfa[state][char]:

            if trans.left <= trans_region <= trans.right:
                if trans.target != new_trans.target or \
                        trans.operator != new_trans.operator or \
                        trans.opt_number != new_trans.opt_number:
                    print('转换冲突！')
                    return 0

            if trans.target == new_trans.target and \
                    trans.operator == new_trans.operator and \
                    trans.opt_number == new_trans.opt_number:

                if trans.left == trans_region + 1:
                    left_trans = Trans(trans.left - 1, trans.right, trans.target, trans.operator, trans.opt_number)
                    self.dfa[state][char].remove(trans)
                    self.dfa[state][char].append(left_trans)
                    covered = True

                if trans.right == trans_region - 1:
                    right_trans = Trans(trans.left, trans.right + 1, trans.target, trans.operator, trans.opt_number)
                    self.dfa[state][char].remove(trans)
                    self.dfa[state][char].append(right_trans)
                    covered = True

        if not covered:
            self.dfa[state][char].append(new_trans)

    def transfer(self, state, char, n):
        selected_trans = None
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
        return state, n, '#', 0

    def member_query(self, test_str):
        if test_str == "":
            return 0, 0
        curr_state = self.start
        n = 0
        for char in test_str:
            result = self.transfer(curr_state, char, n)
            if result:
                curr_state, n, opt, opt_num = result
            else:
                return False

        if curr_state in self.accepted:
            # print(test_str, " 被接收")
            return 1, n
        else:
            # print(test_str, " 被拒绝")
            return 0, n

    def full_query(self, sentence):
        curr_state = self.start
        n = 0
        result = None
        for char in sentence:
            curr_state, next_n, opt, opt_num = self.transfer(curr_state, char, n)
            result = (n, opt, opt_num)
            n = next_n
        return result
