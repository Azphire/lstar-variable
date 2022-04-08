import json
import random
import time
from typing import Tuple

from algorithm_v1.automaton import Machine, Trans

VarMax = 3
LenMax = 20

Alphabet = ['a', 'b']
StateNumber = 3
TransNumber = 10


class TransEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Trans):
            return {
                "l": obj.left,
                "r": obj.right,
                "target": obj.target,
                "opt": obj.operator,
                "num": obj.opt_number
            }
        else:
            return super(TransEncoder, self).default(obj)


def store_machine(machine: Machine, file_name: str):
    store = {
        "alphabet": machine.alphabet,
        "states": machine.states,
        "dfa": machine.dfa,
        "accepted": machine.accepted,
        "start": machine.start
    }
    with open(file_name, 'w', encoding='utf8') as fp:
        json.dump(store, fp, cls=TransEncoder)


def random_dfa(alphabet: list, state_number: int) -> Tuple[Machine, str]:
    states = [i + 1 for i in range(state_number)]
    dfa_map = {}
    for i in states:
        dfa_map[i] = {}
        for char in alphabet:
            trans_list = []
            left = 0
            right = 0
            while True:
                # right += random.randint(0, VarMax - right)
                target = random.choice(states)
                if right >= VarMax or random.randint(0, 2) == 0:
                    trans_list.append(Trans(left, right, target, "=", random.randint(0, VarMax)))
                else:
                    trans_list.append(Trans(left, right, target, "#", 0))
                if right >= VarMax:
                    break
                # left = right + 1
                # right = left
                left += 1
                right += 1
            dfa_map[i][char] = trans_list
    print(dfa_map)
    store = {
        "alphabet": alphabet,
        "states": states,
        "dfa": dfa_map
    }
    file_name = './dfa/' + time.strftime("%Y%m%d%H%M%S", time.localtime())
    with open(file_name + '.json', 'w', encoding='utf8') as fp:
        json.dump(store, fp, cls=TransEncoder)
    machine = Machine(alphabet, states, dfa_map, 1, [2])
    return machine, file_name


def fetch_dfa(file: str) -> Machine:
    with open(file, 'r', encoding='utf8') as fp:
        data = json.load(fp)
    alphabet = data["alphabet"]
    states = data["states"]
    dfa_json = data["dfa"]
    dfa_map = {}
    for i in states:
        dfa_map[i] = {}
        for char in alphabet:
            dfa_map[i][char] = []
            for trans in dfa_json[str(i)][char]:
                dfa_map[i][char].append(Trans(trans["l"], trans["r"], trans["target"], trans["opt"], trans["num"]))
    machine = Machine(alphabet, states, dfa_map, 1, [2])
    return machine


if __name__ == "__main__":
    m1, fn = random_dfa(Alphabet, StateNumber)
    m2 = fetch_dfa(fn+'.json')
    store_machine(m1, fn+'test.json')
