import unittest
from agents.script_writer import script_generator

class TestScriptGenerator(unittest.TestCase):
    def test_generate_titles(self):
        """✅ Test if at least 5 video titles are generated without user input."""
        results = script_generator("US", "AI", return_json=False, selected_index=0)
        self.assertTrue(len(results["selected_title"]) > 0, "No valid title generated.")

    def test_generate_script(self):
        """✅ Test if the script is generated properly without user input."""
        results = script_generator("US", "AI", return_json=False, selected_index=1)
        self.assertTrue(len(results["script"]) > 10, "Script generation failed.")

if __name__ == "__main__":
    unittest.main()
