from typing import Tuple, List, Any


def check_row(row: int, main_matrix: list[list[int]], matching_matrix: list[list[int]], path_matrix: list[list[int]],
              pathed_vertices_in_x: list[int], pathed_vertices_in_y: list[int]) \
        -> tuple[list[list[int]], int]:
    """The purpose of this function is to check if there is an edge not in the matching adjacent to vertex i, and if so,
    add that edge to the matching-alternating path. If there is no such edge, then the existing path will never be
    augmenting, and we return a blank matrix to show that no adjustment to the matching is needed, as well as a
    non existent vertex."""
    for j in range(len(main_matrix)):
        if main_matrix[row][j] == 1 and matching_matrix[row][j] == 0 and j not in pathed_vertices_in_y:
            path_matrix[row][j] = 1
            pathed_vertices_in_y.append(j)
            return check_col(j, main_matrix, matching_matrix, path_matrix, pathed_vertices_in_x, pathed_vertices_in_y)
    return [], -1


def check_col(col: int, main_matrix: list[list[int]], matching_matrix: list[list[int]], path_matrix: list[list[int]],
              pathed_vertices_in_x: list[int], pathed_vertices_in_y: list[int]) \
        -> tuple[list[list[int]], int]:
    """The purpose of this function is to check if there is an edge in the matching adjacent to vertex j, and if so,
    add that edge to the matching-alternating path. If there is no such edge, then the existing path is augmenting, and
    we return it to adjust the existing matching, as well as the column that needs marked as saturated."""
    for i in range(len(main_matrix)):
        if matching_matrix[i][col] == 1 and i not in pathed_vertices_in_x:
            path_matrix[i][col] = 1
            pathed_vertices_in_x.append(i)
            return check_row(i, main_matrix, matching_matrix, path_matrix, pathed_vertices_in_x, pathed_vertices_in_y)
    return path_matrix, col


def matrix_addition(matrix1: list[list[int]], matrix2: list[list[int]]) -> list[list[int]]:
    """A function to add two matrices together entry by entry, if the second matrix is smaller than the
    first in either dimension, it will return an empty matrix and print a warning statement"""
    sum_matrix: list[list[int]] = []
    try:
        for i in range(len(matrix1)):
            sum_matrix.append([])
            for j in range(len(matrix1[i])):
                sum_matrix[i].append(matrix1[i][j] + matrix2[i][j])
    except IndexError:
        print("Second matrix too small, returning empty matrix")
        return []
    return sum_matrix


def matrix_xor(matrix1: list[list[int]], matrix2: list[list[int]]) -> list[list[int]]:
    """A function to calculate bitwise xor entry by entry. In the case of binary matrices, this is equivalent to
    addition in the field of two elements or a symmetric difference of sets. If the second matrix is smaller than the
    first in either dimension, it will return an empty matrix and print a warning statement."""
    sum_matrix: list[list[int]] = []
    try:
        for i in range(len(matrix1)):
            sum_matrix.append([])
            for j in range(len(matrix1[i])):
                sum_matrix[i].append(matrix1[i][j] ^ matrix2[i][j])
    except IndexError:
        print("Second matrix too small, returning empty matrix")
        return []
    return sum_matrix


def scalar_multiplication(scalar: int, matrix: list[list[int]]) -> list[list[int]]:
    """A function to multiply a matrix by an integer scalar entry by entry."""
    scalar_matrix: list[list[int]] = []
    for i in range(len(matrix)):
        scalar_matrix.append([])
        for j in range(len(matrix[i])):
            scalar_matrix[i].append(scalar * matrix[i][j])
    return scalar_matrix


def maximum_matching(matrix: list[list[int]]) -> list[list[int]]:
    """A function to calculate a maximum matching in a bipartite graph using an Augmenting Path Algorithm."""
    unmarked_vertices_in_x: list[int] = []
    marked_vertices_in_x: list[int] = []
    unmarked_vertices_in_y: list[int] = []
    matching_matrix: list[list[int]] = matrix_xor(matrix,matrix)
    for i in range(len(matrix)):
        unmarked_vertices_in_x.append(i)
        unmarked_vertices_in_y.append(i)
    for i in unmarked_vertices_in_x:
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0 and i not in marked_vertices_in_x and j in unmarked_vertices_in_y:
                matching_matrix[i][j] = 1
                marked_vertices_in_x.append(i)
                unmarked_vertices_in_y.remove(j)
            elif matrix[i][j] == 0 or i in marked_vertices_in_x:
                matching_matrix[i][j] = 0
            else:
                path_matrix: list[list[int]] = matrix_xor(matrix, matrix)
                path_matrix[i][j] = 1
                y_vertex: int
                path_matrix, y_vertex = check_col(j, matrix, matching_matrix, path_matrix, [i], [j])
                if path_matrix:
                    marked_vertices_in_x.append(i)
                    unmarked_vertices_in_y.remove(y_vertex)
                    matching_matrix = matrix_xor(matching_matrix, path_matrix)
                else:
                    matching_matrix[i][j] = 0
    return matching_matrix
