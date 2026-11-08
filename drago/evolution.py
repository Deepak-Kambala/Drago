"""
Evolution engine for Drago.
Calculates evolution stage, progression, and individual anatomical feature unlocks
directly driven by developers' authentic GitHub contribution milestones.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import math
from drago.config import STAGE_DEFINITIONS, DEFAULT_WEIGHTS, DECAY_WEIGHTS

@dataclass
class GitHubActivity:
    total_commits: int = 0
    recent_commits_7d: int = 0
    commits_30d: int = 0
    commits_90d: int = 0
    
    total_prs: int = 0
    recent_prs_7d: int = 0
    prs_30d: int = 0
    
    merged_prs: int = 0
    issues_opened: int = 0
    issues_closed: int = 0
    
    public_repos: int = 0
    total_stars: int = 0
    
    current_streak: int = 0
    longest_streak: int = 0
    
    # Raw contribution counts for custom mapping
    raw_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DragonState:
    score: float
    raw_score: float
    stage_id: str
    stage_level: int
    stage_name: str
    stage_title: str
    description: str
    progress_to_next: float  # 0.0 to 1.0
    next_stage_name: Optional[str]
    next_stage_score: Optional[int]
    is_egg: bool = False
    sprite_file: str = "01_egg.png"
    
    # Anatomical feature levels (1.0 to 7.0+ continuous or discrete)
    body_scale: float = 1.0
    horn_level: int = 0
    wing_level: int = 0
    spike_level: int = 0
    armor_level: int = 0
    tail_level: int = 0
    
    # Kinematic parameters
    aura_intensity: float = 0.0
    wing_span_multiplier: float = 1.0
    tail_length_multiplier: float = 1.0
    horn_curvature: float = 0.5
    armor_plates: int = 2
    dorsal_spike_count: int = 3
    eye_glow: float = 0.5
    
    stats_breakdown: Dict[str, Any] = field(default_factory=dict)

class EvolutionEngine:
    def __init__(self, stage_definitions=None, weights=None, decay_weights=None):
        self.stages = stage_definitions or STAGE_DEFINITIONS
        self.weights = weights or DEFAULT_WEIGHTS.copy()
        self.decay_weights = decay_weights or DECAY_WEIGHTS.copy()

    def calculate_score(self, activity: GitHubActivity) -> tuple[float, float, Dict[str, float]]:
        """
        Calculates evolution power (score) directly based on developer contributions.
        Each contribution awards 1.0 XP progression so the user's level and progress bar
        accurately mirror their progress toward the next evolutionary threshold.
        """
        # User's primary progression score is 1:1 with authentic contributions
        base_score = float(activity.total_commits) * self.weights.get("commit", 1.0)
        
        # Subtle streak bonus that rewards continuous coding without jumping levels prematurely
        streak_bonus = round(min(activity.current_streak * 0.1, 5.0), 1) if activity.current_streak > 0 else 0.0
        
        raw_score = round(base_score + streak_bonus, 1)
        decayed_score = raw_score

        categories = {
            "commits": base_score,
            "pull_requests": float(activity.total_prs),
            "issues": float(activity.issues_opened),
            "repos": float(activity.public_repos),
            "stars": float(activity.total_stars),
            "streak_days": float(activity.current_streak),
        }

        return decayed_score, raw_score, categories

    def evaluate(self, activity: GitHubActivity) -> DragonState:
        decayed_score, raw_score, categories = self.calculate_score(activity)

        # Find current stage
        current_stage = self.stages[0]
        next_stage = None
        for i, stage in enumerate(self.stages):
            if decayed_score >= stage["min_score"]:
                current_stage = stage
                if i + 1 < len(self.stages):
                    next_stage = self.stages[i + 1]
                else:
                    next_stage = None
            else:
                break

        # Calculate progress to next stage
        if next_stage:
            stage_range = next_stage["min_score"] - current_stage["min_score"]
            score_in_stage = decayed_score - current_stage["min_score"]
            progress = max(0.0, min(1.0, score_in_stage / max(1.0, stage_range)))
            next_name = next_stage["name"]
            next_score = next_stage["min_score"]
        else:
            progress = 1.0
            next_name = None
            next_score = None

        # Base attributes from stage
        is_egg = current_stage.get("is_egg", False)
        sprite_file = current_stage.get("sprite_file", f"{current_stage['level']:02d}_{current_stage['id']}.png")
        base_scale = current_stage["body_scale"]
        base_horn = current_stage["horn_level"]
        base_wing = current_stage["wing_level"]
        base_spike = current_stage["spike_level"]
        base_armor = current_stage["armor_level"]
        base_tail = current_stage["tail_level"]

        # Feature modifications influenced by specific GitHub activities
        # 1. Commits -> Body mass & muscle maturity (fractional boost up to +0.08)
        commit_boost = min(0.08, math.log10(max(1, activity.total_commits + 1)) * 0.025)
        body_scale = round(base_scale + commit_boost, 3)

        # 2. Pull Requests -> Horn sweeps and majesty
        pr_horn_bonus = min(2, activity.total_prs // 15)
        horn_level = base_horn + pr_horn_bonus
        horn_curvature = round(0.5 + min(1.0, activity.total_prs * 0.03), 2)

        # 3. Merged PRs & Issues -> Carapace plating
        armor_bonus = min(2, activity.merged_prs // 10)
        armor_level = base_armor + armor_bonus
        armor_plates = min(8, 2 + armor_level)

        # 4. Stars & Repositories -> Wing grandeur and tail blades
        wing_span_mult = round(1.0 + min(0.35, (activity.total_stars * 0.01) + (activity.public_repos * 0.015)), 2)
        wing_level = base_wing + min(2, activity.total_stars // 25)

        tail_len_mult = round(1.0 + min(0.30, activity.public_repos * 0.02), 2)
        tail_level = base_tail + min(2, activity.public_repos // 10)

        # 5. Spikes
        spike_level = base_spike + min(2, (activity.total_commits // 100))
        dorsal_spikes = min(12, 3 + spike_level)

        # 6. Contribution Streak -> Flaming Draconic Aura & Eye Glow
        if activity.current_streak >= 3 or current_stage.get("aura_enabled", False):
            aura_intensity = round(min(1.0, 0.4 + (activity.current_streak * 0.05)), 2)
            eye_glow = round(min(1.0, 0.6 + (activity.current_streak * 0.04)), 2)
        else:
            aura_intensity = 0.0
            eye_glow = 0.5

        return DragonState(
            score=decayed_score,
            raw_score=raw_score,
            stage_id=current_stage["id"],
            stage_level=current_stage["level"],
            stage_name=current_stage["name"],
            stage_title=current_stage["title"],
            description=current_stage["description"],
            progress_to_next=round(progress, 4),
            next_stage_name=next_name,
            next_stage_score=next_score,
            is_egg=is_egg,
            sprite_file=sprite_file,
            body_scale=body_scale,
            horn_level=horn_level,
            wing_level=wing_level,
            spike_level=spike_level,
            armor_level=armor_level,
            tail_level=tail_level,
            aura_intensity=aura_intensity,
            wing_span_multiplier=wing_span_mult,
            tail_length_multiplier=tail_len_mult,
            horn_curvature=horn_curvature,
            armor_plates=armor_plates,
            dorsal_spike_count=dorsal_spikes,
            eye_glow=eye_glow,
            stats_breakdown=categories,
        )
