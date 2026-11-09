"""
Command line interface for Drago.
Provides rendering, GitHub activity updating, simulation, preview generation,
and palette management.
"""

import os
import sys
import re
import json
import argparse
import subprocess
from typing import Optional, Tuple
from PIL import Image

from drago.config import DragoConfig, PALETTES, STAGE_DEFINITIONS
from drago.evolution import EvolutionEngine, GitHubActivity, DragonState
from drago.animator import DragonAnimator
from drago.renderer import DragonRenderer
from drago.status_card import generate_status_svg
from drago.github_fetcher import GitHubFetcher

def resolve_username(args_username: Optional[str] = None, config_username: Optional[str] = None) -> Tuple[Optional[str], str]:
    """
    Dynamically and robustly resolves the GitHub username to evaluate.
    Returns: (username, source_description)

    Priority order:
    1. Explicit CLI argument (--username <user>)
    2. Environment variable: TARGET_USER
    3. Environment variable: GITHUB_REPOSITORY_OWNER (set automatically by GitHub Actions)
    4. GITHUB_REPOSITORY environment variable (extracting owner from "owner/repo")
    5. Config file username (if set, non-empty, and not a placeholder like 'octocat')
    6. Git remote origin URL parsing (e.g. from git@github.com:owner/repo or https://github.com/owner/repo)
    """
    if args_username and args_username.strip():
        return args_username.strip(), "CLI argument (--username)"

    env_target = os.environ.get("TARGET_USER")
    if env_target and env_target.strip():
        return env_target.strip(), "TARGET_USER environment variable"

    gh_owner = os.environ.get("GITHUB_REPOSITORY_OWNER")
    if gh_owner and gh_owner.strip():
        return gh_owner.strip(), "GITHUB_REPOSITORY_OWNER environment variable"

    gh_repo = os.environ.get("GITHUB_REPOSITORY")
    if gh_repo and "/" in gh_repo:
        parts = gh_repo.split("/")
        if parts[0].strip():
            return parts[0].strip(), "GITHUB_REPOSITORY environment variable"

    if config_username and config_username.strip():
        cleaned = config_username.strip()
        if cleaned.lower() not in ("octocat", "your_username", "placeholder"):
            return cleaned, "drago.config.json"

    try:
        origin = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        m = re.search(r"github\.com[:/]([^/]+)/", origin)
        if m and m.group(1).strip():
            return m.group(1).strip(), "git remote origin URL"
    except Exception:
        pass

    return None, "none"

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
        card_user, _ = resolve_username(
            getattr(args, "username", None) or getattr(args, "user", None),
            cfg.username
        )
        generate_status_svg(state, activity, cfg, cfg.status_card_path, username=card_user or "Developer")
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

def render_user_dragon(
    username: str,
    palette_name: Optional[str] = None,
    cfg: Optional[DragoConfig] = None,
    token: Optional[str] = None,
    output_dir: str = "assets",
    is_primary: bool = False,
):
    """Renders all dragon assets (GIF, SVG status card, JSON state) for a specific user."""
    if cfg is None:
        cfg = load_config()

    if palette_name and palette_name in PALETTES:
        cfg.palette_name = palette_name

    os.makedirs(output_dir, exist_ok=True)
    out_gif = os.path.join(output_dir, "dragon.gif")
    out_svg = os.path.join(output_dir, "dragon-status.svg")
    out_state = os.path.join(output_dir, "drago-state.json")

    print(f"\n🐉 RENDERING DRAGON FOR: {username} (Palette: {cfg.palette_name})")
    print(f"==========================================")

    fetcher = GitHubFetcher(token=token)
    try:
        activity = fetcher.fetch_activity(username)
    except Exception as e:
        print(f"[Drago] Error fetching GitHub activity for {username}: {e}")
        print(f"[Drago] Using base starter activity...")
        activity = GitHubActivity(total_commits=10, public_repos=1, total_stars=0, current_streak=1)

    engine = EvolutionEngine()
    state = engine.evaluate(activity)

    print(f"Stage:       Level {state.stage_level} - {state.stage_name} ({state.stage_title})")
    print(f"Score:       {state.score} (Raw: {state.raw_score})")
    print(f"Activity:    Commits: {activity.total_commits}, PRs: {activity.total_prs} (Merged: {activity.merged_prs}), Repos: {activity.public_repos}, Stars: {activity.total_stars}, Streak: {activity.current_streak}d")

    renderer = DragonRenderer(cfg, state)
    frames = renderer.render_animation(action="idle")
    renderer.save_gif(frames, out_gif, fps=cfg.fps)
    print(f"GIF Asset:   {out_gif}")

    if cfg.show_status_card:
        generate_status_svg(state, activity, cfg, out_svg, username=username)
        print(f"Status Card: {out_svg}")

    summary = {
        "username": username,
        "palette": cfg.palette_name,
        "stage_level": state.stage_level,
        "stage_name": state.stage_name,
        "score": state.score,
        "progress": state.progress_to_next,
        "asset_path": out_gif,
    }
    with open(out_state, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    if is_primary and output_dir != "assets":
        import shutil
        os.makedirs("assets", exist_ok=True)
        shutil.copyfile(out_gif, "assets/dragon.gif")
        shutil.copyfile(out_svg, "assets/dragon-status.svg")
        shutil.copyfile(out_state, "assets/drago-state.json")

    return state, activity

def cmd_update(args):
    """Production GitHub Actions runner command for a single user."""
    cfg = load_config(args.config)
    username, source = resolve_username(args.username, cfg.username)
    if not username:
        print("[Drago] Error: GitHub username not detected.")
        print("[Drago] Please pass --username <user>, set TARGET_USER or GITHUB_REPOSITORY_OWNER env, or set 'username' in drago.config.json.")
        sys.exit(1)

    print(f"Target User: {username} (resolved via {source})")
    render_user_dragon(
        username=username,
        cfg=cfg,
        token=args.token,
        output_dir="assets",
        is_primary=True,
    )
    print(f"✅ Drago updated successfully for {username}!\n")

def cmd_register(args):
    """Registers a new user in the Central Hub and renders their initial dragon."""
    username = (args.username or "").strip()
    if not username:
        print("[Drago] Error: Username required for registration. Pass --username <user>.")
        sys.exit(1)

    palette = args.palette or "obsidian-gold"
    registry_file = getattr(args, "registry", "registered_users.json")

    users = []
    if os.path.exists(registry_file):
        try:
            with open(registry_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            users.append({"username": item, "palette": "obsidian-gold"})
                        elif isinstance(item, dict) and "username" in item:
                            users.append(item)
        except Exception as e:
            print(f"[Drago] Warning: failed to parse {registry_file}: {e}")

    # Check if already registered
    found = False
    for u in users:
        if u["username"].lower() == username.lower():
            u["palette"] = palette
            found = True
            break

    if not found:
        users.append({"username": username, "palette": palette})

    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
    print(f"✅ Registered '{username}' in {registry_file} (Palette: {palette})")

    repo_owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "Deepak-Kambala")
    is_owner = (username.lower() == repo_owner.lower())

    user_dir = f"assets/users/{username}"
    render_user_dragon(
        username=username,
        palette_name=palette,
        token=args.token,
        output_dir=user_dir,
        is_primary=is_owner,
    )
    print(f"\n🎉 Successfully created dragon for {username}!")
    print(f"Embed in profile README:")
    print(f'<img src="https://raw.githubusercontent.com/{repo_owner}/Drago/main/{user_dir}/dragon.gif" width="650">')
    print(f'<img src="https://raw.githubusercontent.com/{repo_owner}/Drago/main/{user_dir}/dragon-status.svg" width="650">\n')

def cmd_update_all(args):
    """Central Hub runner: updates all registered users in registered_users.json."""
    registry_file = getattr(args, "registry", "registered_users.json")
    if not os.path.exists(registry_file):
        print(f"[Drago] Registry file {registry_file} not found. Nothing to update.")
        return

    with open(registry_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    users = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                users.append({"username": item, "palette": "obsidian-gold"})
            elif isinstance(item, dict) and "username" in item:
                users.append(item)

    repo_owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "Deepak-Kambala")
    print(f"\n🐉 DRAGO CENTRAL HUB: UPDATING ALL {len(users)} REGISTERED USERS")
    print(f"============================================================")

    for idx, user_info in enumerate(users):
        uname = user_info["username"]
        pal = user_info.get("palette", "obsidian-gold")
        print(f"\n[{idx+1}/{len(users)}] Updating {uname} ({pal})...")
        is_owner = (uname.lower() == repo_owner.lower())
        try:
            render_user_dragon(
                username=uname,
                palette_name=pal,
                token=args.token,
                output_dir=f"assets/users/{uname}",
                is_primary=is_owner,
            )
        except Exception as e:
            print(f"[Drago] Error updating {uname}: {e}. Skipping to next user...")

    print(f"\n✅ All {len(users)} registered users updated successfully!\n")

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
    p_render.add_argument("--username", help="GitHub username for status card")
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

    # register (Central Hub)
    p_reg = subparsers.add_parser("register", help="Register user and render their dragon in Central Hub")
    p_reg.add_argument("--username", required=True, help="GitHub username to register")
    p_reg.add_argument("--palette", choices=list(PALETTES.keys()), default="obsidian-gold", help="Dragon color palette")
    p_reg.add_argument("--registry", default="registered_users.json", help="Path to registry JSON file")
    p_reg.add_argument("--token", help="GitHub API Token (or GITHUB_TOKEN env)")

    # update-all (Central Hub)
    p_upall = subparsers.add_parser("update-all", help="Update all registered user dragons in Central Hub")
    p_upall.add_argument("--registry", default="registered_users.json", help="Path to registry JSON file")
    p_upall.add_argument("--token", help="GitHub API Token (or GITHUB_TOKEN env)")
    p_upall.add_argument("--config", default="drago.config.json", help="Path to config file")

    # palettes
    subparsers.add_parser("palettes", help="List available color palettes")

    args = parser.parse_args()
    if args.command == "render":
        cmd_render(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "register":
        cmd_register(args)
    elif args.command == "update-all":
        cmd_update_all(args)
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

