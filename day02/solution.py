import re
from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.ranges = [
            id_range.split("-") for id_range in input_file.read().strip().split(",")
        ]

    def is_invalid(self, number: int, invalid_regex: str) -> bool:
        if re.match(invalid_regex, str(number)):
            return True
        return False

    def solve(self, invalid_regex: str) -> int:
        invalid = []
        for start, end in self.ranges:
            current = int(start)
            while current <= int(end):
                if self.is_invalid(current, invalid_regex):
                    invalid.append(current)
                current += 1

        return sum(invalid)

    def solve_part_1(self) -> int:
        return self.solve(invalid_regex=r"^(\d+)\1$")

    def solve_part_2(self) -> int:
        return self.solve(invalid_regex=r"^(\d+)\1+$")


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 02:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
