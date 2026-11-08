"""
Evolution engine for Drago.
Calculates evolution stage, progression, rolling decay, and individual anatomical feature unlocks.
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
    
    # Anatomical feature levels (1.0 to 7.0+ continuous or discrete)
    body_scale: float
    horn_level: int
    wing_level: int
    spike_level: int
    armor_level: int
    tail_level: int
    aura_intensity: float    # 0.0 to 1.0 (streak effect)
    
    # Specific feature modifiers
    wing_span_multiplier: float
    tail_length_multiplier: float
    horn_curvature: float
    armor_plates: int
    dorsal_spike_count: int
    eye_glow: float
    
    # Breakdown stats for display/logging
    stats_breakdown: Dict[str, Any] = field(default_factory=dict)

class EvolutionEngine:
    def __init__(self, stage_definitions=None, weights=None, decay_weights=None):
        self.stages = stage_definitions or STAGE_DEFINITIONS
        self.weights = weights or DEFAULT_WEIGHTS.copy()
        self.decay_weights = decay_weights or DECAY_WEIGHTS.copy()

    def calculate_score(self, activity: GitHubActivity) -> tuple[float, float, Dict[str, float]]:
        """
        Calculates raw score and rolling time-decayed activity score.
        Returns: (decayed_score, raw_score, category_scores)
        """
        # Base activity points
        commit_pts = activity.total_commits * self.weights.get("commit", 1.0)
        pr_pts = activity.total_prs * self.weights.get("pull_request", 4.0)
        merged_pr_pts = activity.merged_prs * self.weights.get("merged_pr", 6.0)
        issue_pts = (activity.issues_opened + activity.issues_closed * 0.5) * self.weights.get("issue", 2.0)
        repo_pts = activity.public_repos * self.weights.get("repo", 5.0)
        star_pts = activity.total_stars * self.weights.get("star_received", 1.5)

        raw_score = commit_pts + pr_pts + merged_pr_pts + issue_pts + repo_pts + star_pts

        # Rolling decay component:
        # We weigh recent 7d activity with highest weight, 30d with medium, older with base
        w_7d = self.decay_weights.get("recent_7d", 1.0)
        w_30d = self.decay_weights.get("month_30d", 0.65)
        w_90d = self.decay_weights.get("quarter_90d", 0.35)
        w_base = self.decay_weights.get("year_365d", 0.15)

        # Recent burst score
        recent_7d_pts = (
            activity.recent_commits_7d * self.weights.get("commit", 1.0) +
            activity.recent_prs_7d * self.weights.get("pull_request", 4.0)
        )
        month_30d_pts = (
            activity.commits_30d * self.weights.get("commit", 1.0) +
            activity.prs_30d * self.weights.get("pull_request", 4.0)
        )
        older_pts = max(0.0, raw_score - recent_7d_pts - month_30d_pts)

        # Decay blend ensures you never drop to 0 if you worked hard in past months,
        # but active users surge into higher energy states.
        # Floor: at least 30% of lifetime raw score is permanently retained as draconic wisdom.
        permanence_floor = raw_score * 0.30
        decayed_active = (recent_7d_pts * w_7d) + (month_30d_pts * w_30d) + (older_pts * w_base)
        decayed_score = max(permanence_floor, decayed_active)

        # Streak multiplier
        if activity.current_streak > 0:
            streak_bonus = min(0.35, activity.current_streak * 0.02)
            decayed_score *= (1.0 + streak_bonus)

        categories = {
            "commits": commit_pts,
            "pull_requests": pr_pts + merged_pr_pts,
            "issues": issue_pts,
            "repos": repo_pts,
            "stars": star_pts,
            "streak_days": activity.current_streak,
        }

        return round(decayed_score, 2), round(raw_score, 2), categories

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
        base_scale = current_stage["body_scale"]
        base_horn = current_stage["horn_level"]
        base_wing = current_stage["wing_level"]
        base_spike = current_stage["spike_level"]
        base_armor = current_stage["armor_level"]
        base_tail = current_stage["tail_level"]

        # Feature modifications influenced by specific GitHub activities
        # 1. Commits -> Body mass & muscle maturity (fractional boost up to +0.08)
        commit_boost = min(0.08, math.log10(max(1, activity.total_commits + 1)) * 0.025)
        final_body_scale = round(base_scale + commit_boost, 3)

        # 2. PRs -> Horn development
        pr_count = activity.total_prs + activity.merged_prs
        horn_level = base_horn
        if pr_count >= 10 and horn_level < 7:
            horn_level = min(7, horn_level + 1)
        horn_curvature = 1.0 + min(0.5, pr_count * 0.03)

        # 3. Merged PRs -> Armor development
        armor_level = base_armor
        if activity.merged_prs >= 5 and armor_level < 5:
            armor_level = min(5, armor_level + 1)
        armor_plates = min(6, armor_level + (1 if activity.merged_prs >= 15 else 0))

        # 4. Stars -> Wing development
        wing_level = base_wing
        if activity.total_stars >= 10 and wing_level < 7:
            wing_level = min(7, wing_level + 1)
        wing_span_multiplier = 1.0 + min(0.35, math.log10(max(1, activity.total_stars + 1)) * 0.12)

        # 5. Repos -> Tail & crest development
        tail_level = base_tail
        if activity.public_repos >= 8 and tail_level < 7:
            tail_level = min(7, tail_level + 1)
        tail_length_multiplier = 1.0 + min(0.30, activity.public_repos * 0.02)

        # 6. Spikes -> based on combined PRs and stage
        dorsal_spikes = min(9, base_spike + (1 if pr_count >= 5 else 0))

        # 7. Streak -> Aura intensity (flames/sparkles)
        aura_intensity = 0.0
        if activity.current_streak >= 3:
            aura_intensity = min(1.0, 0.2 + (activity.current_streak - 3) * 0.08)
        elif current_stage.get("aura_enabled", False):
            aura_intensity = 0.4  # Elder dragons have innate mild aura

        eye_glow = 0.3 + (current_stage["level"] * 0.1) + (aura_intensity * 0.3)

        return DragonState(
            score=decayed_score,
            raw_score=raw_score,
            stage_id=current_stage["id"],
            stage_level=current_stage["level"],
            stage_name=current_stage["name"],
            stage_title=current_stage["title"],
            description=current_stage["description"],
            progress_to_next=round(progress, 3),
            next_stage_name=next_name,
            next_stage_score=next_score,
            body_scale=final_body_scale,
            horn_level=horn_level,
            wing_level=wing_level,
            spike_level=dorsal_spikes,
            armor_level=armor_level,
            tail_level=tail_level,
            aura_intensity=round(aura_intensity, 2),
            wing_span_multiplier=round(wing_span_multiplier, 3),
            tail_length_multiplier=round(tail_length_multiplier, 3),
            horn_curvature=round(horn_curvature, 3),
            armor_plates=armor_plates,
            dorsal_spike_count=dorsal_spikes,
            eye_glow=round(min(1.0, eye_glow), 2),
            stats_breakdown=categories,
        )
