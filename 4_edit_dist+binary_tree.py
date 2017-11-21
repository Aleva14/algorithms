gap_pen = 0.5
scoring_matrix = {'A': {'A': -1, 'T': -0.5, 'G': -0.1, 'C': -0.1},
                  'T': {'A': -0.5, 'T': -1, 'G': -0.1, 'C': -0.1},
                  'G': {'A': -0.1, 'T': -0.1, 'G': -1, 'C': -0.5},
                  'C': {'A': -0.1, 'T': -0.1, 'G': -0.5, 'C': -1}}


def edit_distance(line1, line2):
    edit_graph = []
    back_track = []
    for rown in range(0, len(line2) + 1):
        edit_graph.append([])
        back_track.append([])
        for coln in range(0, len(line1) + 1):
            tmp = dist(edit_graph, rown, coln, line1, line2)
            edit_graph[rown].append(tmp[0])
            back_track[rown].append(tmp[1])
    # print(back_track)
    aligned_lines = align(back_track, line1, line2)
    return(-edit_graph[-1][-1], *aligned_lines)


def dist(e_g, i, j, line1, line2):
    global scoring_matrix
    global gap_pen

    if i == 0 and j == 0:
        return [0, 0]
    if i == 0:
        return [e_g[i][j - 1] + gap_pen, 1]
    if j == 0:
        return [e_g[i - 1][j] + gap_pen, 0]
    down = e_g[i - 1][j] + gap_pen
    right = e_g[i][j - 1] + gap_pen
    dr = e_g[i - 1][j - 1] + scoring_matrix[line1[j - 1]][line2[i - 1]]
    m = min(down, right, dr)
    if down == m:
        return [m, 0]  # 0 is for "moved down"
    if right == m:
        return [m, 1]  # 1 is for "moved right"
    return [m, 2]  # 2 is for "moved right and down"


def align(b_t, line1, line2):
    line1_aligned = ''
    line2_aligned = ''
    rown = len(line2)
    coln = len(line1)
    while rown > 0 or coln > 0:
        if b_t[rown][coln] == 0:
            line1_aligned = ''.join(('-', line1_aligned))
            line2_aligned = ''.join((line2[rown - 1], line2_aligned))
            rown -= 1
        elif b_t[rown][coln] == 1:
            line1_aligned = ''.join((line1[coln - 1], line1_aligned))
            line2_aligned = ''.join(('-', line2_aligned))
            coln -= 1
        else:
            line1_aligned = ''.join((line1[coln - 1], line1_aligned))
            if line1[coln - 1] == line2[rown - 1]:
                line2_aligned = ''.join((line2[rown - 1], line2_aligned))
            else:
                line2_aligned = ''.join((line2[rown - 1].lower(), line2_aligned))
            rown -= 1
            coln -= 1
    return (line1_aligned, line2_aligned)


class Node:

    def __init__(self, data, line1, line2, name):
        self.left = None
        self.right = None
        self.data = data
        self.line1 = line1
        self.line2 = line2
        self.name = name

    def insert(self, data, line1, line2, name):
        if self.data:
            if data <= self.data:
                if self.left is None:
                    self.left = Node(data, line1, line2, name)
                else:
                    self.left.insert(data, line1, line2, name)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data, line1, line2, name)
                else:
                    self.right.insert(data, line1, line2, name)
        else:
            self.data = data
            self.line1 = line1
            self.line2 = line2
            self.name = name

    def print_tree(self):
        if self.left:
            self.left.print_tree()
        print(self.name)
        print(self.data)
        print(self.line1)
        print(self.line2)
        if self.right:
            self.right.print_tree()


if __name__ == "__main__":
    data = open("test4.txt", 'r')
    data = data.readlines()
    reference = data[0].strip()
    lines = {}
    for line in data[1:]:
        line = line.strip()
        if line.startswith(">"):
            lines[line[1:]] = ''
            cur_str = line[1:]
        else:
            lines[cur_str] += line

    root = None
    for name, line in lines.items():
        if root:
            # print(name, *edit_distance(reference, line))
            root.insert(*edit_distance(reference, line), name)
        else:
            root = Node(*edit_distance(reference, line), name)
    root.print_tree()
