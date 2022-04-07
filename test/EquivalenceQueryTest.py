from algorithm_v1.equivalenceQuery import EquivalenceQuery
from test.randomDFA import fetch_dfa, store_machine

if __name__ == '__main__':

    fn1 = './dfa/20220318222429.json'
    fn2 = '20220318222429test.json'
    m = fetch_dfa(fn1)
    h = fetch_dfa(fn2)
    eq = EquivalenceQuery(m, h)
    print(eq.query())

