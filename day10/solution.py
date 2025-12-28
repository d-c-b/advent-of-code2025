from collections import deque
from os import path

EPSILON = 1e-9


class Machine:
    def __init__(
        self, buttons: list[list[int]], joltage_requirements: list[int]
    ) -> None:
        self.buttons = buttons
        self.joltage_requirements = joltage_requirements
        self.matrix = [
            [*[1 if j in button else 0 for button in buttons], joltage_requirements[j]]
            for j in range(len(joltage_requirements))
        ]
        self.reduced_matrix, self.dependent_variable_indices = (
            self.gaussian_elimination(self.matrix)
        )
        self.free_indices = [
            i for i in range(len(buttons)) if i not in self.dependent_variable_indices
        ]

    def gaussian_elimination(
        self, matrix: list[list[int]]
    ) -> tuple[list[list[float]], list[int]]:
        rows, columns = len(matrix), len(matrix[0])
        current_row, current_column = 0, 0
        reduced_matrix = [[float(x) for x in row] for row in matrix]

        dependent_variable_indices = []

        while current_row < rows and current_column < columns - 1:
            i_nonzero = -1
            for i in range(current_row, rows):
                if abs(reduced_matrix[i][current_column]) > EPSILON:
                    i_nonzero = i
                    break
            else:
                current_column += 1
                continue

            reduced_matrix[i_nonzero], reduced_matrix[current_row] = (
                reduced_matrix[current_row],
                reduced_matrix[i_nonzero],
            )
            dependent_variable_indices.append(current_column)

            for i in range(current_row + 1, rows):
                factor = (
                    reduced_matrix[i][current_column]
                    / reduced_matrix[current_row][current_column]
                )
                reduced_matrix[i][current_column] = 0
                for j in range(current_column + 1, columns):
                    reduced_matrix[i][j] = (
                        reduced_matrix[i][j] - reduced_matrix[current_row][j] * factor
                    )

            current_row += 1
            current_column += 1

        return reduced_matrix, dependent_variable_indices

    def solve_min_presses(self) -> int:
        queue = deque([{free_var: 0 for free_var in self.free_indices}])
        best = 1_000_000
        seen = set()
        max_possible_press_count = {
            free_var: min(
                [self.joltage_requirements[i] for i in self.buttons[free_var]]
            )
            for free_var in self.free_indices
        }

        while queue:
            free_var_counts = queue.popleft()
            if tuple(free_var_counts.items()) in seen:
                continue

            seen.add(tuple(free_var_counts.items()))

            solution_vector = self.get_solution_vector(free_var_counts)
            if self.valid_joltage_configuration(solution_vector):
                total_presses = sum([round(presses) for presses in solution_vector])
                best = min(total_presses, best)

            for free_var_index in free_var_counts:
                updated_free_var_count = {**free_var_counts}
                updated_free_var_count[free_var_index] += 1

                if (
                    updated_free_var_count[free_var_index]
                    > max_possible_press_count[free_var_index]
                ):
                    continue

                queue.append(updated_free_var_count)
        return best

    def get_solution_vector(self, free_var_values: dict[int, int]) -> list[float]:
        solution_vector = [
            float(0) if i not in free_var_values else float(free_var_values[i])
            for i in range(len(self.buttons))
        ]

        for row in reversed(self.reduced_matrix):
            if all(abs(x) < EPSILON for x in row):
                continue
            for dep_var_index, col in enumerate(row):
                if abs(col) < EPSILON:
                    continue
                dep_var, *coefficients, val = row[dep_var_index:]
                solution_vector[dep_var_index] = (
                    val
                    - sum(
                        [
                            solution_vector[n] * coefficient
                            for n, coefficient in enumerate(
                                coefficients, start=dep_var_index + 1
                            )
                        ]
                    )
                ) / dep_var
                break

        return solution_vector

    def valid_joltage_configuration(self, solution_vector: list[float]) -> bool:
        if any([press_count < 0 for press_count in solution_vector]):
            return False

        if not all(
            [
                (press_count - round(press_count)) < EPSILON
                for press_count in solution_vector
            ]
        ):
            return False

        joltage_counts = [0 for _ in range(len(self.joltage_requirements))]
        for button, press_count in zip(self.buttons, solution_vector):
            for c in button:
                joltage_counts[c] += round(press_count)

        if joltage_counts == self.joltage_requirements:
            return True
        return False


class Solution:
    def __init__(self) -> None:
        input_file = open(path.join(path.dirname(__file__), "input.txt"), "r")
        self.machines = []
        for line in input_file.read().strip().splitlines():
            required_lights_string, *buttons_strings, joltage_requirements_string = (
                line.split(" ")
            )
            required_lights = sum(
                [
                    (1 if c == "#" else 0) << i
                    for i, c in enumerate(required_lights_string.strip("[]"))
                ]
            )
            buttons = [
                [int(i) for i in button.strip("()").split(",")]
                for button in buttons_strings
            ]
            joltage_requirements = [
                int(j) for j in joltage_requirements_string.strip("{}").split(",")
            ]
            self.machines.append((required_lights, buttons, joltage_requirements))

    def solve_part_1(self) -> int:
        total_presses_lights = 0
        for required_lights, buttons, _ in self.machines:
            button_bits = [sum([(1 << i) for i in button]) for button in buttons]
            start_lights = 0
            seen_states = dict()
            queue = deque([(start_lights, 0)])

            while queue:
                state, buttons_pressed = queue.popleft()
                if state in seen_states:
                    continue
                seen_states[state] = buttons_pressed
                if state == required_lights:
                    break

                for button in button_bits:
                    queue.append((state ^ button, buttons_pressed + 1))

            total_presses_lights += seen_states[required_lights]

        return total_presses_lights

    def solve_part_2(self) -> int:
        total_presses_joltages = 0
        for _, buttons, joltage_requirements in self.machines:
            machine = Machine(buttons, joltage_requirements)
            total_presses_joltages += machine.solve_min_presses()
        return total_presses_joltages


if __name__ == "__main__":
    s = Solution()
    print(
        f"""
        Day 10:
        Part 1 Solution: {s.solve_part_1()}
        Part 2 Solution: {s.solve_part_2()}
        """
    )
