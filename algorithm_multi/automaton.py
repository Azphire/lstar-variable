class Trans:

    def __init__(self, guards: tuple, target, assignments: tuple):
        self.target = target
        self.guards = guards
        self.assignments = assignments

    def __repr__(self):
        result = {
            "target": self.target,
            "guards": self.guards,
            "assignments": self.assignments
        }
        return str(result)


class Machine:

    def __init__(self, alphabet: list, states: list, dfa: map, start_state, init_params: tuple, accepted: list):
        self.alphabet = alphabet
        self.states = states
        self.dfa = dfa
        self.start_state = start_state
        self.init_params = init_params
        self.accepted = accepted

    # update传入的Trans左右区间为同一个数
    def update_once(self, state, char, new_trans: Trans):
        # print("update dfa: ", state, char, new_trans)
        for trans in self.dfa[state][char]:
            if trans.guards == new_trans.guards:
                if trans.target != new_trans.target or \
                        trans.assignments != new_trans.assignments:
                    print('转换冲突！')
                    return 0
                if trans.target == new_trans.target and \
                        trans.assignments == new_trans.assignments:
                    # 重复，不必添加
                    return 0
        self.dfa[state][char].append(new_trans)

    def transfer(self, state, char, params: tuple):
        # 挑选输入字母对应的Tran
        for trans in (self.dfa[state][char]):
            # 条件判断
            if trans.guards == params:
                return trans.target, trans.assignments
        return state, params

    def member_query(self, test_str):
        if test_str == "":
            return 0, self.init_params
        curr_state = self.start_state
        params = self.init_params
        for char in test_str:
            result = self.transfer(curr_state, char, params)
            if result:
                curr_state, params = result
            else:
                return False

        if curr_state in self.accepted:
            # print(test_str, " 被接收")
            return 1, params
        else:
            # print(test_str, " 被拒绝")
            return 0, params

