import copy
from typing import Tuple

from algorithm_multi.automaton import Machine, Trans

varMax = 5


class EquivalenceQuery:

    def __init__(self, m: Machine, h: Machine):
        self.m = m
        self.h = h
        self.alphabet = m.alphabet
        self.reversed_m = copy.deepcopy(self.m)
        self.reversed_m.accepted = [i for i in self.m.states if i not in self.m.accepted]
        self.reversed_h = copy.deepcopy(self.h)
        self.reversed_h.accepted = [i for i in self.h.states if i not in self.h.accepted]
        self.counter_example = ''

    def sync_product(self, m1: Machine, m2: Machine) -> Machine:
        states = []
        accepted = []
        dfa = {}
        for state1 in m1.states:
            for state2 in m2.states:
                # states数组的下标是平行连接后的state值
                states.append((state1, state2))
                if state1 in m1.accepted and state2 in m2.accepted:
                    accepted.append((state1, state2))
        start = (m1.start_state, m2.start_state)

        prod_m = Machine(self.alphabet, states, dfa, start, (), accepted)
        return prod_m

    def find_counter_example(self, prod_m: Machine, m1: Machine, m2: Machine,
                             state: Tuple, pre: str, v1: tuple, v2: tuple, visited: list) -> bool:
        if state in prod_m.accepted:
            self.counter_example = pre
            return True
        if (state, v1, v2) in visited:
            return False
        visited.append((state, v1, v2))
        for char in self.alphabet:
            result1 = m1.transfer(state[0], char, v1)
            if not result1:
                continue
            target1, cur_n1 = result1
            result2 = m2.transfer(state[1], char, v2)
            if not result2:
                continue
            target2, cur_n2 = result2
            if self.find_counter_example(prod_m, m1, m2, (target1, target2), pre + char, cur_n1, cur_n2, visited):
                return True
        return False

    def query(self) -> Tuple[bool, str]:
        # m和reversed_h平行连接
        prod_1 = self.sync_product(self.m, self.reversed_h)
        if self.find_counter_example(prod_1, self.m, self.reversed_h, prod_1.start_state, '',
                                     self.m.init_params, self.reversed_h.init_params, []):
            return False, self.counter_example
        # h和reversed_m平行连接
        prod_2 = self.sync_product(self.h, self.reversed_m)
        if self.find_counter_example(prod_2, self.h, self.reversed_m, prod_2.start_state, '',
                                     self.h.init_params, self.reversed_m.init_params, []):
            return False, self.counter_example
        return True, ''
