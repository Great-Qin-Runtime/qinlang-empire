import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from court import recruitment


def make_state(year: int = 1) -> dict:
    return {"tick": year * 24, "year": year, "events": []}


class RecruitmentTests(unittest.TestCase):
    def test_first_run_writes_known_and_emits_no_event_when_seeded(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "known.json"
            state = make_state()
            mans = [{"id": "python", "name": "Python", "province": "白蛇郡", "role": "producer"}]
            new_ids = recruitment.check_recruits(state, mans, path)
            # 首跑：known 为空，python 视作新郡，应生成一条 unlock
            self.assertEqual(new_ids, ["python"])
            self.assertEqual(state["events"][0]["type"], "unlock")
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(saved["known"], ["python"])

    def test_no_event_when_no_new_province(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "known.json"
            recruitment.save_known(path, ["python"])
            state = make_state()
            mans = [{"id": "python", "name": "Python", "province": "白蛇郡", "role": "producer"}]
            new_ids = recruitment.check_recruits(state, mans, path)
            self.assertEqual(new_ids, [])
            self.assertEqual(state["events"], [])

    def test_emits_event_for_new_addition(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "known.json"
            recruitment.save_known(path, ["python"])
            state = make_state(year=42)
            mans = [
                {"id": "python", "name": "Python", "province": "白蛇郡", "role": "producer"},
                {"id": "rust", "name": "Rust", "province": "锈铁郡", "role": "producer"},
            ]
            new_ids = recruitment.check_recruits(state, mans, path)
            self.assertEqual(new_ids, ["rust"])
            event = state["events"][0]
            self.assertEqual(event["type"], "unlock")
            self.assertEqual(event["from_province"], "rust")
            self.assertIn("锈铁郡", event["text"])
            self.assertIn("Rust", event["text"])
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(saved["known"], ["python", "rust"])


if __name__ == "__main__":
    unittest.main()
