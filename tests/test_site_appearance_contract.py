import os
import re
import unittest


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(ROOT_DIR, "site", "index.html")

MONTHS = [
    "Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
    "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec",
]
WEEKDAYS = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]


def js_list(items):
    return "[" + ", ".join(f"'{item}'" for item in items) + "]"


class SiteAppearanceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(INDEX_PATH, "r", encoding="utf-8") as handle:
            cls.html = handle.read()

    def test_headings_are_present_and_levels_do_not_skip(self) -> None:
        self.assertRegex(self.html, r"<h1[^>]*>Activity Heatmaps</h1>")
        self.assertIn(">Přehled mých aktivit</p>", self.html)
        levels = [int(level) for level in re.findall(r"<h([1-6])\b", self.html)]
        for previous, current in zip(levels, levels[1:]):
            self.assertLessEqual(current - previous, 1, f"heading levels: {levels}")

    def test_teal_theme_and_heatmap_cell_style(self) -> None:
        self.assertIn("background: #0d5f5f;", self.html)
        self.assertIn("bg-teal-900", self.html)
        self.assertIn("bg-teal-800", self.html)
        cell = re.search(r"\.cell\s*{([^}]*)}", self.html)
        self.assertIsNotNone(cell)
        self.assertIn("width: 14px;", cell.group(1))
        self.assertIn("height: 14px;", cell.group(1))
        self.assertIn("border: 1px solid rgba(255, 255, 255, 0.8);", cell.group(1))

    def test_core_mount_points_and_controls_exist(self) -> None:
        for element_id in (
            "totalElevAll",
            "everestCount",
            "yearFilter",
            "typeFilter",
            "toggleDaysBtn",
            "resetBtn",
            "statsContainer",
            "extraMetrics",
            "monthBarChart",
            "weekdayBarChart",
            "heatmapsContainer",
        ):
            self.assertIn(f'id="{element_id}"', self.html)
        self.assertIn("aspain/git-sweaty", self.html)
        # Stránka je celá v index.html, původní app.js se nenačítá.
        self.assertNotIn("app.js", self.html)

    def test_heatmap_uses_czech_months_and_weekday_rows(self) -> None:
        # Seznam měsíců je na dvou místech a oba se musí shodovat.
        self.assertIn(f"const months = {js_list(MONTHS)};", self.html)
        self.assertIn(f"const monthOrder = {js_list(MONTHS)};", self.html)
        self.assertIn(f"{js_list(WEEKDAYS)}.map(dayName", self.html)

    def test_default_filter_is_cycling_and_goal_is_set(self) -> None:
        self.assertIn(
            js_list(["Ride", "VirtualRide", "GravelRide", "MountainBikeRide", "EBikeRide"]),
            self.html,
        )
        self.assertIn("const goalDist = 8000;", self.html)
        self.assertIn("Měl bych mít", self.html)

    def test_totals_are_summed_from_aggregates(self) -> None:
        # Součet přes activities započítá denní agregát vícekrát.
        self.assertIn("function sumAggregates(years, types)", self.html)
        self.assertIn("sumAggregates(allData.years, new Set(allData.types))", self.html)
        self.assertIn("sumAggregates(selectedYears, selectedTypes).distance", self.html)

    def test_action_buttons_do_not_stack_listeners(self) -> None:
        for button_id in ("resetBtn", "toggleDaysBtn"):
            self.assertIn(f"getElementById('{button_id}').onclick =", self.html)
            self.assertNotIn(f"getElementById('{button_id}').addEventListener", self.html)


if __name__ == "__main__":
    unittest.main()
