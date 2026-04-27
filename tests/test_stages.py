import copy
import unittest

from court import stages


BASE_STATE = {
    "schema_version": 1,
    "dynasty": "秦",
    "tick": 0,
    "year": 0,
    "stage": "qin-yi",
    "stage_progress": 0,
    "treasury": {},
    "provinces": {},
    "events": [],
    "milestones": [
        {"id": "first-100-wenshu", "achieved": False},
        {"id": "first-city", "achieved": False},
        {"id": "fall-of-han", "achieved": False},
        {"id": "fall-of-zhao", "achieved": False},
        {"id": "fall-of-wei", "achieved": False},
        {"id": "fall-of-chu", "achieved": False},
        {"id": "fall-of-yan", "achieved": False},
        {"id": "fall-of-qi", "achieved": False},
    ],
    "stats": {},
    "seal": None,
}


class StageTests(unittest.TestCase):
    def test_qin_yi_does_not_advance_when_requirements_are_missing(self):
        state = copy.deepcopy(BASE_STATE)
        result = stages.maybe_advance(state)
        self.assertFalse(result["advanced"])
        self.assertEqual(state["stage"], "qin-yi")
        self.assertLess(state["stage_progress"], 1)

    def test_qin_yi_advances_to_chun_qiu_when_requirements_are_met(self):
        state = copy.deepcopy(BASE_STATE)
        state["year"] = 40
        state["tick"] = 960
        state["treasury"] = {
            "wen-shu": 500,
            "gong-ju": 200,
            "hu-ji": 100,
            "jian-zhu": 5,
        }
        for milestone in state["milestones"]:
            if milestone["id"] in {"first-100-wenshu", "first-city"}:
                milestone["achieved"] = True

        result = stages.maybe_advance(state)

        self.assertTrue(result["advanced"])
        self.assertEqual(state["stage"], "chun-qiu")
        self.assertEqual(state["seal"], "seal-chun-qiu-960")
        self.assertEqual(state["events"][0]["type"], "epoch")

    def test_heng_sao_to_yi_tong_halves_treasury_and_adds_buff(self):
        state = copy.deepcopy(BASE_STATE)
        state["stage"] = "heng-sao"
        state["year"] = 500
        state["tick"] = 12000
        state["treasury"] = {"bing-qi": 3000, "bing-ma": 2000, "qian-liang": 5000}
        for milestone in state["milestones"]:
            milestone["achieved"] = milestone["id"].startswith("fall-of-")

        result = stages.maybe_advance(state, [{"id": "brainfuck", "province": "奇技郡", "role": "ceremonial"}])

        self.assertTrue(result["advanced"])
        self.assertEqual(state["stage"], "yi-tong")
        self.assertEqual(state["treasury"]["bing-qi"], 1500)
        self.assertEqual(state["treasury"]["bing-ma"], 1000)
        self.assertEqual(state["treasury"]["qian-liang"], 2500)
        self.assertIn("yi-tong-production", state["buffs"])
        self.assertEqual(state["events"][0]["type"], "ceremony")


if __name__ == "__main__":
    unittest.main()
