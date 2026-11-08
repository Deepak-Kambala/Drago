"""
Command line interface for Drago.
Provides rendering, GitHub activity updating, simulation, preview generation,
and palette management.
"""

import os
import sys
import json
import argparse
from typing import Optional
from PIL import Image

from drago.config import DragoConfig, PALETTES, STAGE_DEFINITIONS
from drago.evolution import EvolutionEngine, GitHubActivity, DragonState
from drago.animator import DragonAnimator
from drago.renderer import DragonRenderer
from drago.status_card import generate_status_svg
from drago.github_fetcher import GitHubFetcher

def load_config(config_path: str = "drago.config.json") -> DragoConfig:
    cfg = DragoConfig()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                if hasattr(cfg, k):
                    setattr(cfg, k, v)
        except Exception as e:
            print(f"[Drago] Warning: failed to parse {config_path}: {e}")
    return cfg

def cmd_render(args):
    cfg = load_config(args.config)
    if args.palette:
        cfg.palette_name = args.palette
    if args.output:
        cfg.output_path = args.output
    if args.fps:
        cfg.fps = args.fps
    if args.frames:
        cfg.frame_count = args.frames

    engine = EvolutionEngine()

    # Determine activity: either simulated stage or custom counts
    if args.stage:
        stage_idx = max(0, min(len(STAGE_DEFINITIONS) - 1, int(args.stage) - 1))
        st_def = STAGE_DEFINITIONS[stage_idx]
        target_score = st_def["min_score"] + (10 if st_def["min_score"] > 0 else 5)
        activity = GitHubActivity(
            total_commits=target_score,
            recent_commits_7d=target_score,
            commits_30d=target_score,
            total_prs=int(stage_idx * 2),
            merged_prs=int(stage_idx),
            public_repos=int(1 + stage_idx),
            total_stars=int(stage_idx * 5),
            current_streak=7 if st_def.get("aura_enabled", False) else 2,
        )
    else:
        activity = GitHubActivity(
            total_commits=args.commits,
            recent_commits_7d=args.recent_commits,
            total_prs=args.prs,
            merged_prs=args.merged_prs,
            public_repos=args.repos,
            total_stars=args.stars,
            current_streak=args.streak,
        )

    state = engine.evaluate(activity)
    print(f"\n🐉 DRAGO RENDERING ENGINE")
    print(f"==========================================")
    print(f"Stage:       Level {state.stage_level} - {state.stage_name} ({state.stage_title})")
    print(f"Score:       {state.score} (Raw: {state.raw_score})")
    print(f"Horns:       Tier {state.horn_level} | Wings: Tier {state.wing_level} | Spikes: {state.dorsal_spike_count}")
    print(f"Armor:       Tier {state.armor_level} | Aura: {state.aura_intensity}")
    print(f"Palette:     {cfg.palette_name}")
    print(f"Action:      {args.action}")
    print(f"Output:      {cfg.output_path}")

    renderer = DragonRenderer(cfg, state)
    frames = renderer.render_animation(action=args.action, custom_frames=cfg.frame_count)
    out_gif = renderer.save_gif(frames, cfg.output_path, fps=cfg.fps)
    
    if cfg.show_status_card:
        generate_status_svg(state, activity, cfg, cfg.status_card_path)
        print(f"Status card: {cfg.status_card_path}")

    print(f"✅ Successfully rendered animated dragon to {out_gif} ({len(frames)} frames @ {cfg.fps} FPS)\n")

def cmd_preview_all(args):
    """Generates preview GIFs and a composite showcase strip for all 7 evolution stages."""
    cfg = load_config(args.config)
    if args.palette:
        cfg.palette_name = args.palette

    engine = EvolutionEngine()
    preview_dir = "assets/previews"
    os.makedirs(preview_dir, exist_ok=True)

    print(f"\n🐉 GENERATING PREVIEWS FOR ALL {len(STAGE_DEFINITIONS)} EVOLUTION FORMS...")
    print(f"============================================================")

    strip_images = []
    
    for i, st_def in enumerate(STAGE_DEFINITIONS):
        target_score = st_def["min_score"] + (10 if st_def["min_score"] > 0 else 5)
        activity = GitHubActivity(
            total_commits=target_score,
            recent_commits_7d=target_score,
            commits_30d=target_score,
            total_prs=int(i * 2),
            merged_prs=int(i),
            public_repos=int(1 + i),
            total_stars=int(i * 5),
            current_streak=7 if st_def.get("aura_enabled", False) else 2,
        )
        state = engine.evaluate(activity)
        out_path = f"{preview_dir}/stage_{i+1}_{st_def['id']}.gif"
        
        renderer = DragonRenderer(cfg, state)
        frames = renderer.render_animation(action="idle", custom_frames=18)
        renderer.save_gif(frames, out_path, fps=12)
        print(f"  [Lvl {i+1}] {st_def['name']:<20} -> {out_path}")
        
        # Capture frame 0 for composite strip
        strip_images.append(frames[0])

    # Build composite showcase image (grid of 4 columns)
    cols = 4
    rows = (len(strip_images) + cols - 1) // cols
    cell_w = 325
    cell_h = 210
    total_w = cell_w * cols
    total_h = cell_h * rows
    showcase = Image.new("RGBA", (total_w, total_h), (13, 17, 23, 255))
    
    for idx, img in enumerate(strip_images):
        c = idx % cols
        r = idx // cols
        scaled_cell = img.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        showcase.paste(scaled_cell, (c * cell_w, r * cell_h))

    showcase_path = "assets/evolution_showcase.png"
    showcase.save(showcase_path)
    print(f"\n✅ All {len(STAGE_DEFINITIONS)} stages rendered! Composite showcase: {showcase_path}\n")

def cmd_simulate(args):
    """Simulates activity progression and decaying over time."""
    engine = EvolutionEngine()
    print("\n🐉 DRAGO EVOLUTION SIMULATOR")
    print("==================================================")
    scenarios = [
        ("New Contributor (Day 1)", GitHubActivity(total_commits=15, total_prs=1, current_streak=1)),
        ("Active Open Sourcer", GitHubActivity(total_commits=180, total_prs=22, merged_prs=18, public_repos=8, total_stars=45, current_streak=9)),
        ("Senior Developer", GitHubActivity(total_commits=650, total_prs=75, merged_prs=62, public_repos=16, total_stars=180, current_streak=18)),
        ("Legendary Maintainer", GitHubActivity(total_commits=2400, total_prs=320, merged_prs=290, public_repos=35, total_stars=1200, current_streak=45)),
        ("Inactive Veteran (Decay Test)", GitHubActivity(total_commits=1200, recent_commits_7d=0, commits_30d=2, total_prs=100, merged_prs=85, public_repos=20, total_stars=500, current_streak=0)),
    ]

    for title, act in scenarios:
        state = engine.evaluate(act)
        print(f"\nScenario: {title}")
        print(f"  Score:       {state.score} (Raw: {state.raw_score})")
        print(f"  Form:        Level {state.stage_level} - {state.stage_name}")
        print(f"  Anatomy:     Scale: {state.body_scale:.2f}x | Horns: Tier {state.horn_level} | Wings: Tier {state.wing_level} | Spikes: {state.dorsal_spike_count} | Armor: Tier {state.armor_level}")
        print(f"  Streak Aura: {state.aura_intensity * 100:.0f}%")

def cmd_update(args):
    """Production GitHub Actions runner command."""
    cfg = load_config(args.config)
    username = args.username or cfg.username
    if not username:
        print("[Drago] Error: GitHub username not specified. Set in drago.config.json or pass --username.")
        sys.exit(1)

    print(f"\n🐉 DRAGO GITHUB UPDATE WORKFLOW")
    print(f"==========================================")
    print(f"User:        {username}")

    fetcher = GitHubFetcher(token=args.token)
    try:
        activity = fetcher.fetch_activity(username)
    except Exception as e:
        print(f"[Drago] Error fetching GitHub activity: {e}")
        print("[Drago] Using fallback base activity...")
        activity = GitHubActivity(total_commits=100, public_repos=5, total_stars=10, current_streak=3)

    engine = EvolutionEngine()
    state = engine.evaluate(activity)

    print(f"Stage:       Level {state.stage_level} - {state.stage_name} ({state.stage_title})")
    print(f"Score:       {state.score} (Raw: {state.raw_score})")
    print(f"Traits:      Horns T{state.horn_level}, Wings T{state.wing_level}, Spikes {state.dorsal_spike_count}, Armor T{state.armor_level}")
    print(f"Activity:    Commits: {activity.total_commits}, PRs: {activity.total_prs} (Merged: {activity.merged_prs}), Repos: {activity.public_repos}, Stars: {activity.total_stars}, Streak: {activity.current_streak}d")

    renderer = DragonRenderer(cfg, state)
    frames = renderer.render_animation(action="idle")
    out_gif = renderer.save_gif(frames, cfg.output_path, fps=cfg.fps)
    print(f"GIF Asset:   {out_gif}")

    if cfg.show_status_card:
        card_path = generate_status_svg(state, activity, cfg, cfg.status_card_path)
        print(f"Status Card: {card_path}")

    # Output machine-readable JSON summary for GitHub Actions if requested
    summary = {
        "username": username,
        "stage_level": state.stage_level,
        "stage_name": state.stage_name,
        "score": state.score,
        "progress": state.progress_to_next,
        "asset_path": out_gif,
    }
    with open("assets/drago-state.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Drago updated successfully!\n")

def cmd_palettes(args):
    print("\n🎨 AVAILABLE COLOR PALETTES:")
    print("==========================================")
    for k, v in PALETTES.items():
        print(f"  • {k:<18} : {v['name']}")
        print(f"      Body: {v['body_primary']} | Accent: {v['accent']} | Eyes: {v['eyes']}")

def main():
    parser = argparse.ArgumentParser(description="Drago - Animated GitHub Profile Dragon")
    subparsers = parser.add_subparsers(dest="command")

    # render
    p_render = subparsers.add_parser("render", help="Render dragon animation")
    p_render.add_argument("--config", default="drago.config.json", help="Path to config file")
    p_render.add_argument("--stage", type=int, choices=range(1, 14), help="Evolution stage (1-13)")
    p_render.add_argument("--palette", choices=list(PALETTES.keys()), help="Color palette")
    p_render.add_argument("--action", choices=["idle", "roar"], default="idle", help="Animation action")
    p_render.add_argument("--output", default="assets/dragon.gif", help="Output GIF path")
    p_render.add_argument("--fps", type=int, help="Frames per second")
    p_render.add_argument("--frames", type=int, help="Total frame count")
    p_render.add_argument("--commits", type=int, default=150)
    p_render.add_argument("--recent-commits", type=int, default=25)
    p_render.add_argument("--prs", type=int, default=15)
    p_render.add_argument("--merged-prs", type=int, default=10)
    p_render.add_argument("--repos", type=int, default=8)
    p_render.add_argument("--stars", type=int, default=30)
    p_render.add_argument("--streak", type=int, default=5)

    # update
    p_update = subparsers.add_parser("update", help="Fetch GitHub activity and update assets")
    p_update.add_argument("--username", help="GitHub username")
    p_update.add_argument("--token", help="GitHub API Token (or GITHUB_TOKEN env)")
    p_update.add_argument("--config", default="drago.config.json", help="Path to config file")

    # preview-all
    p_prev = subparsers.add_parser("preview-all", help="Generate previews for all 7 evolution forms")
    p_prev.add_argument("--config", default="drago.config.json")
    p_prev.add_argument("--palette", choices=list(PALETTES.keys()))

    # simulate
    subparsers.add_parser("simulate", help="Run evolution engine simulations")

    # palettes
    subparsers.add_parser("palettes", help="List available color palettes")

    args = parser.parse_args()
    if args.command == "render":
        cmd_render(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "preview-all":
        cmd_preview_all(args)
    elif args.command == "simulate":
        cmd_simulate(args)
    elif args.command == "palettes":
        cmd_palettes(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

