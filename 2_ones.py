import numpy as np

if __name__ == '__main__':
    M = 8
    N = 9
    matrix = np.random.randint(0, 2, size=(M, N))
    print(matrix)

    aux_col = np.zeros((M, N), dtype=int)
    for i in range(N):
        aux_col[-1, i] = matrix[-1, i]
        for j in range(M - 2, -1, -1):
            aux_col[j, i] = aux_col[j + 1, i] * matrix[j, i] + matrix[j, i]
    aux_row = np.zeros((M, N), dtype=int)
    for i in range(M):
        aux_row[i, 0] = matrix[i, 0]
        for j in range(1, N):
            aux_row[i, j] = aux_row[i, j - 1] * matrix[i, j] + matrix[i, j]

    max_rect = {'Area': 0, 'Top': (0, 0), 'Bottom': (0, 0)}  # area, right top corner, left bottom corner

    for (row, col), x in np.ndenumerate(matrix):
        if x != 0:
            for i in range(aux_row[row, col]):
                height = min(aux_col[row, (col - i):(col + 1)])
                area = (i + 1) * height
                if area > max_rect['Area']:
                    max_rect['Area'] = area
                    max_rect['Top'] = (row, col)
                    max_rect['Bottom'] = (row + height - 1, col - i)
    print('Maximal area = ', max_rect['Area'])
    print('Top right corner: ', max_rect['Top'])
    print('Bottom left corner: ', max_rect['Bottom'])
