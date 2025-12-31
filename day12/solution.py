from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        *presents, regions = input_file.read().strip().split("\n\n")

        self.presents = []
        for pres in presents:
            _, *present = pres.split("\n")
            self.presents.append(present)

        self.regions = []
        for region in regions.split("\n"):
            (size, present_counts) = region.split(": ")
            width, height = size.split("x")
            self.regions.append(
                (
                    int(width),
                    int(height),
                    [int(count) for count in present_counts.split()],
                )
            )

    def filled_spaces(self, present_index: int) -> int:
        return sum([c == "#" for row in self.presents[present_index] for c in row])

    def can_fit(self, region) -> bool:
        width, height, counts = region
        total_space_taken = sum(
            [
                self.filled_spaces(present_index) * n
                for present_index, n in enumerate(counts)
            ]
        )
        if total_space_taken > width * height:
            return False
        return True

    def solve_part_1(self) -> int:
        return sum(self.can_fit(region) for region in self.regions)


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 12:
        Part 1 Solution: {s.solve_part_1()}
        """
    )
