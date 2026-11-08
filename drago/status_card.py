"""
Clean, responsive SVG companion card for Drago.
Displays dynamic developer stats, evolution level, progress bar,
and core GitHub activity metrics in a sleek, minimalist card.
"""

import os
from typing import Optional
from drago.evolution import DragonState, GitHubActivity
from drago.config import DragoConfig

def generate_status_svg(
    state: DragonState,
    activity: GitHubActivity,
    config: DragoConfig,
    output_path: str = "assets/dragon-status.svg",
    username: Optional[str] = None,
) -> str:
    palette = config.get_palette()
    accent = palette.get("accent", "#F5B700")
    accent_glow = palette.get("accent_glow", "#FFD13B")
    
    # Dynamic username resolution
    user = username or getattr(config, "username", None) or "Developer"
    
    # Progress calculations
    pct = int(round(state.progress_to_next * 100))
    bar_width = max(6, int(round(state.progress_to_next * 602)))
    
    next_info = f"Next: {state.next_stage_name} ({state.next_stage_score} XP)" if state.next_stage_name else "★ MAX FORM"
    streak_label = f"{activity.current_streak} days" if activity.current_streak != 1 else "1 day"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 110" width="650" height="110">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161B22" />
      <stop offset="100%" stop-color="#0D1117" />
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" />
      <stop offset="100%" stop-color="{accent_glow}" />
    </linearGradient>
    <filter id="glow" x="-10%" y="-30%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="1" y="1" width="648" height="108" rx="10" fill="url(#bgGrad)" stroke="#30363D" stroke-width="1" />
  <rect x="1" y="1" width="648" height="2.5" rx="1" fill="{accent}" />

  <!-- Top Line: Stage Badge, Stage Name, User & XP -->
  <g transform="translate(24, 28)">
    <!-- Level Badge -->
    <rect x="0" y="0" width="54" height="20" rx="4" fill="{accent}" fill-opacity="0.15" stroke="{accent}" stroke-width="1" />
    <text x="27" y="14" fill="{accent}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="10" font-weight="700" text-anchor="middle" letter-spacing="0.5">LVL {state.stage_level}</text>

    <!-- Stage Name & Dynamic Username -->
    <text x="64" y="15" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
      <tspan fill="#F0F6FC" font-size="15" font-weight="700" letter-spacing="0.3">{state.stage_name.upper()}</tspan>
      <tspan dx="10" fill="#8B949E" font-size="12" font-weight="500">@{user}</tspan>
    </text>

    <!-- XP & Percentage -->
    <text x="602" y="15" fill="#C9D1D9" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" text-anchor="end">
      <tspan fill="{accent}">{state.score:,.1f}</tspan> XP <tspan fill="#8B949E" font-weight="400">({pct}%)</tspan>
    </text>
  </g>

  <!-- Full-Width Sleek Progress Bar -->
  <g transform="translate(24, 48)">
    <rect x="0" y="0" width="602" height="6" rx="3" fill="#21262D" />
    <rect x="0" y="0" width="{bar_width}" height="6" rx="3" fill="url(#barGrad)" filter="url(#glow)" />
  </g>

  <!-- Bottom Useful Metrics Row -->
  <g transform="translate(24, 82)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif">
    <!-- Streak -->
    <text x="0" y="0" fill="#8B949E" font-size="10" font-weight="600" letter-spacing="0.5">STREAK</text>
    <text x="0" y="16" fill="#F0F6FC" font-size="13" font-weight="700">🔥 {streak_label}</text>

    <!-- Evolution Power -->
    <text x="140" y="0" fill="#8B949E" font-size="10" font-weight="600" letter-spacing="0.5">EVOLUTION POWER</text>
    <text x="140" y="16" fill="{accent}" font-size="13" font-weight="700">⚡ {state.score:,.1f}</text>

    <!-- Commits -->
    <text x="290" y="0" fill="#8B949E" font-size="10" font-weight="600" letter-spacing="0.5">COMMITS</text>
    <text x="290" y="16" fill="#F0F6FC" font-size="13" font-weight="700">💻 {activity.total_commits:,}</text>

    <!-- Pull Requests -->
    <text x="430" y="0" fill="#8B949E" font-size="10" font-weight="600" letter-spacing="0.5">PULL REQUESTS</text>
    <text x="430" y="16" fill="#F0F6FC" font-size="13" font-weight="700">🔀 {activity.total_prs}</text>

    <!-- Next Unlock -->
    <text x="602" y="16" fill="#8B949E" font-size="10" font-weight="500" text-anchor="end">{next_info}</text>
  </g>
</svg>
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg.strip())

    return output_path
