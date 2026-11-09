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

# Evolution stages thresholds and metadata (Matching user's exact 13-stage progression)
STAGE_DEFINITIONS = [
    {
        "id": "egg",
        "level": 1,
        "name": "Egg",
        "title": "Dormant Dragon Egg",
        "min_score": 0,
        "max_score": 9,
        "sprite_file": "01_egg.png",
        "is_egg": True,
        "aura_enabled": False,
        "description": "An ancient obsidian dragon egg etched with dormant golden veins, awaiting developer activity.",
        "body_scale": 0.80,
        "horn_level": 0,
        "wing_level": 0,
        "spike_level": 0,
        "armor_level": 0,
        "tail_level": 0,
    },
    {
        "id": "hatchling",
        "level": 2,
        "name": "Hatchling",
        "title": "Freshly Hatched Drake",
        "min_score": 10,
        "max_score": 49,
        "sprite_file": "02_hatchling.png",
        "is_egg": False,
        "aura_enabled": False,
        "description": "A newly hatched dragon chick with eager amber eyes, small horns, and budding wings.",
        "body_scale": 0.85,
        "horn_level": 1,
        "wing_level": 1,
        "spike_level": 0,
        "armor_level": 0,
        "tail_level": 1,
    },
    {
        "id": "youngling",
        "level": 3,
        "name": "Youngling",
        "title": "Playful Young Drake",
        "min_score": 50,
        "max_score": 149,
        "sprite_file": "03_youngling.png",
        "is_egg": False,
        "aura_enabled": False,
        "description": "Growing rapidly, developing distinct horn curves, sharp claws, and a lengthened tail.",
        "body_scale": 0.90,
        "horn_level": 2,
        "wing_level": 2,
        "spike_level": 1,
        "armor_level": 0,
        "tail_level": 2,
    },
    {
        "id": "juvenile",
        "level": 4,
        "name": "Juvenile",
        "title": "Fierce Skystriker",
        "min_score": 150,
        "max_score": 299,
        "sprite_file": "04_juvenile.png",
        "is_egg": False,
        "aura_enabled": False,
        "description": "Athletic build emerging; dorsal spikes line the spine, wings span wider, gold stripes brighten.",
        "body_scale": 0.95,
        "horn_level": 3,
        "wing_level": 3,
        "spike_level": 2,
        "armor_level": 1,
        "tail_level": 3,
    },
    {
        "id": "adolescent",
        "level": 5,
        "name": "Adolescent",
        "title": "Rising Dragon Warrior",
        "min_score": 300,
        "max_score": 499,
        "sprite_file": "05_adolescent.png",
        "is_egg": False,
        "aura_enabled": False,
        "description": "Muscular build with sweeping horns and powerful limbs, ready to defend open source repositories.",
        "body_scale": 1.00,
        "horn_level": 4,
        "wing_level": 4,
        "spike_level": 3,
        "armor_level": 2,
        "tail_level": 4,
    },
    {
        "id": "adult",
        "level": 6,
        "name": "Adult",
        "title": "Battle-Tested Dragon",
        "min_score": 500,
        "max_score": 749,
        "sprite_file": "06_adult.png",
        "is_egg": False,
        "aura_enabled": False,
        "description": "Full adult form with imposing horns, heavy chest musculature, broad wings, and sharp ivory talons.",
        "body_scale": 1.06,
        "horn_level": 5,
        "wing_level": 5,
        "spike_level": 4,
        "armor_level": 3,
        "tail_level": 5,
    },
    {
        "id": "mature",
        "level": 7,
        "name": "Mature",
        "title": "Dominant Apex Predator",
        "min_score": 750,
        "max_score": 999,
        "sprite_file": "07_mature.png",
        "is_egg": False,
        "aura_enabled": False,
        "description": "Heavier scales, prominent shoulder plates, reinforced tail blade, and blazing golden markings.",
        "body_scale": 1.10,
        "horn_level": 6,
        "wing_level": 6,
        "spike_level": 5,
        "armor_level": 4,
        "tail_level": 6,
    },
    {
        "id": "ancient",
        "level": 8,
        "name": "Ancient",
        "title": "Elder Mountain Wyrm",
        "min_score": 1000,
        "max_score": 1499,
        "sprite_file": "08_ancient.png",
        "is_egg": False,
        "aura_enabled": True,
        "description": "Centuries of draconic power; multi-tiered horns, double rows of dorsal spikes, and thick carapace armor.",
        "body_scale": 1.14,
        "horn_level": 7,
        "wing_level": 7,
        "spike_level": 6,
        "armor_level": 5,
        "tail_level": 7,
    },
    {
        "id": "warlord",
        "level": 9,
        "name": "Warlord",
        "title": "Battlefield Overlord",
        "min_score": 1500,
        "max_score": 1999,
        "sprite_file": "09_warlord.png",
        "is_egg": False,
        "aura_enabled": True,
        "description": "Fierce armored champion with massive razor wings, jagged spine armor, and radiating golden power.",
        "body_scale": 1.18,
        "horn_level": 8,
        "wing_level": 8,
        "spike_level": 7,
        "armor_level": 6,
        "tail_level": 8,
    },
    {
        "id": "elder",
        "level": 10,
        "name": "Elder",
        "title": "Grand Elder Wyrm",
        "min_score": 2000,
        "max_score": 2499,
        "sprite_file": "10_elder.png",
        "is_egg": False,
        "aura_enabled": True,
        "description": "Ancient sovereign dragon wielding primordial knowledge and razor-sharp draconic crests.",
        "body_scale": 1.22,
        "horn_level": 9,
        "wing_level": 9,
        "spike_level": 8,
        "armor_level": 7,
        "tail_level": 9,
    },
    {
        "id": "dragon_lord",
        "level": 11,
        "name": "Dragon Lord",
        "title": "Sovereign of the Dragon Realm",
        "min_score": 2500,
        "max_score": 2999,
        "sprite_file": "11_dragon_lord.png",
        "is_egg": False,
        "aura_enabled": True,
        "description": "Supreme draconic ruler commanding massive golden wings, shoulder star emblems, and ground tremors.",
        "body_scale": 1.25,
        "horn_level": 10,
        "wing_level": 10,
        "spike_level": 9,
        "armor_level": 8,
        "tail_level": 10,
    },
    {
        "id": "celestial_dragon",
        "level": 12,
        "name": "Celestial Dragon",
        "title": "Starlight Ascendant",
        "min_score": 3000,
        "max_score": 3999,
        "sprite_file": "12_celestial_dragon.png",
        "is_egg": False,
        "aura_enabled": True,
        "description": "Ascended into cosmic glory with radiant glowing wings, floating star crystals, and celestial energy flames.",
        "body_scale": 1.28,
        "horn_level": 11,
        "wing_level": 11,
        "spike_level": 10,
        "armor_level": 9,
        "tail_level": 11,
    },
    {
        "id": "mythic_dragon",
        "level": 13,
        "name": "Mythic Dragon",
        "title": "Omnipotent Mythic God",
        "min_score": 4000,
        "max_score": 999999,
        "sprite_file": "13_mythic_dragon.png",
        "is_egg": False,
        "aura_enabled": True,
        "description": "The ultimate transcendent lifeform: blazing cosmic aura rings, orbiting energy crystals, and divine golden flame.",
        "body_scale": 1.32,
        "horn_level": 12,
        "wing_level": 12,
        "spike_level": 11,
        "armor_level": 10,
        "tail_level": 12,
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
    username: str = ""
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

