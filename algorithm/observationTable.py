def is_same_state(row_1: list, row_2: list):
    for i in range(len(row_1)):
        if row_1[i][1] == row_2[i][1] and row_1[i][0] != row_2[i][0]:
            return False
    return True


class ObservationTable:

    def __init__(self, alphabet: list):
        self.alphabet = alphabet
        self.S = ['']  # ['', 'a']
        self.E = ['']  # ['', 'a', 'ab', 'aa']
        self.T = []  #
