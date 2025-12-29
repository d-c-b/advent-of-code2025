from functools import cache
from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.servers: dict[str, list[str]] = dict()
        for line in input_file.read().strip().splitlines():
            device, outputs = line.split(": ")
            self.servers[device] = outputs.split(" ")

    @cache
    def find_path_count(
        self, source: str, target: str, must_visit: tuple[str, ...] = tuple()
    ) -> int:
        if source == target:
            if not must_visit:
                return 1
            return 0

        return sum(
            self.find_path_count(
                source=neighbour,
                target=target,
                must_visit=tuple([node for node in must_visit if node != source]),
            )
            for neighbour in self.servers[source]
        )

    def solve_part_1(self) -> int:
        return self.find_path_count(source="you", target="out")

    def solve_part_2(self) -> int:
        return self.find_path_count(
            source="svr", target="out", must_visit=("fft", "dac")
        )


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 11:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
