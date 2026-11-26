import os
import re
import unittest


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(ROOT_DIR, "site", "index.html")


class SummaryResponsiveContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(INDEX_PATH, "r", encoding="utf-8") as handle:
            cls.html = handle.read()

    def _classes_of(self, element_id: str) -> set:
        match = re.search(rf'<div id="{element_id}" class="([^"]*)"', self.html)
        self.assertIsNotNone(match, f"Could not find element: {element_id}")
        return set(match.group(1).split())

    def test_viewport_is_set_for_mobile(self) -> None:
        self.assertIn('content="width=device-width, initial-scale=1"', self.html)

    def test_summary_cards_go_from_two_to_five_columns(self) -> None:
        self.assertLessEqual({"grid", "grid-cols-2", "md:grid-cols-5"}, self._classes_of("statsContainer"))

    def test_extra_metrics_stack_on_mobile(self) -> None:
        self.assertLessEqual({"grid", "grid-cols-1", "md:grid-cols-3"}, self._classes_of("extraMetrics"))

    def test_filters_and_charts_stack_on_mobile(self) -> None:
        self.assertIn('class="grid grid-cols-1 md:grid-cols-4 gap-6"', self.html)
        self.assertIn('class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8"', self.html)

    def test_heatmap_scrolls_inside_its_own_box(self) -> None:
        self.assertIn('class="overflow-x-auto pb-2 mb-8"', self.html)


if __name__ == "__main__":
    unittest.main()
