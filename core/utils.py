import string


def calc_tokens(s, min_len=0):
    for char in string.punctuation:
        s = s.replace(char, ' ')

    s = s.replace('…', ' ')

    words = s.split()
    words.sort(key=len, reverse=True)
    return [x for x in words if len(x) >= min_len]


def damerau_levenshtein_distance(s1, s2):
    d = {}
    s1_len = len(s1)
    s2_len = len(s2)
    for i in range(-1, s1_len + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, s2_len + 1):
        d[(-1, j)] = j + 1
    for i in range(s1_len):
        for j in range(s2_len):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
    return d[s1_len - 1, s2_len - 1]
