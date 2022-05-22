import json
import random
import time
import math
from typing import Tuple

from algorithm_multi.automaton import Machine, Trans
from algorithm_multi.learner import varMax


class TransEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Trans):
            return {
                "guards": obj.guards,
                "target": obj.target,
                "assignments": obj.assignments
            }
        else:
            return super(TransEncoder, self).default(obj)


def store_machine(machine: Machine, time_using, file_name: str):
    store = {
        "alphabet": machine.alphabet,
        "states": machine.states,
        "dfa": machine.dfa,
        "accepted": machine.accepted,
        "start_state": machine.start_state,
        "init_params": machine.init_params,
        "time": time_using
    }
    with open(file_name, 'w', encoding='utf8') as fp:
        json.dump(store, fp, cls=TransEncoder)


def random_dfa(alphabet: list, state_number: int, param_num: int) -> Tuple[Machine, str]:
    states = [i + 1 for i in range(state_number)]
    dfa_map = {}
    init_p_list = []
    for i in range(param_num):
        init_p_list.append(random.randint(0, varMax))
    param_values = []
    for p1 in range(varMax):
        for p2 in range(varMax):
            if param_num < 2:
                break
            for p3 in range(varMax):
                if param_num < 3:
                    break
                for p4 in range(varMax):
                    if param_num < 4:
                        break
                    for p5 in range(varMax):
                        if param_num < 5:
                            break
                        for p6 in range(varMax):
                            if param_num < 6:
                                break
                            param_values.append((p1, p2, p3, p4, p5, p6))
                        if param_num == 5:
                            param_values.append((p1, p2, p3, p4, p5))
                    if param_num == 4:
                        param_values.append((p1, p2, p3, p4))
                if param_num == 3:
                    param_values.append((p1, p2, p3))
            if param_num == 2:
                param_values.append((p1, p2))
        if param_num == 1:
            param_values.append((p1))
    init_params = tuple(init_p_list)

    for i in states:
        dfa_map[i] = {}
        for char in alphabet:
            trans_list = []
            for guard in param_values:
                # if random.randint(0, 3) == 0:
                #     trans_list.append(Trans(guard, i, guard))
                # else:
                    target = random.choice(states)
                    assignment = random.choice(param_values)
                    trans_list.append(Trans(guard, target, assignment))

            dfa_map[i][char] = trans_list
    print(dfa_map)
    store = {
        "alphabet": alphabet,
        "states": states,
        "dfa": dfa_map,
        "start_state": 1,
        "init_params": init_params
    }
    file_name = './dfa/' + time.strftime("%Y%m%d%H%M%S", time.localtime())
    with open(file_name + '.json', 'w', encoding='utf8') as fp:
        json.dump(store, fp, cls=TransEncoder)
    machine = Machine(alphabet, states, dfa_map, 1, init_params, [2])
    return machine, file_name


def fetch_dfa(file: str) -> Machine:
    with open(file, 'r', encoding='utf8') as fp:
        data = json.load(fp)
    alphabet = data["alphabet"]
    states = data["states"]
    init_params = data["init_params"]
    dfa_json = data["dfa"]
    dfa_map = {}
    for i in states:
        dfa_map[i] = {}
        for char in alphabet:
            dfa_map[i][char] = []
            for trans in dfa_json[str(i)][char]:
                dfa_map[i][char].append(Trans(tuple(trans["guards"]), trans["target"], tuple(trans["assignments"])))
    machine = Machine(alphabet, states, dfa_map, 1, init_params, [2])
    return machine


if __name__ == "__main__":
    m1, fn = random_dfa(["a", "b"], 3, 2)
    m2 = fetch_dfa(fn+'.json')
    store_machine(m1, fn+'test.json')
