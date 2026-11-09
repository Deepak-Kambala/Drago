# Drago Technical & Developer Setup Guide

## About

Drago is an open-source, procedurally animated profile companion that translates GitHub activity into evolving visual assets. This document serves as the comprehensive technical reference for local developers, contributors, and advanced GitHub Actions configurations.

## Description

This guide covers:
- Complete local environment installation and dependency management.
- CLI command options (`render`, `update`, `simulate`, `preview-all`, `palettes`).
- Schema documentation for `drago.config.json` including dimensions, frame rates, and supersampling.
- Architecture internals across geometry, kinematics, asset rendering, and GitHub GraphQL / REST fetchers.
- Workflow permission setup for GitHub Actions automation.

---

## Table of Contents
- [1. GitHub Actions Permissions & Automation](#1-github-actions-permissions--automation)
- [2. Local Installation & Development](#2-local-installation--development)
- [3. CLI Tool Reference](#3-cli-tool-reference)
- [4. Configuration Reference (`drago.config.json`)](#4-configuration-reference-dragoconfigjson)
- [5. System Architecture & Rendering Pipeline](#5-system-architecture--rendering-pipeline)
- [6. Testing & Quality Assurance](#6-testing--quality-assurance)
- [7. Troubleshooting & FAQs](#7-troubleshooting--faqs)

---

## 1. GitHub Actions Permissions & Automation

Drago runs an automated GitHub Action (`.github/workflows/drago-update.yml`) every 15 minutes that queries GitHub's API for the user's latest contributions, evaluates the evolution score, re-renders the assets, and commits them.

### Workflow Permissions Setup
For GitHub Actions to push updated dragon assets back to your repository:

1. Navigate to your repository on GitHub.
2. Go to **Settings** $\rightarrow$ **Actions** $\rightarrow$ **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions**.
5. Check **Allow GitHub Actions to create and approve pull requests** (if prompted).
6. Click **Save**.

### Manual Trigger
You can test the workflow at any time without waiting for the scheduled 15-minute run:
1. Go to the **Actions** tab in your repository.
2. Select **Drago Evolution Update** in the left sidebar.
3. Click **Run workflow**, optionally specifying:
   - `username`: Target GitHub username (defaults to repository owner).
   - `force_stage`: Specific stage (1–13) to test rendering.

### Optional: Exact On-Time Scheduling via External Cron (e.g. cron-job.org)
GitHub Actions schedule crons can experience queuing delays during peak GitHub hours. If you want updates to execute at the exact second, you can trigger the workflow from an external service such as [cron-job.org](https://cron-job.org):

1. Generate a GitHub Personal Access Token (classic) with `repo` scope (**Settings** $\rightarrow$ **Developer Settings** $\rightarrow$ **Personal access tokens**).
2. In cron-job.org, click **Create cronjob** $\rightarrow$ **Import from cURL**, and paste:

```bash
curl -X POST "https://api.github.com/repos/YOUR_USERNAME/drago/dispatches" \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "User-Agent: Drago-Cron-Job" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"drago-update"}'
```

3. Set the schedule to **Every 15 minutes** and save.

---

## 2. Local Installation & Development

### Prerequisites
- Python 3.10 or higher
- `pip`

### Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/Deepak-Kambala/Drago.git
cd Drago

# Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install editable package
pip install -e .
```

---

## 3. CLI Tool Reference

Drago includes a complete CLI for rendering, simulation, and preview generation:

```bash
python3 -m drago.cli <command> [options]
```

### Available Commands

#### `render`
Renders an animation loop of Drago to GIF:
```bash
# Render specific stage (1–13) with specific palette
python3 -m drago.cli render --stage 4 --palette obsidian-gold --output assets/dragon.gif

# Render custom action (idle or roar)
python3 -m drago.cli render --stage 5 --action roar --output assets/dragon_roar.gif

# Render with simulated contribution numbers
python3 -m drago.cli render --commits 250 --prs 20 --merged-prs 15 --stars 40 --streak 10
```

#### `update`
Fetches live GitHub activity for a user and updates `assets/dragon.gif` and `assets/dragon-status.svg`:
```bash
# Update using personal access token (optional, increases rate limits)
python3 -m drago.cli update --username your-username --token GITHUB_TOKEN
```

#### `preview-all`
Generates animated preview GIFs for all 13 evolution phases into `assets/previews/`:
```bash
python3 -m drago.cli preview-all
```

#### `simulate`
Simulates GitHub activity over 60 days to test the rolling decay algorithm and score trajectory:
```bash
python3 -m drago.cli simulate
```

#### `palettes`
Lists all available color palettes and their hex codes:
```bash
python3 -m drago.cli palettes
```

---

## 4. Configuration Reference (`drago.config.json`)

Customize Drago's behavior by editing `drago.config.json`:

```json
{
  "username": "",
  "palette_name": "obsidian-gold",
  "species": "action-dragon",
  "fps": 12,
  "frame_count": 24,
  "width": 650,
  "height": 420,
  "supersample": 2,
  "background": "github-dark",
  "show_status_card": true,
  "output_path": "assets/dragon.gif",
  "status_card_path": "assets/dragon-status.svg",
  "weights": {
    "commit": 1.0,
    "pull_request": 4.0,
    "merged_pr": 6.0,
    "issue": 2.0,
    "repo": 5.0,
    "star_received": 1.5,
    "streak_multiplier": 1.2
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `username` | `string` | *(repo owner)* | Target GitHub username to track |
| `palette_name` | `string` | `"obsidian-gold"` | Color theme: `obsidian-gold`, `crimson-fury`, `arctic-frost`, `cyberpunk-neon`, `toxic-emerald`, `solar-flare` |
| `species` | `string` | `"action-dragon"` | Dragon anatomy model (`action-dragon`) |
| `fps` | `integer` | `12` | Frame rate of the generated GIF |
| `frame_count` | `integer` | `24` | Total animation frames per loop (2.0s loop cycle) |
| `width` | `integer` | `650` | Output GIF width in pixels (standard GitHub README width) |
| `height` | `integer` | `420` | Output GIF height in pixels |
| `supersample` | `integer` | `2` | Internal rendering scale (2x with Lanczos resampling for anti-aliasing) |
| `background` | `string` | `"github-dark"` | Canvas background (`github-dark` `#0D1117` or `transparent`) |
| `show_status_card` | `boolean` | `true` | Generate companion `assets/dragon-status.svg` |
| `weights` | `object` | `{...}` | Multipliers applied to raw GitHub metrics |

---

## 5. System Architecture & Rendering Pipeline

Drago is architected with clear separation of concerns:

```text
drago/
├── config.py         # Configuration loader, palette definitions, and dimension settings
├── evolution.py      # XP scoring, rolling time-decay engine, and 13-stage threshold mapper
├── geometry.py       # Bezier curves, polygon transforms, ribbon math, and color gradients
├── anatomy.py        # Cel-shaded 2D vector cartoon dragon anatomy and sprite compositor
├── animator.py       # Skeletal kinematics for breathing, blinking, wing flutters, and tail swaying
├── renderer.py       # Supersampled rendering canvas, ambient lighting, and GIF encoder
├── github_fetcher.py # Live GraphQL / REST GitHub contribution statistics fetcher
├── status_card.py    # Chamfered cyberpunk companion status card SVG generator
└── cli.py            # Unified command-line interface
```

### Evolution Math
Score calculations combine immediate activity with long-term wisdom:
$$\text{Score} = \left( \text{Recent}_{7\text{d}} \times 1.0 + \text{Mid}_{30\text{d}} \times 0.6 + \text{Lifetime} \times 0.3 \right) \times (1.0 + \text{Streak Bonus})$$

- **Streaks** provide up to a $+35\%$ multiplier.
- **Lifetime wisdom** guarantees you retain 30% of your progress permanently.

---

## 6. Testing & Quality Assurance

Run the comprehensive unit test suite:

```bash
python3 -m unittest discover tests
```

Tests validate:
- **Geometry & Curves**: Bezier evaluation and polygon offsets
- **Evolution Engine**: Stage threshold transitions, streak bonuses, and decay curves
- **Renderer**: GIF generation, frame dimensions, and palette application
- **Status Card**: SVG XML validity, dynamic XP calculations, and responsive tags

---

## 7. Troubleshooting & FAQs

### Why does my forked Drago show the original repository stats/dragon initially?
When you fork Drago, your fork inherits the initial committed assets until your GitHub Actions workflow runs for the first time. GitHub disables Actions on forks by default:
1. Go to your fork's **Actions** tab and click **I understand my workflows, go ahead and enable them**.
2. Click **Drago Evolution Update** in the left sidebar, click **Run workflow**, and run it once.
3. This immediately evaluates your real GitHub activity and commits your personalized dragon and status card to your fork.

### Why is my dragon not updating on my profile?
GitHub aggressively caches image assets via its `camo.githubusercontent.com` proxy.
- Allow up to 10–15 minutes for the GitHub proxy cache to expire after a commit.
- Alternatively, you can append a timestamp or commit hash query parameter to the URL in your README.

### GitHub Actions fails with "Permission denied to github-actions[bot]"
Ensure you have enabled **Read and write permissions** under **Repository Settings $\rightarrow$ Actions $\rightarrow$ General $\rightarrow$ Workflow permissions**.

### Can I run Drago for private contributions?
Yes! In your GitHub profile settings (**Public profile**), check **Include private contributions on my profile**. Additionally, you can pass a Personal Access Token (`PAT`) with the `repo` scope to the workflow.

