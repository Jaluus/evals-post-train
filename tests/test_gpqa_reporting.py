import tempfile
import unittest
from pathlib import Path

from make_html_table import build_html, parse_metrics_file

REPO_ROOT = Path(__file__).resolve().parents[1]


class GpqaReportingTests(unittest.TestCase):
    def test_main_and_diamond_render_as_separate_test_benchmarks(self):
        groups = parse_metrics_file(
            REPO_ROOT / "configs/apertus/tasks_default_main_table.txt"
        )
        scores = {
            "model": {
                "gpqa_main_cot_zeroshot/exact_match,ordered-extract": 40.0,
                "gpqa_diamond_cot_zeroshot/exact_match,ordered-extract": 30.0,
            }
        }
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "report.html"
            build_html(groups, ["model"], scores, output)
            html = output.read_text()

        train_table, test_table = html.split("id=\"table-train\">", 1)[1].split(
            "id=\"table-test\">", 1
        )
        for task in ["gpqa_main_cot_zeroshot", "gpqa_diamond_cot_zeroshot"]:
            self.assertIn(task, test_table)
            self.assertNotIn(task, train_table)


if __name__ == "__main__":
    unittest.main()
