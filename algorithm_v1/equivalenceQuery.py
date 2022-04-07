import copy
from typing import Tuple

from algorithm_v1.automaton import Machine, Trans
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
                state = states.index((state1, state2))
                if state1 in m1.accepted and state2 in m2.accepted:
                    accepted.append(state)
                arcs = {}
                for a in self.alphabet:
                    arcs[a] = []
                dfa[state] = arcs
        start = states.index((m1.start, m2.start))

        prod_m = Machine(self.alphabet, [i for i in range(len(states))], dfa, start, accepted)

        for state1 in m1.states:
            for state2 in m2.states:
                state = states.index((state1, state2))
                for char in self.alphabet:
                    for n in range(varMax):
                        result1 = m1.transfer(state1, char, n)
                        if not result1:
                            continue
                        target1, cur_n1, operator1, opt_number1 = result1
                        result2 = m2.transfer(state2, char, n)
                        if not result2:
                            continue
                        target2, cur_n2, operator2, opt_number2 = result2
                        if cur_n1 == cur_n2:
                            target = states.index((target1, target2))
                            new_trans = Trans(n, n, target, operator1, opt_number1)
                            prod_m.update_once(state, char, new_trans)
        return prod_m

    def find_counter_example(self, machine: Machine, state, pre: str, variable: int, visited: list) -> bool:
        if state in machine.accepted:
            self.counter_example = pre
            return True
        if (state, variable) in visited:
            return False
        visited.append((state, variable))
        for char in self.alphabet:
            result = machine.transfer(state, char, variable)
            if not result:
                continue
            target, cur_n, operator, opt_number = result
            if self.find_counter_example(machine, target, pre + char, cur_n, visited):
                return True
        return False

    def query(self) -> Tuple[bool, str]:
        # m和reversed_h平行连接
        prod_1 = self.sync_product(self.m, self.reversed_h)
        if self.find_counter_example(prod_1, prod_1.start, '', 0, []):
            return False, self.counter_example
        prod_2 = self.sync_product(self.h, self.reversed_m)
        if self.find_counter_example(prod_2, prod_2.start, '', 0, []):
            return False, self.counter_example
        return True, ''

