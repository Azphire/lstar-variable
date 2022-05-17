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
    trans_max = pow(varMax, param_num)
    init_p_list = []
    for i in range(param_num):
        init_p_list.append(random.randint(0, varMax))
    init_params = tuple(init_p_list)
    pre_params = init_params
    for i in states:
        dfa_map[i] = {}
        for char in alphabet:
            trans_list = []
            for n in range(trans_max):
                p_list = []
                for p in range(param_num):
                    p_list.append(random.randint(0, varMax))
                params = tuple(p_list)
                if random.randint(0, 10) == 0:
                    trans_list.append(Trans(pre_params, 2, params))
                if random.randint(0, 2) == 0:
                    target = random.choice(states)
                    trans_list.append(Trans(pre_params, target, params))
                else:
                    trans_list.append(Trans(pre_params, i, params))
                pre_params = params
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
