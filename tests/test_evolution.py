"""
Tests for Drago evolution engine, feature unlocks, and rolling decay.
"""

import unittest
from drago.evolution import EvolutionEngine, GitHubActivity
from drago.config import STAGE_DEFINITIONS

class TestEvolutionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EvolutionEngine()

    def test_egg_stage(self):
        act = GitHubActivity(total_commits=5, recent_commits_7d=5)
        state = self.engine.evaluate(act)
        self.assertEqual(state.stage_level, 1)
        self.assertEqual(state.stage_name, "Egg")
        self.assertTrue(state.is_egg)

    def test_hatchling_stage(self):
        act = GitHubActivity(total_commits=30, recent_commits_7d=30)
        state = self.engine.evaluate(act)
        self.assertEqual(state.stage_level, 2)
        self.assertEqual(state.stage_name, "Hatchling")
        self.assertFalse(state.is_egg)

    def test_progression_thresholds(self):
        # Test crossing into Adolescent with active recent commits
        act = GitHubActivity(
            total_commits=220,
            recent_commits_7d=60,
            commits_30d=120,
            total_prs=15,
            merged_prs=10,
        )
        state = self.engine.evaluate(act)
        self.assertGreaterEqual(state.stage_level, 3)

    def test_feature_unlock_prs_affect_horns(self):
        act_few_prs = GitHubActivity(total_commits=300, total_prs=2)
        act_many_prs = GitHubActivity(total_commits=300, total_prs=30, merged_prs=20)
        
        s1 = self.engine.evaluate(act_few_prs)
        s2 = self.engine.evaluate(act_many_prs)
        self.assertGreater(s2.horn_level, s1.horn_level)
        self.assertGreater(s2.horn_curvature, s1.horn_curvature)

    def test_feature_unlock_merged_prs_affect_armor(self):
        act_no_merged = GitHubActivity(total_commits=300, merged_prs=0)
        act_many_merged = GitHubActivity(total_commits=300, merged_prs=25)
        
        s1 = self.engine.evaluate(act_no_merged)
        s2 = self.engine.evaluate(act_many_merged)
        self.assertGreater(s2.armor_level, s1.armor_level)
        self.assertGreater(s2.armor_plates, s1.armor_plates)

    def test_stars_affect_wings(self):
        act_no_stars = GitHubActivity(total_commits=300, total_stars=0)
        act_starred = GitHubActivity(total_commits=300, total_stars=150)
        
        s1 = self.engine.evaluate(act_no_stars)
        s2 = self.engine.evaluate(act_many_stars := act_starred)
        self.assertGreater(s2.wing_span_multiplier, s1.wing_span_multiplier)

    def test_rolling_decay_gradual(self):
        # User who had 1000 commits long ago but 0 recent commits
        act_inactive = GitHubActivity(
            total_commits=1000,
            recent_commits_7d=0,
            commits_30d=0,
            commits_90d=10,
        )
        state = self.engine.evaluate(act_inactive)
        # Should NOT drop to 0! Permanence floor retains wisdom
        self.assertGreater(state.score, 0)
        self.assertGreaterEqual(state.stage_level, 3)

    def test_streak_multiplier_and_aura(self):
        act_no_streak = GitHubActivity(total_commits=300, current_streak=0)
        act_high_streak = GitHubActivity(total_commits=300, current_streak=15)
        
        s1 = self.engine.evaluate(act_no_streak)
        s2 = self.engine.evaluate(act_high_streak)
        self.assertGreater(s2.score, s1.score)
        self.assertGreater(s2.aura_intensity, s1.aura_intensity)

if __name__ == "__main__":
    unittest.main()
