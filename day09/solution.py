from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.coords = [[int(coord) for coord in line.split(",")] for line in lines]
        self.boundary_edges = [
            (coord1, coord2)
            for coord1, coord2 in zip(self.coords, [*self.coords[1:], self.coords[0]])
        ]

        corner_pairs: list[tuple[list[int], list[int]]] = []
        for i, corner1 in enumerate(self.coords):
            for corner2 in self.coords[i + 1 :]:
                corner_pairs.append((corner1, corner2))

        self.sorted_possible_corner_pairs = sorted(
            corner_pairs,
            key=lambda corner_pair: self.rectangle_area(*corner_pair),
            reverse=True,
        )

    def rectangle_area(self, coord1: list[int], coord2: list[int]) -> int:
        (x1, y1), (x2, y2) = coord1, coord2
        return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

    def crosses_boundary_edge(self, coord1: list[int], coord2: list[int]) -> bool:
        for (bx1, by1), (bx2, by2) in self.boundary_edges:
            (x1, y1), (x2, y2) = coord1, coord2
            no_overlap_x = max(bx1, bx2) <= min(x1, x2) or max(x1, x2) <= min(bx1, bx2)
            no_overlap_y = max(by1, by2) <= min(y1, y2) or max(y1, y2) <= min(by1, by2)

            if no_overlap_x or no_overlap_y:
                continue
            else:
                return True
        return False

    def solve_part_1(self) -> int:
        largest, *_ = self.sorted_possible_corner_pairs
        return self.rectangle_area(*largest)

    def solve_part_2(self) -> int:
        for rectangle in self.sorted_possible_corner_pairs:
            if not self.crosses_boundary_edge(*rectangle):
                return self.rectangle_area(*rectangle)
        return 0


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 09:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
