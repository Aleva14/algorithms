class Heap:
    def __init__(self, A):
        self.list = A
        self.size = len(A)

    def sift_up(self, i):
        par = ((i + 1) // 2) - 1

        while (self.list[i] > self.list[par]) and par >= 0:
            self.list[i], self.list[par] = self.list[par], self.list[i]
            i = par
            par = ((i + 1) // 2) - 1

    def extract_max(self):
        heap_max = self.list[0]
        if len(self.list) == 1:
            self.list.pop()
        else:
            self.list[0] = self.list.pop()
        if self.list:
            self.sift_down(0)
        return heap_max

    def sift_down(self, i, size):
        lchild = 2 * (i + 1) - 1
        rchild = 2 * (i + 1)
        if rchild < size:
            m = max(self.list[i], self.list[lchild], self.list[rchild])
            if m == self.list[lchild]:
                self.list[i], self.list[lchild] = self.list[lchild], self.list[i]
                self.sift_down(lchild, size)
            elif m == self.list[rchild]:
                self.list[i], self.list[rchild] = self.list[rchild], self.list[i]
                self.sift_down(rchild, size)
        elif lchild < size:
            if self.list[lchild] > self.list[i]:
                self.list[i], self.list[lchild] = self.list[lchild], self.list[i]
                self.sift_down(lchild, size)

    def sort(self):
        size = self.size - 1
        for i in range((self.size // 2), -1, -1):
            self.sift_down(i, self.size)
        for i in range(self.size - 1, 0, -1):
            self.list[0], self.list[size] = self.list[size], self.list[0]
            self.sift_down(0, size)
            size -= 1

    def __str__(self):
        return '\n'.join(map(str, self.list[0:]))


if __name__ == '__main__':
    data = open("test1.txt", 'r')
    lines = {}
    for line in data:
        line = line.strip()
        if line.startswith(">"):
            lines[line[1:]] = ''
            cur_str = line[1:]
        else:
            lines[cur_str] += line

    h = Heap(list(lines.values()))
    h.sort()
    print(h)
