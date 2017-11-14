def findSubstrs(reference, substrs):
    # p should be prime and larger than max code of symbol
    p = 117
    # save all necessary powers of p
    pw = [p ** i for i in range(len(reference))]
    # all + and * are mod 2^64 not to use long arithmetics
    b = 2 ** 64

    # calculate hashes of all perfixes of reference
    ref_hash = [0] * len(reference)

    ref_hash[0] = ord(reference[0]) % b
    for i in range(1, len(reference)):
        ref_hash[i] = (ref_hash[i - 1] + pw[i] * ord(reference[i])) % b
        result = {}
        collisions = {}
    for i in substrs.keys():
        result[i], collisions[i] = findSubstr(ref_hash, substrs[i], pw, b, reference)
        print(">", i)
        print(substrs[i])
        print("Positions: ", " ".join(list(map(str, result[i]))))
        print("Collisions: ", collisions[i])


# calculate hash of substring from L to R,
# h - hashes of prefixes
def getHash(h, L, R, b):
        if L == 0:
            return h[R]
        else:
            return (h[R] - h[L - 1]) % b


def findSubstr(ref_hash, substr, pw, b, reference):
    # calculate hash of substr
    substr_hash = sum([(ord(substr[i]) * pw[i]) for i in range(len(substr))]) % b
    m = len(substr)
    result = []
    n_col = 0
    for i in range(0, len(ref_hash) - m):
        if getHash(ref_hash, i, i + m - 1, b)  == substr_hash * pw[i] % b:
            # Check to avoid possible collisions
            if reference[i:i + m] == substr:
                result.append(i)
            else:
                n_col += 1
    return result, n_col


if __name__ == "__main__":
    data = open("test.txt", 'r')
    data = data.readlines()
    reference = data[0].strip()
    substrs = {}
    for line in data[1:]:
        line = line.strip()
        if line.startswith(">"):
            substrs[line[1:]] = ''
            cur_str = line[1:]
        else:
            substrs[cur_str] += line

    findSubstrs(reference, substrs)
