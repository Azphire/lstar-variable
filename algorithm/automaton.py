class Trans:

    def __init__(self, left, right, target, operator, opt_number):
        self.left = left
        self.right = right
        self.target = target
        self.operator = operator
        self.opt_number = opt_number


class Machine:

    def __init__(self, alphabet: list, states: list, dfa: map, start, accepted: list):
        self.alphabet = alphabet
        self.states = states
        self.dfa = dfa
        self.start = start
        self.accepted = accepted

    # update传入的Trans左右区间为同一个数
    def update_once(self, state, char, new_trans: Trans):
        print("update dfa: ", state, char, new_trans)
        trans_region = new_trans.left
        for trans in self.dfa[state][char]:
            # 发现重叠的情况
            if trans.left <= trans_region <= trans.right:
                # 转换相同
                if trans.target == new_trans.target and \
                        trans.operator == new_trans.operator and \
                        trans.opt_number == new_trans.opt_number:
                    return 0
                right_trans = Trans(new_trans.right + 1, trans.right, trans.target, trans.operator, trans.opt_number)
                left_trans = Trans(trans.left, new_trans.left - 1, trans.target, trans.operator, trans.opt_number)
                self.dfa[state][char].remove(trans)
                if right_trans.left <= right_trans.right:
                    self.dfa[state][char].append(right_trans)
                if left_trans.left <= left_trans.right:
                    self.dfa[state][char].append(left_trans)
                break
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
        return None

    def member_query(self, test_str):
        curr_state = self.start
        n = 0
        opt = ''
        opt_num = 0
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
            curr_state, n, opt, opt_num = self.transfer(curr_state, char, n)
            result = (n, opt, opt_num)
        return result