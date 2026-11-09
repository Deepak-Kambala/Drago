"""
Sprite animation and organic deformation kinematics engine for Drago.
Animates the exact authentic dragon artwork across all 13 evolution phases
with continuous breathing, tail waving, wing flutters, head tilts, blinking,
and shimmering cosmic aura.
"""

import os
import math
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw
import numpy as np
from drago.evolution import DragonState
from drago.config import DragoConfig

class SpriteAnimator:
    def __init__(self, config: DragoConfig, state: DragonState):
        self.config = config
        self.state = state
        sprite_filename = getattr(state, "sprite_file", None)
        if not sprite_filename:
            from drago.config import STAGE_DEFINITIONS
            lvl = getattr(state, "stage_level", 1)
            stage_idx = max(0, min(len(STAGE_DEFINITIONS) - 1, lvl - 1))
            sprite_filename = STAGE_DEFINITIONS[stage_idx].get("sprite_file", f"{lvl:02d}_{getattr(state, 'stage_id', 'dragon')}.png")

        self.sprite_path = os.path.join("assets", "sprites", sprite_filename)
        if not os.path.exists(self.sprite_path):
            self.sprite_path = os.path.join("assets", "sprites", "06_adult.png")

        raw_im = Image.open(self.sprite_path)
        self.orig_w, self.orig_h = raw_im.size

        # If RGBA image has native alpha, preserve its pristine alpha channel
        if raw_im.mode == "RGBA":
            raw_arr = np.array(raw_im, dtype=np.float32)
            self.sprite_arr = raw_arr[:, :, :3]
            self.alpha_arr = raw_arr[:, :, 3]
        else:
            raw_rgb = raw_im.convert("RGB")
            raw_arr = np.array(raw_rgb, dtype=np.float32)
            max_c = np.max(raw_arr, axis=2)
            self.sprite_arr = raw_arr
            self.alpha_arr = np.clip((max_c - 2.0) / 10.0, 0.0, 1.0) * 255.0

        # Apply dynamic palette recoloring across all 6 cel-shaded themes
        self.sprite_arr = self._recolor_to_palette(self.sprite_arr, self.alpha_arr)

        # Detect eye location for blinking
        self.eye_pos = self._detect_eye_position(self.sprite_arr)
        self.is_egg = getattr(state, "is_egg", False)

    def _recolor_to_palette(self, rgb_arr: np.ndarray, alpha_arr: np.ndarray) -> np.ndarray:
        """
        Dynamically recolors dragon sprites to match any of the 6 authentic themes
        (Obsidian Gold, Crimson Fury, Arctic Frost, Cyberpunk Neon, Toxic Emerald, Solar Flare)
        or custom user-defined palettes while preserving cel-shading and alpha anti-aliasing.
        """
        palette_name = getattr(self.config, "palette_name", "obsidian-gold")
        if palette_name == "obsidian-gold" and not getattr(self.config, "custom_palette", None):
            return rgb_arr.copy()

        from drago.geometry import hex_to_rgb
        palette = self.config.get_palette()
        out_rgb = rgb_arr.copy()
        r = out_rgb[:, :, 0]
        g = out_rgb[:, :, 1]
        b = out_rgb[:, :, 2]

        target_accent = np.array(hex_to_rgb(palette.get("accent", "#F5B700")), dtype=np.float32)
        target_glow = np.array(hex_to_rgb(palette.get("accent_glow", palette.get("accent", "#FFD13B"))), dtype=np.float32)
        target_dark = np.array(hex_to_rgb(palette.get("accent_dark", palette.get("accent", "#B88200"))), dtype=np.float32)
        body_tint = np.array(hex_to_rgb(palette.get("body_primary", "#1E1F24")), dtype=np.float32)

        # Detect glowing gold / warm accent markings (high R, high G, lower B)
        warmth = np.maximum(0.0, np.minimum(r, g * 1.15) - b * 1.35)
        accent_weight = np.clip((warmth - 25.0) / 90.0, 0.0, 1.0)

        # Luminance determines shading (dark shade -> primary accent -> specular glow)
        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0

        low_mask = lum < 0.60
        f_low = np.clip(lum / 0.60, 0.0, 1.0)[:, :, None]
        t_low = target_dark * (1.0 - f_low) + target_accent * f_low

        f_high = np.clip((lum - 0.60) / 0.40, 0.0, 1.0)[:, :, None]
        t_high = target_accent * (1.0 - f_high) + target_glow * f_high

        t_color = np.where(low_mask[:, :, None], t_low, t_high)

        # Blend accents smoothly
        w = accent_weight[:, :, None]
        out_rgb = out_rgb * (1.0 - w) + t_color * w

        # Subtle body tinting (adapts dark charcoal body to match theme tone)
        body_mask = (1.0 - accent_weight) * (alpha_arr / 255.0) * (1.0 - np.clip((r + g + b) / 280.0, 0.0, 1.0))
        b_w = (body_mask * 0.22)[:, :, None]
        out_rgb = out_rgb * (1.0 - b_w) + body_tint * b_w

        return np.clip(out_rgb, 0.0, 255.0)

    def _detect_eye_position(self, arr: np.ndarray) -> Optional[Tuple[int, int]]:
        """Finds the amber eye coordinates on the dragon's head."""
        h, w, _ = arr.shape
        # Precision calibration for high-res master sprites
        if '02_hatchling' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 2:
            return (int(w * 0.716), int(h * 0.294))  # ~ (425, 140) for 593x476
        if '03_youngling' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 3:
            return (int(w * 0.825), int(h * 0.315))  # ~ (778, 252) for 944x801
        if '04_juvenile' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 4:
            return (int(w * 0.821), int(h * 0.295))  # ~ (765, 224) for 933x760
        if '05_adolescent' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 5:
            return (int(w * 0.836), int(h * 0.304))  # ~ (800, 231) for 957x760
        if '06_adult' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 6:
            return (int(w * 0.806), int(h * 0.300))  # ~ (825, 205) for 1024x682
        if '07_mature' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 7:
            return (int(w * 0.864), int(h * 0.321))  # ~ (824, 227) for 954x707
        if '08_ancient' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 8:
            return (int(w * 0.849), int(h * 0.348))  # ~ (855, 245) for 1007x704
        if '09_warlord' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 9:
            return (int(w * 0.865), int(h * 0.388))  # ~ (875, 258) for 1012x665
        if '10_elder' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 10:
            return (int(w * 0.843), int(h * 0.394))  # ~ (828, 306) for 982x777
        if '11_dragon_lord' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 11:
            return (int(w * 0.873), int(h * 0.342))  # ~ (878, 230) for 1006x673
        if '12_celestial_dragon' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 12:
            return (int(w * 0.731), int(h * 0.453))  # ~ (721, 286) for 986x631
        if '13_mythic_dragon' in self.sprite_path or getattr(self.state, 'stage_level', 0) == 13:
            return (int(w * 0.734), int(h * 0.476))  # ~ (744, 282) for 1014x593

        # Head is generally in upper-right quadrant
        head_region = arr[:int(h * 0.55), int(w * 0.55):]
        eye_mask = (head_region[:, :, 0] > 170) & (head_region[:, :, 1] > 110) & (head_region[:, :, 2] < 70)
        y_indices, x_indices = np.where(eye_mask)
        if len(y_indices) > 0:
            ey = int(np.mean(y_indices))
            ex = int(w * 0.55) + int(np.mean(x_indices))
            return (ex, ey)
        return (int(w * 0.82), int(h * 0.30))

    def warp_frame(self, t: float, action: str = "idle") -> Image.Image:
        """
        Applies organic 2D mesh kinematic displacement for animation phase t in [0.0, 1.0).
        """
        arr = self.sprite_arr.copy()
        alpha = self.alpha_arr.copy()
        h, w, _ = arr.shape

        t_rad = 2.0 * math.pi * t
        y_coords, x_coords = np.mgrid[0:h, 0:w].astype(np.float32)

        if self.is_egg:
            # --- EGG KINEMATICS ---
            # Gentle rhythmic rocking and internal magma heartbeat pulse
            rock_angle = math.sin(t_rad) * 0.065
            cx, cy = w * 0.5, h * 0.90

            cos_a = math.cos(rock_angle)
            sin_a = math.sin(rock_angle)
            rx = (x_coords - cx) * cos_a - (y_coords - cy) * sin_a + cx
            ry = (x_coords - cx) * sin_a + (y_coords - cy) * cos_a + cy

            src_x = np.clip(rx, 0, w - 1)
            src_y = np.clip(ry, 0, h - 1)

            # Glowing magma heartbeat pulse
            pulse = math.sin(t_rad) * 0.22
            gold_mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] > 100) & (arr[:, :, 2] < 70)
            arr[gold_mask, 0] = np.clip(arr[gold_mask, 0] * (1.0 + pulse * 0.15), 0, 255)
            arr[gold_mask, 1] = np.clip(arr[gold_mask, 1] * (1.0 + pulse * 0.15), 0, 255)
        else:
            # --- DRAGON SKELETAL KINEMATICS ---
            # 1. Tail undulating wave (left region: x < w * 0.44)
            tail_prog = np.clip((w * 0.44 - x_coords) / (w * 0.44), 0.0, 1.0)
            tail_sway_amp = 6.5 * (tail_prog ** 1.4)
            tail_dy = np.sin(t_rad - tail_prog * 3.6) * tail_sway_amp
            tail_dx = -np.cos(t_rad - tail_prog * 3.6) * (1.8 * tail_prog)

            # 2. Wing lift & flare (upper-middle region)
            wing_x = np.clip(1.0 - np.abs(x_coords - w * 0.42) / (w * 0.30), 0.0, 1.0)
            wing_y = np.clip((h * 0.62 - y_coords) / (h * 0.62), 0.0, 1.0)
            wing_amp = 5.5
            if action == "roar":
                wing_amp = 14.0
            wing_dy = - np.sin(t_rad + 0.8) * (wing_amp * wing_x * wing_y)

            # 3. Head & neck tilt (upper-right region)
            head_x = np.clip((x_coords - w * 0.60) / (w * 0.40), 0.0, 1.0)
            head_y = np.clip((h * 0.55 - y_coords) / (h * 0.55), 0.0, 1.0)
            head_amp = 3.8
            if action == "roar":
                head_amp = -9.0  # Head raises back
            head_dy = np.sin(t_rad + 0.4) * (head_amp * head_x * head_y)

            # 4. Chest breathing expansion
            chest_x = np.clip(1.0 - np.abs(x_coords - w * 0.58) / (w * 0.22), 0.0, 1.0)
            chest_y = np.clip(1.0 - np.abs(y_coords - h * 0.64) / (h * 0.24), 0.0, 1.0)
            breath_dy = np.sin(t_rad) * (2.4 * chest_x * chest_y)

            total_dy = tail_dy + wing_dy + head_dy + breath_dy
            total_dx = tail_dx

            src_x = np.clip(x_coords - total_dx, 0, w - 1)
            src_y = np.clip(y_coords - total_dy, 0, h - 1)

            # 5. Cosmic Aura / Flame shimmer (for Elder, Dragon Lord, Celestial, Mythic)
            if self.state.stage_level >= 8 or getattr(self.state, "aura_intensity", 0) > 0.05:
                # High brightness outer pixels pulse gently
                bright_mask = np.mean(arr, axis=2) > 90
                shimmer = 1.0 + math.sin(t_rad * 2.0) * 0.12
                arr[bright_mask] = np.clip(arr[bright_mask] * shimmer, 0, 255)

        # Bilinear interpolation warp
        x0 = np.floor(src_x).astype(int)
        x1 = np.clip(x0 + 1, 0, w - 1)
        y0 = np.floor(src_y).astype(int)
        y1 = np.clip(y0 + 1, 0, h - 1)

        wx = (src_x - x0)[:, :, None]
        wy = (src_y - y0)[:, :, None]

        top_rgb = (1.0 - wx) * arr[y0, x0] + wx * arr[y0, x1]
        bot_rgb = (1.0 - wx) * arr[y1, x0] + wx * arr[y1, x1]
        warped_rgb = (1.0 - wy) * top_rgb + wy * bot_rgb

        top_a = (1.0 - wx[:, :, 0]) * alpha[y0, x0] + wx[:, :, 0] * alpha[y0, x1]
        bot_a = (1.0 - wx[:, :, 0]) * alpha[y1, x0] + wx[:, :, 0] * alpha[y1, x1]
        warped_a = (1.0 - wy[:, :, 0]) * top_a + wy[:, :, 0] * bot_a

        # 6. Eye Blink (between t = 0.65 and 0.80)
        if not self.is_egg and self.eye_pos and 0.65 <= t <= 0.80:
            blink_rel = (t - 0.65) / 0.15
            # Parabolic blink down and up
            blink_amt = 1.0 - abs(math.cos(blink_rel * math.pi))
            ex, ey = self.eye_pos
            # Apply eyelid darkening to amber pixels in eye bounding zone
            rad_x = max(4, int(w * 0.026))
            rad_y = max(3, int(h * 0.022))
            for by in range(max(0, ey - rad_y), min(h, ey + rad_y + 1)):
                for bx in range(max(0, ex - rad_x), min(w, ex + rad_x + 1)):
                    if warped_rgb[by, bx, 0] > 140 and warped_rgb[by, bx, 1] > 90 and warped_rgb[by, bx, 2] < 90:
                        dark_eyelid = np.array([22, 23, 28], dtype=np.float32)
                        warped_rgb[by, bx] = (1.0 - blink_amt) * warped_rgb[by, bx] + blink_amt * dark_eyelid

        final_rgba = np.dstack([
            np.clip(warped_rgb, 0, 255),
            np.clip(warped_a, 0, 255)
        ]).astype(np.uint8)

        return Image.fromarray(final_rgba, mode="RGBA")

    def render_canvas_frame(self, t: float, width: int = 650, height: int = 420, action: str = "idle") -> Image.Image:
        """
        Renders the fully warped dragon composited onto the GitHub dark canvas
        with atmospheric ambient radial glow and contact shadow.
        """
        warped_sprite = self.warp_frame(t, action=action)
        canvas = Image.new("RGBA", (width, height), (13, 17, 23, 255))
        
        # 1. True Alpha-blended Ambient Amber Glow behind dragon
        glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)

        palette = self.config.get_palette()
        accent = palette.get("accent", "#FCB42B")
        from drago.geometry import hex_to_rgb
        accent_rgb = hex_to_rgb(accent)

        cx, cy = width * 0.48, height * 0.54
        r_mult = 1.0 + (self.state.stage_level / 13.0) * 0.35
        glow_alpha = int(24 + (self.state.stage_level / 13.0) * 35)

        for r_step in range(6, 0, -1):
            rx = (width * 0.34 * r_mult) * (r_step / 6.0)
            ry = (height * 0.28 * r_mult) * (r_step / 6.0)
            step_alpha = int(glow_alpha * (1.0 - (r_step / 6.0) * 0.75))
            glow_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], step_alpha))

        # 2. Contact Shadow under feet
        glow_draw.ellipse([80, int(height * 0.88 - 14), width - 80, int(height * 0.88 + 14)], fill=(5, 6, 8, 170))

        # Composite glow and shadow onto background
        canvas = Image.alpha_composite(canvas, glow_layer)

        # 3. Optimal Scaling for crystal-clear fidelity
        target_h = int(height * 0.86)
        scale_factor = target_h / self.orig_h
        scaled_w = int(round(self.orig_w * scale_factor))
        scaled_h = int(round(self.orig_h * scale_factor))

        scaled_sprite = warped_sprite.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)

        # 4. Paste Dragon Sprite centered
        px = (width - scaled_w) // 2
        py = int(height * 0.88) - scaled_h + 8
        canvas.alpha_composite(scaled_sprite, (px, py))

        return canvas

