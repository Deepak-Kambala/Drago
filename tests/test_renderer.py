"""
Tests for Drago rendering pipeline, geometry, and status card generation.
"""

import os
import unittest
from drago.config import DragoConfig
from drago.evolution import EvolutionEngine, GitHubActivity
from drago.renderer import DragonRenderer
from drago.status_card import generate_status_svg

class TestRenderer(unittest.TestCase):
    def setUp(self):
        self.config = DragoConfig(width=320, height=210, frame_count=4, fps=8)
        self.engine = EvolutionEngine()
        self.activity = GitHubActivity(total_commits=200, total_prs=15, merged_prs=10)
        self.state = self.engine.evaluate(self.activity)

    def test_render_animation_frames(self):
        renderer = DragonRenderer(self.config, self.state)
        frames = renderer.render_animation(action="idle")
        self.assertEqual(len(frames), self.config.frame_count)
        self.assertEqual(frames[0].size, (self.config.width, self.config.height))

    def test_save_gif(self):
        renderer = DragonRenderer(self.config, self.state)
        frames = renderer.render_animation(action="idle")
        test_out = "assets/test_output.gif"
        renderer.save_gif(frames, test_out)
        self.assertTrue(os.path.exists(test_out))
        self.assertGreater(os.path.getsize(test_out), 1000)
        os.remove(test_out)

    def test_status_card_svg(self):
        test_svg = "assets/test_status.svg"
        generate_status_svg(self.state, self.activity, self.config, test_svg)
        self.assertTrue(os.path.exists(test_svg))
        with open(test_svg, "r") as f:
            content = f.read()
        self.assertIn("<svg", content)
        self.assertIn("EVOLUTION POWER", content.upper())
        os.remove(test_svg)

if __name__ == "__main__":
    unittest.main()
