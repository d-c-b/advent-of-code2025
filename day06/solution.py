from math import prod
from os import path
from typing import Callable, Iterable

FUNCTION_MAP: dict[str, Callable[[Iterable[int]], int]] = {"+": sum, "*": prod}


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        *number_rows, functions_row = input_file.read().strip().splitlines()
        start_indices = [
            i for i, char in enumerate(functions_row) if char in FUNCTION_MAP
        ]
        end_indices = [*[i - 1 for i in start_indices[1:]], None]
        number_matrix = [
            [line[start:end] for start, end, in zip(start_indices, end_indices)]
            for line in number_rows
        ]
        self.functions = [FUNCTION_MAP[operator] for operator in functions_row.split()]
        self.columns: list[list[str]] = [[] for _ in range(len(start_indices))]

        for row in number_matrix:
            for j, num in enumerate(row):
                self.columns[j].append(num)

    def solve_part_1(self) -> int:
        return sum(
            func(map(int, column)) for column, func in zip(self.columns, self.functions)
        )

    def solve_part_2(self) -> int:
        grand_total = 0
        for column, func in zip(reversed(self.columns), reversed(self.functions)):
            grand_total += func([int("".join(digits)) for digits in zip(*column)])

        return grand_total


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 06:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
