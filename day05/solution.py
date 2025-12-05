from os import path
from typing import Generator


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        id_ranges, id_list = input_file.read().strip().split("\n\n")
        self.fresh_id_ranges = sorted(
            [
                tuple(int(val) for val in id_range.split("-"))
                for id_range in id_ranges.split("\n")
            ]
        )
        self.id_list = [int(i) for i in id_list.split("\n")]

    def get_combined_ranges(self) -> Generator[tuple[int, int], None, None]:
        for i, (start, end) in enumerate(self.fresh_id_ranges):
            if i == 0:
                current_start, current_end = start, end
                continue

            if start > current_end:
                yield current_start, current_end
                current_start, current_end = start, end

            else:
                current_start = min(start, current_start)
                current_end = max(end, current_end)

        else:
            yield current_start, current_end

    def solve_part_1(self) -> int:
        fresh_count = 0
        for id_to_check in self.id_list:
            for start, end in self.fresh_id_ranges:
                if start <= id_to_check <= end:
                    fresh_count += 1
                    break
        return fresh_count

    def solve_part_2(self) -> int:
        return sum([end - start + 1 for start, end in self.get_combined_ranges()])


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 05:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
