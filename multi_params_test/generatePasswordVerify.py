import json
from typing import Tuple

from algorithm_multi.automaton import Machine, Trans


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


def generatePasswordVerify() -> Tuple[Machine, str]:
    alphabet = ["A", "B"]
    state_number = 6
    varMax = 2
    states = [i + 1 for i in range(state_number)]
    dfa_map = {}
    param_values = []
    for p1 in range(varMax):
        for p2 in range(varMax):
            for p3 in range(varMax):
                for p4 in range(varMax):
                    for p5 in range(varMax):
                        param_values.append((p1, p2, p3, p4, p5))

    init_params = (0, 0, 0, 0, 0)

    # 状态1
    dfa_map[1] = {"A": [], "B": []}
    for t in param_values:
        if t[0] == 0:
            target = list(t)
            target[1] = 0
            dfa_map[1]["A"].append(Trans(t, 2, tuple(target)))
            target[1] = 1
            dfa_map[1]["B"].append(Trans(t, 2, tuple(target)))
        if t[0] == 1:
            if t[1] == 0:
                dfa_map[1]["A"].append(Trans(t, 2, t))
                dfa_map[1]["B"].append(Trans(t, 6, t))
            if t[1] == 1:
                dfa_map[1]["A"].append(Trans(t, 6, t))
                dfa_map[1]["B"].append(Trans(t, 2, t))

    # 状态2
    dfa_map[2] = {"A": [], "B": []}
    for t in param_values:
        if t[0] == 0:
            target = list(t)
            target[2] = 0
            dfa_map[2]["A"].append(Trans(t, 3, tuple(target)))
            target[2] = 1
            dfa_map[2]["B"].append(Trans(t, 3, tuple(target)))
        if t[0] == 1:
            if t[2] == 0:
                dfa_map[2]["A"].append(Trans(t, 3, t))
                dfa_map[2]["B"].append(Trans(t, 6, t))
            if t[2] == 1:
                dfa_map[2]["A"].append(Trans(t, 6, t))
                dfa_map[2]["B"].append(Trans(t, 3, t))

    # 状态3
    dfa_map[3] = {"A": [], "B": []}
    for t in param_values:
        if t[0] == 0:
            target = list(t)
            target[3] = 0
            dfa_map[3]["A"].append(Trans(t, 4, tuple(target)))
            target[3] = 1
            dfa_map[3]["B"].append(Trans(t, 4, tuple(target)))
        if t[0] == 1:
            if t[3] == 0:
                dfa_map[3]["A"].append(Trans(t, 4, t))
                dfa_map[3]["B"].append(Trans(t, 6, t))
            if t[3] == 1:
                dfa_map[3]["A"].append(Trans(t, 6, t))
                dfa_map[3]["B"].append(Trans(t, 4, t))

    # 状态4
    dfa_map[4] = {"A": [], "B": []}
    for t in param_values:
        if t[0] == 0:
            target = list(t)
            target[0] = 1
            target[4] = 0
            dfa_map[4]["A"].append(Trans(t, 1, tuple(target)))
            target[4] = 1
            dfa_map[4]["B"].append(Trans(t, 1, tuple(target)))
        if t[0] == 1:
            if t[4] == 0:
                dfa_map[4]["A"].append(Trans(t, 5, t))
                dfa_map[4]["B"].append(Trans(t, 6, t))
            if t[4] == 1:
                dfa_map[4]["A"].append(Trans(t, 6, t))
                dfa_map[4]["B"].append(Trans(t, 5, t))

    # 状态5
    dfa_map[5] = {"A": [], "B": []}
    for t in param_values:
        dfa_map[5]["A"].append(Trans(t, 5, t))
        dfa_map[5]["B"].append(Trans(t, 5, t))

    # 状态6
    dfa_map[6] = {"A": [], "B": []}
    for t in param_values:
        dfa_map[6]["A"].append(Trans(t, 6, t))
        dfa_map[6]["B"].append(Trans(t, 6, t))

    store = {
        "alphabet": alphabet,
        "states": states,
        "dfa": dfa_map,
        "start_state": 1,
        "init_params": init_params
    }
    file_name = './dfa/' + "PasswordVerify"
    with open(file_name + '.json', 'w', encoding='utf8') as fp:
        json.dump(store, fp, cls=TransEncoder)
    machine = Machine(alphabet, states, dfa_map, 1, init_params, [5])
    return machine, file_name


if __name__ == "__main__":
    generatePasswordVerify()
