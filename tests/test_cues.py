import unittest
from app import extract_cues

class CueTests(unittest.TestCase):
    def test_url_detected(self):
        self.assertIn("URL included in the message", extract_cues("Check https://example.invalid"))

    def test_urgent_detected(self):
        self.assertIn("Urgency or time pressure", extract_cues("Urgent, act now"))

if __name__ == "__main__":
    unittest.main()
