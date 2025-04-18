import unittest
from selenium import webdriver

class TestWebAutomation(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # You can change this to the browser of your choice

    def test_example(self):
        self.driver.get("http://example.com")
        self.assertIn("Example Domain", self.driver.title)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()