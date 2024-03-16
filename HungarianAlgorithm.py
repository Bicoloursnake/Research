import copy

from MatrixSupplements import maximum_matching, matrix_addition, scalar_multiplication, matrix_xor


def maximum_weight_matching(matrix: list[list[int]]) -> list[list[int]]:
    """A function implementing the Hungarian algorithm for integer matrices"""
    "TODO: calculate the epsilon value instead of assuming it's 1"
    mutable_matrix: list[list[int]] = copy.deepcopy(matrix)
    equality_matrix: list[list[int]] = copy.deepcopy(matrix)
    row_headers: list = []
    col_headers: list = []
    for row in matrix:
        max_row_entry: int = 0
        for i in range(len(row)):
            if row[i] > max_row_entry:
                max_row_entry = row[i]
        row_headers.append(max_row_entry)
        col_headers.append(0)
    repetitions: int = 0
    while True:
        adjusted_rows: list[int] = []
        adjusted_cols: list[int] = []
        for i in range(len(mutable_matrix)):
            for j in range(len(mutable_matrix[i])):
                mutable_matrix[i][j] = row_headers[i] + col_headers[j] - matrix[i][j]
                if mutable_matrix[i][j] == 0:
                    equality_matrix[i][j] = 1
                else:
                    equality_matrix[i][j] = 0
        match_matrix: list[list[int]] = maximum_matching(equality_matrix)
        leftover_matrix: list[list[int]] = matrix_xor(equality_matrix, match_matrix)
        match_count: int = 0
        for i in range(len(leftover_matrix)):
            for j in range(len(leftover_matrix[i])):
                if leftover_matrix[i][j] == 1:
                    col_headers[j] += 1
                    adjusted_cols.append(j)
                    row_headers[i] -= 1
                    adjusted_rows.append(i)
                    break
        for j in adjusted_cols:
            for i in range(len(match_matrix)):
                if match_matrix[i][j] == 1 and i not in adjusted_rows:
                    row_headers[i] -= 1
                    adjusted_rows.append(i)
                    break
        for i in range(len(match_matrix)):
            for j in range(len(match_matrix[i])):
                if match_matrix[i][j] == 1:
                    match_count += 1
        if match_count == len(match_matrix):
            return match_matrix

