from collections import deque
from math import prod
from os import path


def distance(coord1: tuple[int, int, int], coord2: tuple[int, int, int]) -> int:
    (x1, y1, z1), (x2, y2, z2) = coord1, coord2
    return (abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2 + abs(z1 - z2) ** 2) ** 0.5


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        lines = input_file.read().strip().splitlines()
        self.junction_boxes: list[tuple[int, int, int]] = []
        for line in lines:
            x, y, z = line.split(",")
            self.junction_boxes.append((int(x), int(y), int(z)))

        self.distances = sorted(
            [
                tuple((coord1, coord2))
                for i, coord1 in enumerate(self.junction_boxes)
                for coord2 in self.junction_boxes[i + 1 :]
            ],
            key=lambda pair: distance(*pair),
        )

    def separate_components_after_n_connections(
        self, n: int
    ) -> list[set[tuple[int, int, int]]]:

        connections: dict[tuple[int, int, int], set[tuple[int, int, int]]] = {
            junction_box: set() for junction_box in self.junction_boxes
        }
        for i in range(n):
            c1, c2 = self.distances[i]
            connections[c1].add(c2)
            connections[c2].add(c1)

        components: list[set[tuple[int, int, int]]] = []

        for junction_box in self.junction_boxes:
            if any(junction_box in component for component in components):
                continue
            current_component = set()
            queue = deque([junction_box])

            while queue:
                junction_box = queue.popleft()
                current_component.add(junction_box)
                direct_connections = connections[junction_box]
                queue.extend(direct_connections - current_component)
                current_component.update(direct_connections)

            components.append(current_component)

        return components

    def solve_part_1(self) -> int:
        components = self.separate_components_after_n_connections(n=1000)
        return prod(sorted([len(comp) for comp in components], reverse=True)[:3])

    def solve_part_2(self) -> int:
        left, right = 0, len(self.distances) - 1
        while right - left > 1:
            middle = left + (right - left) // 2
            if len(self.separate_components_after_n_connections(middle)) > 1:
                left = middle
            else:
                right = middle

        (x1, *_), (x2, *_) = self.distances[left]
        return x1 * x2


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 08:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
