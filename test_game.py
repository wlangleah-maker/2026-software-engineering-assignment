import unittest

from game_logic import Arrow, GameModel, find_solution
from levels import LEVELS, MAX_MISTAKES


class GameLogicTests(unittest.TestCase):
    def test_t01_unblocked_arrow_is_removed(self):
        model = GameModel([Arrow("A", 2, 2, "right")])
        self.assertEqual(model.click("A"), "won")
        self.assertEqual(model.remaining, 0)

    def test_t02_blocked_arrow_stays_and_costs_one_mistake(self):
        model = GameModel([
            Arrow("A", 2, 1, "right"),
            Arrow("B", 2, 4, "up"),
        ])
        self.assertEqual(model.click("A"), "blocked")
        self.assertIn("A", model.arrows)
        self.assertEqual(model.mistakes_left, MAX_MISTAKES - 1)

    def test_t03_edge_arrow_does_not_go_out_of_bounds(self):
        cases = [
            Arrow("U", 0, 2, "up"),
            Arrow("D", 4, 2, "down"),
            Arrow("L", 2, 0, "left"),
            Arrow("R", 2, 4, "right"),
        ]
        for arrow in cases:
            with self.subTest(direction=arrow.direction):
                model = GameModel([arrow])
                self.assertFalse(model.is_blocked(arrow.id))
                self.assertEqual(model.click(arrow.id), "won")

    def test_t04_clearing_level_reports_win(self):
        model = GameModel([
            Arrow("A", 0, 0, "up"),
            Arrow("B", 4, 4, "down"),
        ])
        self.assertEqual(model.click("A"), "removed")
        self.assertEqual(model.click("B"), "won")
        self.assertTrue(model.won)

    def test_t05_mistakes_exhausted_reports_failure(self):
        model = GameModel([
            Arrow("A", 2, 1, "right"),
            Arrow("B", 2, 4, "left"),
        ], max_mistakes=3)
        self.assertEqual(model.click("A"), "blocked")
        self.assertEqual(model.click("A"), "blocked")
        self.assertEqual(model.click("A"), "failed")
        self.assertTrue(model.failed)

    def test_t06_restart_restores_layout_and_mistakes(self):
        arrows = [Arrow("A", 2, 1, "right"), Arrow("B", 2, 4, "up")]
        model = GameModel(arrows)
        model.click("A")
        model.click("B")
        model.reset()
        self.assertEqual(set(model.arrows), {"A", "B"})
        self.assertEqual(model.mistakes_left, MAX_MISTAKES)

    def test_all_official_levels_are_solvable(self):
        for index, level in enumerate(LEVELS, start=1):
            with self.subTest(level=index):
                solution = find_solution(level["arrows"])
                self.assertIsNotNone(solution)
                self.assertEqual(len(solution), len(level["arrows"]))

    def test_solution_really_clears_each_level(self):
        for level in LEVELS:
            model = GameModel(level["arrows"])
            solution = find_solution(level["arrows"])
            self.assertIsNotNone(solution)
            for arrow_id in solution:
                self.assertFalse(model.is_blocked(arrow_id))
                model.click(arrow_id)
            self.assertTrue(model.won)


if __name__ == "__main__":
    unittest.main(verbosity=2)
