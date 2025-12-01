from os import path


DIRECTION_NUMBERS = {"L": -1, "R": 1}


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.START = 50
        self.turns = [
            (t[0], int(t[1:])) for t in input_file.read().strip().splitlines()
        ]

    def solve_part_1(self) -> int:
        current_pos = self.START
        zero_count = 0
        for direction, number in self.turns:
            current_pos = (current_pos + number * DIRECTION_NUMBERS[direction]) % 100
            if current_pos == 0:
                zero_count += 1
        return zero_count

    def solve_part_2(self) -> int:
        current_pos = self.START
        zero_count = 0
        for direction, number in self.turns:
            if current_pos == 0:
                dist_to_zero = 100
            else:
                match direction:
                    case "L":
                        dist_to_zero = current_pos

                    case "R":
                        dist_to_zero = 100 - current_pos

            if dist_to_zero <= number:
                zero_count += 1 + (number - dist_to_zero) // 100

            current_pos = (current_pos + number * DIRECTION_NUMBERS[direction]) % 100

        return zero_count


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 01:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
