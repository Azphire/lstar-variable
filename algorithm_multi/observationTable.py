
def is_same_state(row_1: list, row_2: list):
    for i in range(len(row_1)):
        if row_1[i] != row_2[i]:
            return False
    return True


def no_conflict(row_1: list, row_2: list):
    if row_1[0][0] != row_2[0][0]:
        return False
    if row_1[0][1] != row_2[0][1]:
        return True
    for i in range(len(row_1)):
        if row_1[i] != row_2[i]:
            return False
    return True


class ObservationTable:

    def __init__(self, alphabet: list):
        self.alphabet = alphabet
        self.S = ['']  # ['', 'a']
        self.E = ['']  # ['', 'a', 'ab', 'aa']
        self.T = []  #
        self.R = []
        self.RT = []
        for a in self.alphabet:
            self.S.append(a)