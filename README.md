<p align="center">
  <img src="./assets/dragon.gif" width="650" alt="Drago - Animated GitHub Profile Dragon">
</p>

<p align="center">
  <img src="./assets/dragon-status.svg" width="650" alt="Drago Evolution Status Card">
</p>

<p align="center">
  <strong>An animated dragon living in your GitHub README that breathes, blinks, and evolves from your real GitHub coding activity.</strong>
</p>

<p align="center">
  <a href="#quick-setup-60-seconds"><img src="https://img.shields.io/badge/Setup-60_Seconds-2EA043?style=flat-square" alt="Quick Setup"></a>
  <a href="#evolution-tiers"><img src="https://img.shields.io/badge/Evolution-13_Tiers-00D2FF?style=flat-square" alt="Evolution Stages"></a>
  <a href="#about"><img src="https://img.shields.io/badge/About-Drago-F5B700?style=flat-square" alt="About Drago"></a>
  <a href="#how-it-works"><img src="https://img.shields.io/badge/Architecture-Autonomous-orange?style=flat-square" alt="Autonomous"></a>
  <a href="#color-palettes"><img src="https://img.shields.io/badge/Palettes-6_Styles-8957E5?style=flat-square" alt="Palettes"></a>
  <a href="SETUP.md"><img src="https://img.shields.io/badge/Technical_Docs-SETUP.md-blue?style=flat-square" alt="Technical Docs"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-gray?style=flat-square" alt="License"></a>
</p>

---

## Quick Setup (30 Seconds)

Add your evolving dragon to your GitHub Profile README:

### Option A: Central Hub (Recommended - No Forking Required)

No need to fork or configure GitHub Actions. We generate and host your evolving dragon automatically:

1. **Register your Profile (Zero Code)**:
   Comment `/register` on the **[Pinned Registration Issue (#2)](https://github.com/Deepak-Kambala/Drago/issues/2)** (or submit a 1-click issue via **[Register My Dragon](https://github.com/Deepak-Kambala/Drago/issues/new?template=register.yml)**).
2. **Instant Generation**:
   Within 30 seconds, Drago's automated bot evaluates your GitHub contributions, generates your personal dragon, comments with your embed link, and closes the issue.
3. **Embed in your Profile README** (`<username>/<username>`):
   Paste this snippet into your profile `README.md` (replace `YOUR_USERNAME` with your GitHub username):

```markdown
<p align="center">
  <img src="https://raw.githubusercontent.com/Deepak-Kambala/Drago/main/assets/users/YOUR_USERNAME/dragon.gif" width="650" alt="My Evolving Dragon">
  <br>
  <img src="https://raw.githubusercontent.com/Deepak-Kambala/Drago/main/assets/users/YOUR_USERNAME/dragon-status.svg" width="650" alt="Drago Status Card">
</p>
```

> [!TIP]
> Your dragon automatically updates every 15 minutes as you push commits, merge pull requests, and maintain coding streaks. Zero maintenance required.

---

### Option B: The Independent Fork Way

If you prefer hosting and running the GitHub Action inside your own forked repository:

1. **Fork this repository** to your GitHub account (keep the default name `drago`).
2. **Enable Workflow Write Permissions**:
   - In your forked repository, go to **Settings** > **Actions** > **General**.
   - Under **Workflow permissions**, choose **Read and write permissions** and click **Save**.
3. **Enable and Run GitHub Actions**:
   - Go to the **Actions** tab in your repository.
   - Click the green button: **I understand my workflows, go ahead and enable them**.
   - Click **Drago Evolution Update** in the left sidebar, click **Run workflow**, and click the green **Run workflow** button.
4. **Embed in your Profile README** (`<username>/<username>`):
   Paste this snippet into your profile `README.md` (replace `YOUR_USERNAME` with your GitHub username):

```markdown
<p align="center">
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/drago/main/assets/dragon.gif" width="650" alt="My Evolving Dragon">
  <br>
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/drago/main/assets/dragon-status.svg" width="650" alt="Drago Status Card">
</p>
```

> [!IMPORTANT]
> **Do not open a Pull Request back to this repository.** Your forked repository is completely independent. Once Actions runs in your fork, your assets are already live in your repository and ready to display.

---

### Option C: Directly Inside Your Profile Repository

If you prefer keeping everything consolidated inside your existing `<username>/<username>` profile repository:

1. Copy the `drago/`, `.github/`, and `drago.config.json` files directly into your profile repository root.
2. Ensure **Read and write permissions** are enabled (**Settings** > **Actions** > **General** > **Workflow permissions**).
3. Add this relative snippet to your profile `README.md`:

```markdown
<p align="center">
  <img src="./assets/dragon.gif" width="650" alt="My Evolving Dragon">
  <br>
  <img src="./assets/dragon-status.svg" width="650" alt="Drago Status Card">
</p>
```

---

## Evolution Tiers

Drago progresses through **13 distinct evolutionary forms** based on your GitHub activity:

| Level | Stage | XP Threshold | Distinct Traits | Animation Preview |
|:---:|:---|:---:|:---|:---:|
| **1** | **Egg** | `0 – 9` | Obsidian shell with golden magma veins & inner heartbeat pulse | <img src="./assets/previews/stage_1_egg.gif" width="130" alt="Egg"> |
| **2** | **Hatchling** | `10 – 49` | Small compact wings, horn buds, eager amber eyes | <img src="./assets/previews/stage_2_hatchling.gif" width="130" alt="Hatchling"> |
| **3** | **Youngling** | `50 – 149` | Curved horns, lengthened tail, sharp ivory talons | <img src="./assets/previews/stage_3_youngling.gif" width="130" alt="Youngling"> |
| **4** | **Juvenile** | `150 – 299` | Athletic build, dorsal spines, wider wingspan, glowing markings | <img src="./assets/previews/stage_4_juvenile.gif" width="130" alt="Juvenile"> |
| **5** | **Adolescent** | `300 – 499` | Muscular limbs, sweeping battle horns, battle stance | <img src="./assets/previews/stage_5_adolescent.gif" width="130" alt="Adolescent"> |
| **6** | **Adult** | `500 – 799` | Broad wingspan, heavy chest musculature, imposing silhouette | <img src="./assets/previews/stage_6_adult.gif" width="130" alt="Adult"> |
| **7** | **Mature** | `800 – 1199` | Shoulder carapaces, reinforced tail blade, golden flank markings | <img src="./assets/previews/stage_7_mature.gif" width="130" alt="Mature"> |
| **8** | **Ancient** | `1200 – 1799` | Multi-tiered monolithic horns, double dorsal spikes, dense armor | <img src="./assets/previews/stage_8_ancient.gif" width="130" alt="Ancient"> |
| **9** | **Warlord** | `1800 – 2699` | Massive razor wings, jagged spine armor, and radiating golden power | <img src="./assets/previews/stage_9_warlord.gif" width="130" alt="Warlord"> |
| **10** | **Elder** | `2700 – 3999` | Primordial horns, sharp dragon crests, and reinforced battle carapaces | <img src="./assets/previews/stage_10_elder.gif" width="130" alt="Elder"> |
| **11** | **Dragon Lord** | `4000 – 5999` | Sovereign golden wings, shoulder star emblems, ground-tremoring talons | <img src="./assets/previews/stage_11_dragon_lord.gif" width="130" alt="Dragon Lord"> |
| **12** | **Celestial Dragon** | `6000 – 8999` | Radiant cosmic wings, floating star crystals, and celestial energy flames | <img src="./assets/previews/stage_12_celestial_dragon.gif" width="130" alt="Celestial Dragon"> |
| **13** | **Mythic Dragon** | `9000+` | Omnipotent form: blazing cosmic aura rings, orbiting energy crystals, divine flame | <img src="./assets/previews/stage_13_mythic_dragon.gif" width="130" alt="Mythic Dragon"> |

<p align="center">
  <img src="./assets/evolution_showcase.png" width="700" alt="Drago 13-Phase Evolution Showcase Grid">
</p>

---

## About

Drago is an open-source, automated GitHub profile companion designed to bring gamification to everyday software development. Instead of static contributor charts or plain streak counters, Drago lives directly inside your GitHub profile README as an animated dragon that breathes, blinks, and evolves in real time based on your actual GitHub activity.

---

## Description

Drago bridges procedural animation and the GitHub Developer API into a zero-maintenance profile widget:

- **Continuous Native Animation**: Features deep chest breathing, reactive eye blinking, and organic tail motion rendered natively via standard Markdown with zero client-side JavaScript.
- **Dynamic 1:1 Progression**: Evolution Power (XP) directly mirrors your authentic contribution calendar milestones. Each commit and contribution drives your golden progress bar forward toward the next evolutionary tier.
- **Cyberpunk HUD Status Card**: An action-game styled companion card displaying your current level, stage name, active streak, evolution power (XP), and live GitHub activity metrics (commits and pull requests).
- **13 Evolution Tiers**: Watch your companion mature from a dormant Magma Egg into a mythical Celestial Dragon and divine Mythic Dragon as your coding journey progresses.
- **Autonomous Updates via GitHub Actions**: Runs autonomously every 15 minutes inside your own repository, fetching your latest activity, calculating evolution progression, rendering updated high-resolution assets, and committing them without requiring external servers.
- **6 Cel-Shaded Palettes**: Choose from Obsidian Gold, Crimson Fury, Arctic Frost, Cyberpunk Neon, Toxic Emerald, and Solar Flare to complement your personal profile aesthetic.

---

## How It Works

Drago is designed to be completely autonomous and self-sustaining:

- **Independent Execution**: When you fork Drago, the GitHub Actions workflow executes entirely on GitHub's free runners under your account. It evaluates `github.repository_owner`, meaning it always calculates data for the owner of the fork.
- **No Third-Party Servers**: There are no external servers, databases, or API quotas to manage. Your assets live directly in your Git repository.
- **Automated Cycles**: Every 15 minutes, the workflow fetches your authentic contribution calendar, recalculates your XP and level, re-renders the companion animation and status card, and commits the updated assets directly to your `main` branch.

---

## How Evolution Works

Drago's physical traits reflect your actual development habits:

| GitHub Metric | Draconic Impact |
| :--- | :--- |
| **Commits** | Increases overall body mass and muscular maturity |
| **Pull Requests** | Grows sweeping horns and dorsal armor plates |
| **Merged PRs** | Reinforces chest carapaces and shoulder guards |
| **Contribution Streak** | Ignites an active fiery energy aura (streak 3+ days) |
| **Stars & Repositories** | Expands wingspan and elongates the bladed tail |

### XP & Level Progression
- **1:1 Contribution Mapping**: Each contribution on your GitHub calendar grants 1.0 XP.
- **Pull Request Rewards**: Each pull request awards 4.0 XP, with accepted/merged pull requests granting an additional 6.0 XP.
- **Streak Bonus**: Each consecutive day in your active streak grants an additional 0.1 XP (up to 5.0 XP bonus).
- **Smooth Progress Bar**: The golden progress bar on your status card fills proportionally between your current level and the next tier, advancing with every commit, contribution, and pull request.

---

## Color Palettes

Drago features **6 cel-shaded color palettes**. Both your animated dragon companion and the cyberpunk HUD status card automatically adapt to your chosen aesthetic:

<p align="center">
  <img src="./assets/palettes_showcase.png" width="700" alt="Drago 6 Cel-Shaded Color Palettes Showcase">
</p>

| Palette | Config Key | Theme & Accents | Dragon Preview | Matching Status Card |
| :--- | :--- | :--- | :---: | :---: |
| **Obsidian Gold** *(Default)* | `"obsidian-gold"` | Charcoal obsidian body `#1E1F24` with gold accents `#F5B700` | <img src="./assets/palettes/obsidian-gold.png" width="170" alt="Obsidian Gold"> | <img src="./assets/palettes/status-obsidian-gold.svg" width="220" alt="Obsidian Gold Card"> |
| **Crimson Fury** | `"crimson-fury"` | Deep scarlet body `#2D0F14` with radiant crimson accents `#FF2A4D` | <img src="./assets/palettes/crimson-fury.png" width="170" alt="Crimson Fury"> | <img src="./assets/palettes/status-crimson-fury.svg" width="220" alt="Crimson Fury Card"> |
| **Arctic Frost** | `"arctic-frost"` | Glacial silver body `#E2E9F2` with electric cyan accents `#00D2FF` | <img src="./assets/palettes/arctic-frost.png" width="170" alt="Arctic Frost"> | <img src="./assets/palettes/status-arctic-frost.svg" width="220" alt="Arctic Frost Card"> |
| **Cyberpunk Neon** | `"cyberpunk-neon"` | Midnight synth body `#14141E` with hyper turquoise `#00F5D4` | <img src="./assets/palettes/cyberpunk-neon.png" width="170" alt="Cyberpunk Neon"> | <img src="./assets/palettes/status-cyberpunk-neon.svg" width="220" alt="Cyberpunk Neon Card"> |
| **Toxic Emerald** | `"toxic-emerald"` | Bio-forest body `#141D17` with radioactive green `#2BEE6C` | <img src="./assets/palettes/toxic-emerald.png" width="170" alt="Toxic Emerald"> | <img src="./assets/palettes/status-toxic-emerald.svg" width="220" alt="Toxic Emerald Card"> |
| **Solar Flare** | `"solar-flare"` | Ember ash body `#241812` with blazing solar orange flame `#FF7700` | <img src="./assets/palettes/solar-flare.png" width="170" alt="Solar Flare"> | <img src="./assets/palettes/status-solar-flare.svg" width="220" alt="Solar Flare Card"> |

### 13-Phase Evolution Showcases by Palette

Every evolutionary form physically transforms and radiates in your selected palette:

<details open>
<summary><strong>Obsidian Gold (Default) - 13 Evolution Phases</strong></summary>
<br>
<p align="center">
  <img src="./assets/evolution_showcase_obsidian-gold.png" width="700" alt="Obsidian Gold 13-Phase Evolution Showcase Grid">
</p>
</details>

<details>
<summary><strong>Crimson Fury - 13 Evolution Phases</strong></summary>
<br>
<p align="center">
  <img src="./assets/evolution_showcase_crimson-fury.png" width="700" alt="Crimson Fury 13-Phase Evolution Showcase Grid">
</p>
</details>

<details>
<summary><strong>Arctic Frost - 13 Evolution Phases</strong></summary>
<br>
<p align="center">
  <img src="./assets/evolution_showcase_arctic-frost.png" width="700" alt="Arctic Frost 13-Phase Evolution Showcase Grid">
</p>
</details>

<details>
<summary><strong>Cyberpunk Neon - 13 Evolution Phases</strong></summary>
<br>
<p align="center">
  <img src="./assets/evolution_showcase_cyberpunk-neon.png" width="700" alt="Cyberpunk Neon 13-Phase Evolution Showcase Grid">
</p>
</details>

<details>
<summary><strong>Toxic Emerald - 13 Evolution Phases</strong></summary>
<br>
<p align="center">
  <img src="./assets/evolution_showcase_toxic-emerald.png" width="700" alt="Toxic Emerald 13-Phase Evolution Showcase Grid">
</p>
</details>

<details>
<summary><strong>Solar Flare - 13 Evolution Phases</strong></summary>
<br>
<p align="center">
  <img src="./assets/evolution_showcase_solar-flare.png" width="700" alt="Solar Flare 13-Phase Evolution Showcase Grid">
</p>
</details>

### How to Switch Your Palette
To change your dragon's skin, set `"palette_name"` in your `drago.config.json`:

```json
{
  "palette_name": "crimson-fury"
}
```

The next time GitHub Actions executes (or when triggered manually), your dragon GIF and status card will automatically update to your selected palette.

---

## Advanced Configuration & Technical Docs

Looking for local CLI commands, custom point weights, testing suites, or architecture internals?

Check out the **[Technical & Developer Setup Guide (SETUP.md)](SETUP.md)**.

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
