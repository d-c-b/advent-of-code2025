from collections import deque
from functools import cache
from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.y_max, self.x_max = len(lines) - 1, len(lines[0]) - 1
        self.beam_splitters: set[tuple[int, int]] = set()
        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                if char == "^":
                    self.beam_splitters.add((i, j))
                elif char == "S":
                    self.start = (i, j)

    def solve_part_1(self) -> int:
        activated_beam_splitters: set[tuple[int, int]] = set()
        queue = deque([self.start])
        while queue:
            x, y = queue.popleft()
            while (x, y) not in self.beam_splitters and y <= self.y_max:
                y += 1
            if y > self.y_max or (x, y) in activated_beam_splitters:
                continue
            activated_beam_splitters.add((x, y))
            queue.extend(
                [
                    (x + 1, y),
                    (x - 1, y),
                ]
            )

        return len(activated_beam_splitters)

    @cache
    def distinct_beams_from_position(self, position: tuple[int, int]) -> int:
        x, y = position
        while (x, y) not in self.beam_splitters:
            y += 1
            if y > self.y_max:
                return 1

        return self.distinct_beams_from_position(
            (x - 1, y)
        ) + self.distinct_beams_from_position((x + 1, y))

    def solve_part_2(self) -> int:
        return self.distinct_beams_from_position(self.start)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 07:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
