import unittest

from tools.check_data_safety import find_forbidden_paths


class DataSafetyTests(unittest.TestCase):
    def test_repository_contains_no_personal_data_paths(self):
        self.assertEqual(find_forbidden_paths(), [])


if __name__ == "__main__":
    unittest.main()
