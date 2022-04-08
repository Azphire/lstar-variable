from algorithm_v1.equivalenceQuery import EquivalenceQuery
from algorithm_v1.automaton import Machine, Trans
from test.randomDFA import fetch_dfa, store_machine
varMax = 3

alphabet_1 = ["a", "b"]
states_1 = [1, 2]
dfa_1 = {
    1: {
        "a": [Trans(0, 0, 1, "+", 1), Trans(1, varMax, 2, "+", 1)],
        "b": [Trans(0, varMax, 1, "#", 0)]},
    2: {
        "a": [Trans(0, varMax, 2, "#", 0)],
        "b": [Trans(0, varMax, 2, "#", 0)]}
}
machine_1 = Machine(alphabet_1, states_1, dfa_1, 1, [2])

alphabet_3 = ["a", "b"]
states_3 = [1, 2, 3, 4]
dfa_3 = {
    1: {
        "a": [Trans(0, 2, 1, "+", 1), Trans(3, varMax, 3, "#", 0)],
        "b": [Trans(0, varMax, 2, "#", 0)]},
    2: {
        "a": [Trans(0, varMax, 4, "#", 0)],
        "b": [Trans(0, 2, 1, "+", 1), Trans(3, varMax, 3, "#", 0)]},
    3: {
        "a": [Trans(0, varMax, 3, "#", 0)],
        "b": [Trans(0, varMax, 3, "#", 0)]},
    4: {
        "a": [Trans(0, varMax, 3, "#", 0)],
        "b": [Trans(0, varMax, 3, "#", 0)]}
}
machine_3 = Machine(alphabet_3, states_3, dfa_3, 1, [4])

if __name__ == '__main__':

    fn1 = './dfa/20220323094641.json'
    fn2 = './dfa/20220323094641learn.json'
    m = fetch_dfa(fn1)
    h = fetch_dfa(fn2)
    eq = EquivalenceQuery(m, h)
    print(eq.query())

