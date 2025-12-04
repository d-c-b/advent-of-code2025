from os import path

ALL_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().splitlines()
        self.roll_positions = set(
            [
                (i, j)
                for j, line in enumerate(lines)
                for i, char in enumerate(line)
                if char == "@"
            ]
        )

    def find_removable_positions(self) -> set[tuple[int, int]]:
        removable = set()
        for (x, y) in self.roll_positions:
            neighbours = [(x + dx, y + dy) for dx, dy in ALL_DIRECTIONS]
            if len([n for n in neighbours if n in self.roll_positions]) < 4:
                removable.add((x, y))

        return removable

    def solve_part_1(self) -> int:
        return len(self.find_removable_positions())

    def solve_part_2(self) -> int:
        total_removed = 0
        while removable := self.find_removable_positions():
            total_removed += len(removable)
            self.roll_positions -= removable

        return total_removed


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 04:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
