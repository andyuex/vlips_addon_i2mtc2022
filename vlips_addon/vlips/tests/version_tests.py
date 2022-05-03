import unittest

from vlips import Version


class TestVersion(unittest.TestCase):

    def test_init_version_with_three_components(self):
        version_as_string = "1.2.3"
        version = Version(1, 2, 3)
        self.assertEqual(
            version_as_string, version.to_string(),
            f"Version as string should be {version_as_string} but is {version.to_string()}")

    def test_init_version_with_tuple(self):
        version_as_string = "1.2.3"
        version = Version(components=(1, 2, 3))
        self.assertEqual(
            version_as_string, version.to_string(),
            f"Version as string should be {version_as_string} but is {version.to_string()}")
