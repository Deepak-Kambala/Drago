"""
Status card generator for Drago.
Generates a crisp, responsive SVG companion card displaying evolution stage,
XP progress bar, unlocked draconic traits, and GitHub activity matrix.
"""

import os
from typing import Dict, Any
from drago.evolution import DragonState, GitHubActivity
from drago.config import DragoConfig

def generate_status_svg(state: DragonState, activity: GitHubActivity, config: DragoConfig, output_path: str = "assets/dragon-status.svg") -> str:
    palette = config.get_palette()
    accent = palette.get("accent", "#F5B700")
    accent_glow = palette.get("accent_glow", "#FFD13B")
    
    # Progress math
    pct = int(round(state.progress_to_next * 100))
    bar_width = int(round(state.progress_to_next * 280))
    
    next_info = f"Next: {state.next_stage_name} ({state.next_stage_score} XP)" if state.next_stage_name else "MAX EVOLUTION"
    aura_text = f"Active ({int(state.aura_intensity * 100)}%)" if state.aura_intensity > 0.05 else "Dormant"
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 180" width="650" height="180">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161B22" />
      <stop offset="100%" stop-color="#0D1117" />
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent}" />
      <stop offset="100%" stop-color="{accent_glow}" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background Card -->
  <rect x="1" y="1" width="648" height="178" rx="12" fill="url(#bgGrad)" stroke="#30363D" stroke-width="1.5" />

  <!-- Top Accent Bar -->
  <rect x="1" y="1" width="648" height="3" rx="1.5" fill="{accent}" />

  <!-- Stage Badge & Title -->
  <g transform="translate(24, 28)">
    <rect x="0" y="0" width="76" height="22" rx="4" fill="{accent}" fill-opacity="0.15" stroke="{accent}" stroke-width="1" />
    <text x="38" y="15" fill="{accent}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="11" font-weight="700" text-anchor="middle" letter-spacing="0.5">LVL {state.stage_level}</text>
    
    <text x="88" y="17" fill="#F0F6FC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="18" font-weight="700">{state.stage_name.upper()}</text>
    <text x="88" y="36" fill="#8B949E" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="12">{state.stage_title}</text>
  </g>

  <!-- Progress Bar & Score -->
  <g transform="translate(340, 28)">
    <text x="0" y="14" fill="#C9D1D9" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="12" font-weight="600">Evolution Power: <tspan fill="{accent}">{state.score:,.1f}</tspan></text>
    <text x="280" y="14" fill="#8B949E" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="11" text-anchor="end">{pct}%</text>
    
    <!-- Track -->
    <rect x="0" y="22" width="280" height="8" rx="4" fill="#21262D" />
    <!-- Filled Bar -->
    <rect x="0" y="22" width="{bar_width}" height="8" rx="4" fill="url(#barGrad)" filter="url(#glow)" />
    
    <text x="0" y="44" fill="#8B949E" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="10">{next_info}</text>
  </g>

  <!-- Divider Line -->
  <line x1="24" y1="84" x2="626" y2="84" stroke="#21262D" stroke-width="1" />

  <!-- Traits & Activity Metrics (2-column layout) -->
  <g transform="translate(24, 102)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
    <!-- Unlocked Traits Column -->
    <text x="0" y="12" fill="#8B949E" font-size="10" font-weight="700" letter-spacing="1">ANATOMICAL TRAITS</text>
    <text x="0" y="32" fill="#C9D1D9" font-size="12">Horns: <tspan fill="{accent}">Tier {state.horn_level}</tspan> • Wings: <tspan fill="{accent}">Tier {state.wing_level}</tspan></text>
    <text x="0" y="52" fill="#C9D1D9" font-size="12">Spikes: <tspan fill="{accent}">{state.dorsal_spike_count}</tspan> • Armor: <tspan fill="{accent}">Tier {state.armor_level}</tspan> • Streak Aura: <tspan fill="{accent}">{aura_text}</tspan></text>

    <!-- Activity Stats Column -->
    <text x="340" y="12" fill="#8B949E" font-size="10" font-weight="700" letter-spacing="1">GITHUB ACTIVITY</text>
    <text x="340" y="32" fill="#C9D1D9" font-size="12">Commits: <tspan fill="#F0F6FC" font-weight="600">{activity.total_commits:,}</tspan> • PRs: <tspan fill="#F0F6FC" font-weight="600">{activity.total_prs}</tspan> (Merged: <tspan fill="#F0F6FC" font-weight="600">{activity.merged_prs}</tspan>)</text>
    <text x="340" y="52" fill="#C9D1D9" font-size="12">Repos: <tspan fill="#F0F6FC" font-weight="600">{activity.public_repos}</tspan> • Stars: <tspan fill="#F0F6FC" font-weight="600">{activity.total_stars}</tspan> • Streak: <tspan fill="{accent}" font-weight="600">{activity.current_streak}d 🔥</tspan></text>
  </g>
</svg>
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg.strip())

    return output_path
