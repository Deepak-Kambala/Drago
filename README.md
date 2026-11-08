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
  <a href="#-quick-setup-2-minutes"><img src="https://img.shields.io/badge/Setup-2_Minutes-F5B700?style=flat-square" alt="Quick Setup"></a>
  <a href="#-evolution-tiers"><img src="https://img.shields.io/badge/Evolution-13_Tiers-2EA043?style=flat-square" alt="Evolution Stages"></a>
  <a href="#-color-palettes"><img src="https://img.shields.io/badge/Palettes-6_Styles-00D2FF?style=flat-square" alt="Palettes"></a>
  <a href="SETUP.md"><img src="https://img.shields.io/badge/Technical_Docs-SETUP.md-8957E5?style=flat-square" alt="Technical Docs"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License"></a>
</p>

---

## 🐉 Meet Drago

**Drago is not a static badge or flat image.** 

He is an animated draconic companion designed in a cel-shaded action-adventure cartoon style who lives directly on your GitHub profile:

- 🫁 **Deep breathing motion** with rhythmic chest and wing flexion
- 👁️ **Natural eye blinking** tracking visitors across your profile
- 🐾 **Sinuous tail sway** and ground-gripping talons
- 🔥 **Blazing energy aura** that ignites when you are on an active contribution streak
- 🧬 **Physical anatomical evolution** growing from a gentle Magma Egg into a mythical deity as you commit code

Works out of the box on GitHub with **zero JavaScript or client dependencies**.

---

## ⚡ Quick Setup (2 Minutes)

Add Drago to your GitHub Profile README in two simple steps:

### Option A: The Easy Fork Way (Recommended)

1. **Fork this repository** to your GitHub account (name it `drago`).
2. **Enable GitHub Actions**:
   - In your forked repo, go to **Settings** $\rightarrow$ **Actions** $\rightarrow$ **General**.
   - Under **Workflow permissions**, choose **Read and write permissions** and click **Save**.
   - Go to the **Actions** tab and click **I understand my workflows, go ahead and enable them**.
3. **Embed in your Profile README** (`<username>/<username>`):
   Paste this snippet into your profile `README.md` (replace `YOUR_USERNAME` with your actual GitHub username, e.g. `Deepak-Kambala`):

```markdown
<p align="center">
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/Drago/main/assets/dragon.gif" width="650" alt="My Evolving Dragon">
  <br>
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/Drago/main/assets/dragon-status.svg" width="650" alt="Drago Status Card">
</p>
```

> [!TIP]
> **Example for `@Deepak-Kambala`:**
> ```markdown
> <p align="center">
>   <img src="https://raw.githubusercontent.com/Deepak-Kambala/Drago/main/assets/dragon.gif" width="650" alt="My Evolving Dragon">
>   <br>
>   <img src="https://raw.githubusercontent.com/Deepak-Kambala/Drago/main/assets/dragon-status.svg" width="650" alt="Drago Status Card">
> </p>
> ```

That's it! GitHub Actions automatically runs daily at midnight UTC to evaluate your commits, PRs, and streaks, continuously evolving your dragon.

---

### Option B: Directly Inside Your Profile Repository

If you prefer keeping everything in your `<username>/<username>` profile repository:

1. Copy the `drago/`, `.github/`, and `drago.config.json` folders into your profile repository.
2. In your profile repo settings, ensure **Read and write permissions** are enabled for Actions (**Settings $\rightarrow$ Actions $\rightarrow$ General $\rightarrow$ Workflow permissions**).
3. Add this snippet to your `README.md`:

```markdown
<p align="center">
  <img src="./assets/dragon.gif" width="650" alt="My Evolving Dragon">
  <br>
  <img src="./assets/dragon-status.svg" width="650" alt="Drago Status Card">
</p>
```

---

## 🏆 Evolution Tiers

Drago progresses through **13 distinct evolutionary forms** based on your GitHub activity:

| Level | Stage | XP Threshold | Distinct Traits | Animation Preview |
|:---:|:---|:---:|:---|:---:|
| **1** | **Egg** | `0 – 9` | Obsidian shell with golden magma veins & inner heartbeat pulse | <img src="./assets/previews/stage_1_egg.gif" width="130" alt="Egg"> |
| **2** | **Hatchling** | `10 – 49` | Small compact wings, horn buds, eager amber eyes | <img src="./assets/previews/stage_2_hatchling.gif" width="130" alt="Hatchling"> |
| **3** | **Youngling** | `50 – 149` | Curved horns, lengthened tail, sharp ivory talons | <img src="./assets/previews/stage_3_youngling.gif" width="130" alt="Youngling"> |
| **4** | **Juvenile** | `150 – 299` | Athletic build, dorsal spines, wider wingspan, glowing markings | <img src="./assets/previews/stage_4_juvenile.gif" width="130" alt="Juvenile"> |
| **5** | **Adolescent** | `300 – 499` | Muscular limbs, sweeping battle horns, battle stance | <img src="./assets/previews/stage_5_adolescent.gif" width="130" alt="Adolescent"> |
| **6** | **Adult** | `500 – 749` | Broad wingspan, heavy chest musculature, imposing silhouette | <img src="./assets/previews/stage_6_adult.gif" width="130" alt="Adult"> |
| **7** | **Mature** | `750 – 999` | Shoulder carapaces, reinforced tail blade, golden flank markings | <img src="./assets/previews/stage_7_mature.gif" width="130" alt="Mature"> |
| **8** | **Ancient** | `1000 – 1499` | Multi-tiered monolithic horns, double dorsal spikes, dense armor | <img src="./assets/previews/stage_8_ancient.gif" width="130" alt="Ancient"> |
| **9** | **Warlord** | `1500 – 1999` | Massive razor wings, jagged spine armor, and radiating golden power | <img src="./assets/previews/stage_9_warlord.gif" width="130" alt="Warlord"> |
| **10** | **Elder** | `2000 – 2499` | Primordial horns, sharp dragon crests, and reinforced battle carapaces | <img src="./assets/previews/stage_10_elder.gif" width="130" alt="Elder"> |
| **11** | **Dragon Lord** | `2500 – 2999` | Sovereign golden wings, shoulder star emblems, ground-tremoring talons | <img src="./assets/previews/stage_11_dragon_lord.gif" width="130" alt="Dragon Lord"> |
| **12** | **Celestial Dragon** | `3000 – 3999` | Radiant cosmic wings, floating star crystals, and celestial energy flames | <img src="./assets/previews/stage_12_celestial_dragon.gif" width="130" alt="Celestial Dragon"> |
| **13** | **Mythic Dragon** | `4000+` | Omnipotent form: blazing cosmic aura rings, orbiting energy crystals, divine flame | <img src="./assets/previews/stage_13_mythic_dragon.gif" width="130" alt="Mythic Dragon"> |

<p align="center">
  <img src="./assets/evolution_showcase.png" width="700" alt="Drago 13-Phase Evolution Showcase Grid">
</p>

---

## 🧬 How Evolution Works

Drago's physical traits reflect your actual development habits:

| GitHub Metric | Draconic Impact |
| :--- | :--- |
| **Commits** | Increases overall body mass and muscular maturity |
| **Pull Requests** | Grows sweeping horns and dorsal armor plates |
| **Merged PRs** | Reinforces chest carapaces and shoulder guards |
| **Contribution Streak** | Ignites an active fiery energy aura |
| **Stars & Repositories** | Expands wingspan and elongates the bladed tail |

### Gentle Rolling Decay
- **Recent activity (0–7 days)** provides maximum energy and power.
- **Monthly contributions (8–30 days)** sustain body mass and wing structures.
- **Lifetime wisdom**: 30% of all contributions become permanent experience that never decays, so taking a break will never reset your dragon.

---

## 🎨 Color Palettes

Choose the skin that matches your profile's aesthetic:

- **Obsidian Gold** *(Default)*: Charcoal obsidian body `#1E1F24` with racing gold accents `#F5B700` and amber eyes.
- **Crimson Fury**: Deep scarlet charcoal `#2D0F14` with blazing crimson accents `#FF2A4D`.
- **Arctic Frost**: Glacial silver `#E2E9F2` with electric cyan energy `#00D2FF`.
- **Cyberpunk Neon**: Midnight synth `#14141E` with hyper turquoise `#00F5D4` and magenta spikes.
- **Toxic Emerald**: Bio-forest `#141D17` with radioactive green `#2BEE6C`.
- **Solar Flare**: Ember ash `#241812` with blazing solar orange flame `#FF7700`.

To change your palette, set `"palette_name"` in `drago.config.json` (e.g. `"palette_name": "crimson-fury"`).

---

## ⚙️ Advanced Configuration & Technical Docs

Looking for local CLI commands, custom point weights, testing suites, or architecture internals?

👉 Check out the **[Technical & Developer Setup Guide (SETUP.md)](SETUP.md)**.

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
