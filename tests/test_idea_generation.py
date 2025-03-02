import unittest
from agents.idea_generation import get_trending_ideas

class TestIdeaGeneration(unittest.TestCase):
    def test_general_trends(self):
        results = get_trending_ideas("US", None, 5)
        self.assertTrue(len(results["trending_topics"]) > 0, "No trending topics found!")

    def test_topic_trends(self):
        results = get_trending_ideas("US", "AI", 5)
        self.assertTrue(len(results["trending_topics"]) > 0, "No AI-related trending topics found!")

if __name__ == "__main__":
    unittest.main()
 
