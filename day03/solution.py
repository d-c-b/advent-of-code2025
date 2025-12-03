from os import path


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.battery_banks = input_file.read().splitlines()

    def find_max_joltage(self, bank: str, n: int) -> int:
        digits, next_available_index = "", 0
        for digits_to_fill in range(n, 0, -1):
            available_characters = bank[
                next_available_index : len(bank) - digits_to_fill + 1
            ]
            largest_permitted_digit = max(available_characters)
            digits += largest_permitted_digit
            next_available_index += (
                available_characters.index(largest_permitted_digit) + 1
            )

        return int(digits)

    def solve_part_1(self) -> int:
        return sum(
            self.find_max_joltage(battery_bank, n=2)
            for battery_bank in self.battery_banks
        )

    def solve_part_2(self) -> int:
        return sum(
            self.find_max_joltage(battery_bank, n=12)
            for battery_bank in self.battery_banks
        )


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 03:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
