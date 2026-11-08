"""
Configuration and color palettes for Drago.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List

# Color Palettes
PALETTES: Dict[str, Dict[str, str]] = {
    # Default: homage to the iconic bold action-cartoon dragon aesthetic
    "obsidian-gold": {
        "name": "Obsidian Gold",
        "body_primary": "#1E1F24",      # Dark charcoal / near-black
        "body_secondary": "#121317",    # Deepest shadow
        "body_highlight": "#34363F",    # Subtle blue-charcoal rim/highlight
        "underbelly": "#2A2C34",        # Lighter charcoal belly plates
        "accent": "#F5B700",            # Radiant energetic gold markings
        "accent_glow": "#FFD13B",       # Glowing highlight for markings
        "accent_dark": "#B88200",       # Dark amber shading on markings
        "horns": "#15161A",             # Deep horn tone
        "horns_highlight": "#4B4E59",   # Horn ridge highlight
        "claws": "#E8EAF0",             # Sharp bone/ivory claws
        "claws_shadow": "#8C90A0",
        "eyes": "#FFB703",              # Piercing amber eyes
        "pupil": "#0B0C0E",
        "wing_bone": "#1A1B20",
        "wing_membrane": "#22242B",     # Dark leather membrane
        "wing_membrane_inner": "#2E303A",
        "armor": "#2B2D37",             # Reinforced plating
        "armor_edge": "#5A5E70",
        "spikes": "#18191E",
        "aura": "#FFD13B",              # Streak energy flame/aura
    },
    "crimson-fury": {
        "name": "Crimson Fury",
        "body_primary": "#2D0F14",
        "body_secondary": "#180609",
        "body_highlight": "#4E1A22",
        "underbelly": "#3B151C",
        "accent": "#FF2A4D",
        "accent_glow": "#FF6B85",
        "accent_dark": "#A6142E",
        "horns": "#1A090C",
        "horns_highlight": "#57212B",
        "claws": "#F4D9DC",
        "claws_shadow": "#9A6B72",
        "eyes": "#FF4D00",
        "pupil": "#0D0405",
        "wing_bone": "#240C10",
        "wing_membrane": "#2B1117",
        "wing_membrane_inner": "#3C1820",
        "armor": "#3A131A",
        "armor_edge": "#702A36",
        "spikes": "#1E0A0D",
        "aura": "#FF3366",
    },
    "arctic-frost": {
        "name": "Arctic Frost",
        "body_primary": "#E2E9F2",
        "body_secondary": "#B0C2D6",
        "body_highlight": "#FFFFFF",
        "underbelly": "#CBD8E7",
        "accent": "#00D2FF",
        "accent_glow": "#80E9FF",
        "accent_dark": "#008EB3",
        "horns": "#1B2A3D",
        "horns_highlight": "#38567A",
        "claws": "#D4E8F8",
        "claws_shadow": "#6E93B5",
        "eyes": "#00F0FF",
        "pupil": "#08131F",
        "wing_bone": "#BDD0E4",
        "wing_membrane": "#8EAAC5",
        "wing_membrane_inner": "#A5BFD8",
        "armor": "#96ADC7",
        "armor_edge": "#CAD9EA",
        "spikes": "#23374F",
        "aura": "#5CE1E6",
    },
    "cyberpunk-neon": {
        "name": "Cyberpunk Neon",
        "body_primary": "#14141E",
        "body_secondary": "#0A0A10",
        "body_highlight": "#28283C",
        "underbelly": "#1E1E2C",
        "accent": "#00F5D4",
        "accent_glow": "#7BFDEB",
        "accent_dark": "#009E88",
        "horns": "#1C1126",
        "horns_highlight": "#7B2CBF",
        "claws": "#F72585",
        "claws_shadow": "#9B004D",
        "eyes": "#FF007F",
        "pupil": "#05050A",
        "wing_bone": "#191726",
        "wing_membrane": "#1B1728",
        "wing_membrane_inner": "#271E3A",
        "armor": "#231B33",
        "armor_edge": "#9D4EDD",
        "spikes": "#7B2CBF",
        "aura": "#00F5D4",
    },
    "toxic-emerald": {
        "name": "Toxic Emerald",
        "body_primary": "#141D17",
        "body_secondary": "#0B110D",
        "body_highlight": "#25352A",
        "underbelly": "#1A261E",
        "accent": "#2BEE6C",
        "accent_glow": "#7DFFAB",
        "accent_dark": "#169440",
        "horns": "#0E1510",
        "horns_highlight": "#2D4735",
        "claws": "#D7FBE4",
        "claws_shadow": "#6CAE83",
        "eyes": "#A7F432",
        "pupil": "#050B07",
        "wing_bone": "#121A15",
        "wing_membrane": "#17231B",
        "wing_membrane_inner": "#223528",
        "armor": "#1C2D22",
        "armor_edge": "#3B6149",
        "spikes": "#101913",
        "aura": "#39FF14",
    },
    "solar-flare": {
        "name": "Solar Flare",
        "body_primary": "#241812",
        "body_secondary": "#140D0A",
        "body_highlight": "#3E2B20",
        "underbelly": "#2E1E17",
        "accent": "#FF7700",
        "accent_glow": "#FFAA4D",
        "accent_dark": "#B34A00",
        "horns": "#18100C",
        "horns_highlight": "#4B3226",
        "claws": "#FFE0CC",
        "claws_shadow": "#9E6D50",
        "eyes": "#FFCC00",
        "pupil": "#0C0705",
        "wing_bone": "#1E130E",
        "wing_membrane": "#271912",
        "wing_membrane_inner": "#38241A",
        "armor": "#332118",
        "armor_edge": "#6E4835",
        "spikes": "#1A100C",
        "aura": "#FF9E00",
    }
}

# Evolution stages thresholds and metadata
STAGE_DEFINITIONS = [
    {
        "id": "hatchling",
        "level": 1,
        "name": "Hatchling",
        "title": "Baby Dragon",
        "min_score": 0,
        "max_score": 49,
        "description": "Newly awakened hatchling with eager eyes, small horn buds, and budding wings.",
        "body_scale": 0.82,
        "horn_level": 1,
        "wing_level": 1,
        "spike_level": 0,
        "armor_level": 0,
        "tail_level": 1,
        "aura_enabled": False,
    },
    {
        "id": "young",
        "level": 2,
        "name": "Young Drake",
        "title": "Energetic Juvenile",
        "min_score": 50,
        "max_score": 149,
        "description": "Growing rapidly; developing distinct horn curves, strong claws, and lengthened tail.",
        "body_scale": 0.90,
        "horn_level": 2,
        "wing_level": 2,
        "spike_level": 1,
        "armor_level": 0,
        "tail_level": 2,
        "aura_enabled": False,
    },
    {
        "id": "adolescent",
        "level": 3,
        "name": "Adolescent Dragon",
        "title": "Fierce Skystriker",
        "min_score": 150,
        "max_score": 299,
        "description": "Muscular build emerging; dorsal spikes line the spine, wings span wider, markings glow brightly.",
        "body_scale": 0.98,
        "horn_level": 3,
        "wing_level": 3,
        "spike_level": 2,
        "armor_level": 1,
        "tail_level": 3,
        "aura_enabled": False,
    },
    {
        "id": "adult",
        "level": 4,
        "name": "Adult Wyrm",
        "title": "Battle-Tested Dragon",
        "min_score": 300,
        "max_score": 599,
        "description": "Powerful jaw, prominent sweeping horns, armor plating on shoulders, and broad leathery wings.",
        "body_scale": 1.06,
        "horn_level": 4,
        "wing_level": 4,
        "spike_level": 3,
        "armor_level": 2,
        "tail_level": 4,
        "aura_enabled": False,
    },
    {
        "id": "mature",
        "level": 5,
        "name": "Mature Dreadwyrm",
        "title": "Dominant Apex Predator",
        "min_score": 600,
        "max_score": 999,
        "description": "Heavy carapaces, secondary brow horns, reinforced tail blade, and blazing golden markings.",
        "body_scale": 1.13,
        "horn_level": 5,
        "wing_level": 5,
        "spike_level": 4,
        "armor_level": 3,
        "tail_level": 5,
        "aura_enabled": True,
    },
    {
        "id": "ancient",
        "level": 6,
        "name": "Ancient Leviathan",
        "title": "Elder Dragon Lord",
        "min_score": 1000,
        "max_score": 1999,
        "description": "Monolithic horns, double row of dorsal spikes, layered carapace armor, and radiating energy.",
        "body_scale": 1.19,
        "horn_level": 6,
        "wing_level": 6,
        "spike_level": 5,
        "armor_level": 4,
        "tail_level": 6,
        "aura_enabled": True,
    },
    {
        "id": "legendary",
        "level": 7,
        "name": "Legendary Titan",
        "title": "Mythic World-Eater",
        "min_score": 2000,
        "max_score": 999999,
        "description": "The pinnacle of draconic power. Enormous wings, transcendent golden crest, impenetrable armor, and cosmic aura.",
        "body_scale": 1.25,
        "horn_level": 7,
        "wing_level": 7,
        "spike_level": 6,
        "armor_level": 5,
        "tail_level": 7,
        "aura_enabled": True,
    },
]

# GitHub Activity Scoring Weights
DEFAULT_WEIGHTS = {
    "commit": 1.0,               # General progression
    "pull_request": 4.0,         # Horns & dorsal spikes
    "merged_pr": 6.0,            # Armor plating & carapace
    "issue": 2.0,                # Scale / armor complexity
    "review": 3.0,               # Wing span & membrane
    "repo": 5.0,                 # Tail & crest development
    "star_received": 1.5,        # Radiance & markings
    "streak_multiplier": 1.2,    # Multiplier bonus for active streaks
}

# Rolling Decay Weights
# Activities are grouped into time windows:
# 0-7 days (current week): 1.0
# 8-30 days (current month): 0.65
# 31-90 days (quarter): 0.35
# 91-365 days (year): 0.15
DECAY_WEIGHTS = {
    "recent_7d": 1.0,
    "month_30d": 0.65,
    "quarter_90d": 0.35,
    "year_365d": 0.15,
}

@dataclass
class DragoConfig:
    username: str = "octocat"
    palette_name: str = "obsidian-gold"
    custom_palette: Dict[str, str] = field(default_factory=dict)
    species: str = "action-dragon"
    fps: int = 12
    frame_count: int = 24
    width: int = 650
    height: int = 420
    supersample: int = 2  # 2x internal resolution for antialiasing
    weights: Dict[str, float] = field(default_factory=lambda: DEFAULT_WEIGHTS.copy())
    show_status_card: bool = True
    output_path: str = "assets/dragon.gif"
    status_card_path: str = "assets/dragon-status.svg"

    def get_palette(self) -> Dict[str, str]:
        base = PALETTES.get(self.palette_name, PALETTES["obsidian-gold"]).copy()
        if self.custom_palette:
            base.update(self.custom_palette)
        return base
