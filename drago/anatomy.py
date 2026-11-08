"""
Anatomical components and vector illustration pipeline for Drago.
Constructs the cel-shaded 2D action cartoon dragon with scalable parts,
cel-shading layers, and bold graphic outlines.
"""

import math
from typing import List, Tuple, Dict, Any, Optional
from PIL import Image, ImageDraw
from drago.geometry import (
    Point, rotate_point, translate_point, scale_point,
    quadratic_bezier, cubic_bezier, hex_to_rgb, hex_to_rgba,
    blend_colors, draw_polygon_with_outline, draw_ribbon
)
from drago.evolution import DragonState

class DragonAnatomy:
    def __init__(self, state: DragonState, palette: Dict[str, str], supersample: int = 2):
        self.state = state
        self.pal = palette
        self.ss = supersample

        # Precompute RGB / RGBA colors
        self.c_body = hex_to_rgb(palette.get("body_primary", "#1E1F24"))
        self.c_body_dark = hex_to_rgb(palette.get("body_secondary", "#121317"))
        self.c_body_light = hex_to_rgb(palette.get("body_highlight", "#34363F"))
        self.c_belly = hex_to_rgb(palette.get("underbelly", "#2A2C34"))
        self.c_accent = hex_to_rgb(palette.get("accent", "#F5B700"))
        self.c_accent_glow = hex_to_rgb(palette.get("accent_glow", "#FFD13B"))
        self.c_accent_dark = hex_to_rgb(palette.get("accent_dark", "#B88200"))
        self.c_horns = hex_to_rgb(palette.get("horns", "#15161A"))
        self.c_horns_hi = hex_to_rgb(palette.get("horns_highlight", "#4B4E59"))
        self.c_claws = hex_to_rgb(palette.get("claws", "#E8EAF0"))
        self.c_claws_dark = hex_to_rgb(palette.get("claws_shadow", "#8C90A0"))
        self.c_eyes = hex_to_rgb(palette.get("eyes", "#FFB703"))
        self.c_pupil = hex_to_rgb(palette.get("pupil", "#0B0C0E"))
        self.c_wing_bone = hex_to_rgb(palette.get("wing_bone", "#1A1B20"))
        self.c_wing_mem = hex_to_rgb(palette.get("wing_membrane", "#22242B"))
        self.c_wing_mem_in = hex_to_rgb(palette.get("wing_membrane_inner", "#2E303A"))
        self.c_armor = hex_to_rgb(palette.get("armor", "#2B2D37"))
        self.c_armor_edge = hex_to_rgb(palette.get("armor_edge", "#5A5E70"))
        self.c_spikes = hex_to_rgb(palette.get("spikes", "#18191E"))
        self.c_aura = hex_to_rgb(palette.get("aura", "#FFD13B"))

        # Outline color: deep obsidian ink line
        self.c_ink = (8, 9, 12)
        self.line_w = int(round(3 * self.ss))
        self.line_w_heavy = int(round(4.5 * self.ss))
        self.line_w_thin = int(round(2 * self.ss))

    def render_frame(
        self,
        canvas_width: int,
        canvas_height: int,
        frame_idx: int,
        total_frames: int,
        action: str = "idle",
    ) -> Image.Image:
        """
        Renders a single animation frame of the dragon at internal supersampled resolution.
        """
        w = canvas_width * self.ss
        h = canvas_height * self.ss

        # Create transparent canvas
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Animation parameters based on time t in [0.0, 1.0)
        t = frame_idx / max(1, total_frames)
        t_rad = t * 2.0 * math.pi

        # 1. Breathing motion (sine wave)
        # Chest expands and contracts; subtle body shift
        breath = math.sin(t_rad)
        breath_y = breath * (4.0 * self.ss)
        breath_scale = 1.0 + (breath * 0.02)

        # 2. Eye blinking
        # Blink once per cycle around frame 15-18
        blink_val = 1.0  # 1.0 = fully open, 0.0 = fully closed
        blink_start = 0.65
        blink_end = 0.80
        if blink_start <= t <= blink_end:
            rel = (t - blink_start) / (blink_end - blink_start)
            # Dip to 0 in middle
            blink_val = abs(math.cos(rel * math.pi))

        # 3. Head & Look Around movement
        # Subtle nod and tilt
        head_nod = math.sin(t_rad + 0.4) * (2.5 * self.ss)
        head_angle = math.sin(t_rad) * 0.03  # radians
        look_shift = math.sin(t_rad * 0.5) * (3.0 * self.ss)

        # 4. Tail wave motion (traveling wave)
        # Each segment follows a lagging phase
        tail_waves = [
            math.sin(t_rad - i * 0.65) * (8.0 * self.ss * (1.0 + i * 0.4))
            for i in range(7)
        ]

        # 5. Wing folding / floating
        # Idle gentle rise and fall of the wings
        wing_flare = math.sin(t_rad + 0.8) * 0.06
        wing_y_bob = math.sin(t_rad + 0.8) * (6.0 * self.ss)

        # 6. Roar action overrides if action == 'roar'
        mouth_open_rad = 0.0
        jaw_drop = 0.0
        if action == "roar":
            # Roar crests between 0.3 and 0.7
            if 0.2 < t < 0.8:
                intensity = math.sin((t - 0.2) / 0.6 * math.pi)
                mouth_open_rad = intensity * 0.35
                jaw_drop = intensity * (16.0 * self.ss)
                head_angle -= intensity * 0.12
                wing_flare += intensity * 0.22
                breath_y -= intensity * (10.0 * self.ss)

        # Base anchor coordinates in supersampled space
        # Center the dragon comfortably with ground plane at bottom
        center_x = w * 0.48
        ground_y = h * 0.86

        # Draw Layers in correct Z-order (Back to Front):
        # 0. Ground shadow
        self._draw_shadow(draw, center_x, ground_y, w, h)

        # 1. Background Aura / streak energy motes (if active)
        if self.state.aura_intensity > 0.05:
            self._draw_aura(draw, center_x, ground_y - (200 * self.ss), t, w, h)

        # 2. Far Wing (Left Wing, behind torso)
        self._draw_wing_far(draw, center_x, ground_y + breath_y, wing_flare, wing_y_bob)

        # 3. Tail (curves behind hips and sweeps up)
        self._draw_tail(draw, center_x, ground_y + breath_y, tail_waves)

        # 4. Hind Leg & Claws
        self._draw_hind_leg(draw, center_x, ground_y)

        # 5. Torso / Ribcage / Underbelly
        torso_origin = self._draw_torso(draw, center_x, ground_y, breath_y, breath_scale)

        # 6. Dorsal Spikes along spine
        self._draw_dorsal_spikes(draw, torso_origin, breath_y)

        # 7. Forelimb & Front Claws
        self._draw_forelimb(draw, center_x, ground_y, breath_y)

        # 8. Neck, Head, Horns, Eyes, Jaw
        self._draw_head_and_neck(
            draw, torso_origin, head_angle, head_nod, look_shift,
            blink_val, mouth_open_rad, jaw_drop, t
        )

        # 9. Near Wing (Right Wing, in front of back/shoulder)
        self._draw_wing_near(draw, center_x, ground_y + breath_y, wing_flare, wing_y_bob)

        # 10. Armor Plates (Shoulder & Chest carapace)
        if self.state.armor_level > 0:
            self._draw_armor(draw, torso_origin, breath_y)

        return img

    def _draw_shadow(self, draw: ImageDraw.ImageDraw, cx: float, gy: float, w: float, h: float):
        """Draws dynamic cel-shaded action-cartoon contact shadow."""
        scale = self.state.body_scale
        sx = cx - (30 * self.ss)
        sy = gy + (4 * self.ss)
        rx = (190 * self.ss) * scale
        ry = (32 * self.ss) * scale

        # Outer soft shadow
        draw.ellipse(
            [sx - rx, sy - ry, sx + rx, sy + ry],
            fill=(10, 12, 16, 90)
        )
        # Inner dense contact shadow
        draw.ellipse(
            [sx - rx * 0.65, sy - ry * 0.6, sx + rx * 0.65, sy + ry * 0.6],
            fill=(5, 6, 8, 170)
        )

    def _draw_aura(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, t: float, w: float, h: float):
        """Draws radiant streak energy motes and flame wisps around the dragon."""
        intensity = self.state.aura_intensity
        count = int(round(12 * intensity))
        glow_color = hex_to_rgba(self.pal.get("aura", "#FFD13B"), int(130 * intensity))
        core_color = hex_to_rgba(self.pal.get("accent_glow", "#FFFFFF"), int(200 * intensity))

        for i in range(count):
            seed = (i * 47.19)
            prog = (t * 1.5 + (i / max(1, count))) % 1.0
            flame_y = cy + (120 * self.ss) - (prog * (300 * self.ss))
            sway = math.sin(prog * 6.0 + seed) * (35 * self.ss)
            flame_x = cx + math.cos(seed) * (180 * self.ss * self.state.body_scale) + sway
            size = (6.0 * self.ss + math.sin(prog * math.pi) * (8.0 * self.ss)) * (1.0 - prog * 0.5)

            # Diamond spark / flame droplet
            pts = [
                (flame_x, flame_y - size * 1.8),
                (flame_x + size, flame_y),
                (flame_x, flame_y + size * 1.2),
                (flame_x - size, flame_y),
            ]
            draw.polygon([(int(x), int(y)) for x, y in pts], fill=glow_color)
            inner_pts = [
                (flame_x, flame_y - size * 0.9),
                (flame_x + size * 0.5, flame_y),
                (flame_x, flame_y + size * 0.6),
                (flame_x - size * 0.5, flame_y),
            ]
            draw.polygon([(int(x), int(y)) for x, y in inner_pts], fill=core_color)

    def _draw_tail(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, waves: List[float]):
        """
        Draws multi-segment sinuous dragon tail with dorsal spikes, underbelly ridge,
        and evolving tail blade fins.
        """
        scale = self.state.body_scale * self.state.tail_length_multiplier
        t_lvl = self.state.tail_level

        # Hip anchor
        base_x = cx - (90 * self.ss * scale)
        base_y = cy - (110 * self.ss * scale)

        # S-curve spine points from hip extending back and whipping upwards
        p0 = (base_x, base_y)
        p1 = (base_x - (90 * self.ss * scale) + waves[1], base_y + (15 * self.ss) + waves[1] * 0.3)
        p2 = (base_x - (190 * self.ss * scale) + waves[3], base_y - (20 * self.ss) + waves[3] * 0.5)
        p3 = (base_x - (250 * self.ss * scale) + waves[5], base_y - (110 * self.ss * scale) + waves[5] * 0.7)
        p4 = (base_x - (210 * self.ss * scale) + waves[6], base_y - (200 * self.ss * scale) + waves[6])

        spine_pts = cubic_bezier(p0, p1, p2, p3, steps=14) + cubic_bezier(p3, (p3[0]+15, p3[1]-40), (p4[0]-20, p4[1]+30), p4, steps=10)

        # Width tapering from muscular base (36px) to sharp whip tip (4px)
        widths = []
        n_pts = len(spine_pts)
        for i in range(n_pts):
            ratio = i / max(1, n_pts - 1)
            w = (38.0 * self.ss * scale) * (1.0 - ratio * 0.88)
            widths.append(max(2.5 * self.ss, w))

        # Main tail body ribbon
        draw_ribbon(draw, spine_pts, widths, self.c_body, self.c_ink, self.line_w)

        # Cel-shaded underbelly highlight on lower edge
        belly_widths = [w * 0.45 for w in widths]
        draw_ribbon(draw, spine_pts, belly_widths, self.c_belly, None, 0)

        # Dynamic Gold Racing Stripes along tail (Dragon Booster aesthetic!)
        stripe_step = max(3, 16 - t_lvl)
        for i in range(4, n_pts - 4, stripe_step):
            pt = spine_pts[i]
            w = widths[i]
            # Angled chevron mark
            m_pts = [
                (pt[0] - 6 * self.ss, pt[1] - w * 0.5),
                (pt[0] + 10 * self.ss, pt[1]),
                (pt[0] - 4 * self.ss, pt[1] + w * 0.6),
                (pt[0] - 12 * self.ss, pt[1] + w * 0.2),
            ]
            draw.polygon([(int(x), int(y)) for x, y in m_pts], fill=self.c_accent)

        # Tail blade / fins at the tip based on tail_level
        tip = spine_pts[-1]
        tip_prev = spine_pts[-3]
        angle = math.atan2(tip[1] - tip_prev[1], tip[0] - tip_prev[0])
        fin_size = (18.0 * self.ss + (t_lvl * 5.0 * self.ss)) * scale

        # Main tail fin / blade
        f1 = (tip[0] + math.cos(angle + 2.3) * fin_size, tip[1] + math.sin(angle + 2.3) * fin_size)
        f2 = (tip[0] + math.cos(angle) * (fin_size * 1.5), tip[1] + math.sin(angle) * (fin_size * 1.5))
        f3 = (tip[0] + math.cos(angle - 2.3) * fin_size, tip[1] + math.sin(angle - 2.3) * fin_size)
        fin_poly = [tip, f1, f2, f3]
        draw_polygon_with_outline(draw, fin_poly, self.c_horns, self.c_ink, self.line_w)

        # Inner blade gold accent
        if t_lvl >= 2:
            f1_in = (tip[0] + math.cos(angle + 2.3) * (fin_size * 0.6), tip[1] + math.sin(angle + 2.3) * (fin_size * 0.6))
            f2_in = (tip[0] + math.cos(angle) * (fin_size * 0.9), tip[1] + math.sin(angle) * (fin_size * 0.9))
            f3_in = (tip[0] + math.cos(angle - 2.3) * (fin_size * 0.6), tip[1] + math.sin(angle - 2.3) * (fin_size * 0.6))
            draw.polygon([(int(x), int(y)) for x, y in [tip, f1_in, f2_in, f3_in]], fill=self.c_accent)

        # Secondary tail spikes along the upper arch if tail_level >= 3
        if t_lvl >= 3:
            spike_count = min(6, t_lvl)
            for j in range(spike_count):
                idx = 10 + j * 3
                if idx < n_pts:
                    s_pt = spine_pts[idx]
                    s_len = (12.0 + j * 2.0) * self.ss * scale
                    sp_pts = [
                        (s_pt[0] - 5 * self.ss, s_pt[1] - widths[idx]),
                        (s_pt[0] - 12 * self.ss - s_len * 0.5, s_pt[1] - widths[idx] - s_len),
                        (s_pt[0] + 5 * self.ss, s_pt[1] - widths[idx]),
                    ]
                    draw_polygon_with_outline(draw, sp_pts, self.c_spikes, self.c_ink, self.line_w_thin)

    def _draw_hind_leg(self, draw: ImageDraw.ImageDraw, cx: float, gy: float):
        """Draws massive muscular dragon hindquarters, knee, hock, and talons."""
        scale = self.state.body_scale

        hip_x = cx - (80 * self.ss * scale)
        hip_y = gy - (150 * self.ss * scale)

        knee_x = cx - (120 * self.ss * scale)
        knee_y = gy - (75 * self.ss * scale)

        hock_x = cx - (60 * self.ss * scale)
        hock_y = gy - (30 * self.ss * scale)

        foot_x = cx - (45 * self.ss * scale)
        foot_y = gy - (4 * self.ss)

        # Massive muscular thigh polygon
        thigh_poly = [
            (hip_x - 30 * self.ss * scale, hip_y - 20 * self.ss * scale),
            (hip_x + 50 * self.ss * scale, hip_y),
            (knee_x + 60 * self.ss * scale, knee_y + 15 * self.ss * scale),
            (knee_x + 10 * self.ss * scale, knee_y + 35 * self.ss * scale),
            (knee_x - 20 * self.ss * scale, knee_y),
            (hip_x - 45 * self.ss * scale, hip_y - 10 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, thigh_poly, self.c_body, self.c_ink, self.line_w)

        # Cel-shaded thigh muscle highlight
        thigh_hi = [
            (hip_x - 15 * self.ss * scale, hip_y - 10 * self.ss * scale),
            (hip_x + 30 * self.ss * scale, hip_y + 5 * self.ss * scale),
            (knee_x + 35 * self.ss * scale, knee_y + 10 * self.ss * scale),
            (knee_x - 5 * self.ss * scale, knee_y),
        ]
        draw.polygon([(int(x), int(y)) for x, y in thigh_hi], fill=self.c_body_light)

        # Dynamic Gold Action Stripe on thigh
        stripe_poly = [
            (hip_x - 10 * self.ss * scale, hip_y + 5 * self.ss * scale),
            (hip_x + 15 * self.ss * scale, hip_y + 10 * self.ss * scale),
            (knee_x + 25 * self.ss * scale, knee_y + 20 * self.ss * scale),
            (knee_x + 8 * self.ss * scale, knee_y + 18 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, stripe_poly, self.c_accent, self.c_ink, self.line_w_thin)

        # Hock and foot
        hock_poly = [
            (knee_x + 10 * self.ss * scale, knee_y + 25 * self.ss * scale),
            (knee_x + 45 * self.ss * scale, knee_y + 15 * self.ss * scale),
            (hock_x + 20 * self.ss * scale, hock_y),
            (foot_x + 20 * self.ss * scale, foot_y - 6 * self.ss),
            (foot_x - 25 * self.ss * scale, foot_y - 6 * self.ss),
            (hock_x - 15 * self.ss * scale, hock_y),
        ]
        draw_polygon_with_outline(draw, hock_poly, self.c_body_dark, self.c_ink, self.line_w)

        # 3 Sharp talons on foot
        claw_size = (18.0 + self.state.stage_level * 2.5) * self.ss * scale
        for ci, c_offset in enumerate([-16, 2, 20]):
            cx_pos = foot_x + (c_offset * self.ss * scale)
            claw = [
                (cx_pos - 6 * self.ss, foot_y - 6 * self.ss),
                (cx_pos + 6 * self.ss, foot_y - 6 * self.ss),
                (cx_pos + 12 * self.ss + claw_size * 0.4, foot_y + 3 * self.ss),
                (cx_pos - 2 * self.ss, foot_y),
            ]
            draw_polygon_with_outline(draw, claw, self.c_claws, self.c_ink, self.line_w_thin)

    def _draw_torso(self, draw: ImageDraw.ImageDraw, cx: float, gy: float, breath_y: float, breath_scale: float) -> Tuple[float, float]:
        """
        Draws muscular torso, arching ribcage, and armored underbelly.
        Returns: (shoulder_x, shoulder_y) for neck/limb anchoring.
        """
        scale = self.state.body_scale
        base_x = cx
        base_y = gy - (120 * self.ss * scale) + breath_y

        # Pelvis back:
        p_x = base_x - (90 * self.ss * scale)
        p_y = base_y - (20 * self.ss * scale)

        # Shoulder front:
        s_x = base_x + (100 * self.ss * scale)
        s_y = base_y - (70 * self.ss * scale)

        # Chest belly point:
        c_x = base_x + (40 * self.ss * scale)
        c_y = base_y + (40 * self.ss * scale * breath_scale)

        # Main arched torso contour
        spine_curve = cubic_bezier(
            (p_x, p_y),
            (base_x - 40 * self.ss * scale, base_y - 90 * self.ss * scale),
            (base_x + 40 * self.ss * scale, base_y - 100 * self.ss * scale),
            (s_x, s_y),
            steps=12
        )
        belly_curve = cubic_bezier(
            (s_x, s_y),
            (base_x + 90 * self.ss * scale, c_y),
            (base_x - 20 * self.ss * scale, c_y + 10 * self.ss * scale),
            (p_x, p_y),
            steps=12
        )

        torso_poly = spine_curve + belly_curve
        draw_polygon_with_outline(draw, torso_poly, self.c_body, self.c_ink, self.line_w_heavy)

        # Underbelly armored scutes (keeled belly plates)
        underbelly_curve = cubic_bezier(
            (s_x - 10 * self.ss * scale, s_y + 30 * self.ss * scale),
            (base_x + 75 * self.ss * scale, c_y - 10 * self.ss * scale),
            (base_x - 15 * self.ss * scale, c_y),
            (p_x + 10 * self.ss * scale, p_y + 10 * self.ss * scale),
            steps=10
        )
        belly_poly = underbelly_curve + belly_curve
        draw.polygon([(int(x), int(y)) for x, y in belly_poly], fill=self.c_belly)
        draw.line([(int(x), int(y)) for x, y in underbelly_curve], fill=self.c_ink, width=self.line_w_thin)

        # Segmented transverse ridges across belly
        for bi in range(2, len(underbelly_curve) - 2, 2):
            b_top = underbelly_curve[bi]
            b_bot = belly_curve[len(belly_curve) - bi]
            draw.line([(int(b_top[0]), int(b_top[1])), (int(b_bot[0]), int(b_bot[1]))], fill=self.c_body_dark, width=self.line_w_thin)

        # Bold Racing bio-markings on ribcage flank (Homage to Dragon Booster)
        mark_pts = [
            (base_x - 10 * self.ss * scale, base_y - 50 * self.ss * scale),
            (base_x + 35 * self.ss * scale, base_y - 30 * self.ss * scale),
            (base_x + 20 * self.ss * scale, base_y + 5 * self.ss * scale),
            (base_x - 5 * self.ss * scale, base_y - 15 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, mark_pts, self.c_accent, self.c_ink, self.line_w_thin)

        # Secondary slash accent
        mark_pts2 = [
            (base_x + 30 * self.ss * scale, base_y - 55 * self.ss * scale),
            (base_x + 65 * self.ss * scale, base_y - 40 * self.ss * scale),
            (base_x + 55 * self.ss * scale, base_y - 20 * self.ss * scale),
            (base_x + 35 * self.ss * scale, base_y - 35 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, mark_pts2, self.c_accent, self.c_ink, self.line_w_thin)

        return (s_x, s_y)

    def _draw_dorsal_spikes(self, draw: ImageDraw.ImageDraw, shoulder: Tuple[float, float], breath_y: float):
        """Draws sharp dorsal spikes along the dragon's spine based on spike_level."""
        count = self.state.dorsal_spike_count
        if count <= 0:
            return

        scale = self.state.body_scale
        sx, sy = shoulder

        # Spikes along back toward pelvis
        for i in range(count):
            offset_x = - (25.0 * self.ss * scale) - (i * 26.0 * self.ss * scale)
            offset_y = - (12.0 * self.ss * scale) + (i * 6.0 * self.ss * scale)
            h = (18.0 + (count - i) * 3.5) * self.ss * scale

            sp_base_x = sx + offset_x
            sp_base_y = sy + offset_y

            spike = [
                (sp_base_x - 8 * self.ss * scale, sp_base_y),
                (sp_base_x - 16 * self.ss * scale, sp_base_y - h),
                (sp_base_x + 6 * self.ss * scale, sp_base_y + 2 * self.ss * scale),
            ]
            draw_polygon_with_outline(draw, spike, self.c_spikes, self.c_ink, self.line_w_thin)
            # Edge highlight
            draw.line([
                (int(sp_base_x - 16 * self.ss * scale), int(sp_base_y - h)),
                (int(sp_base_x + 6 * self.ss * scale), int(sp_base_y + 2 * self.ss * scale))
            ], fill=self.c_horns_hi, width=int(round(1.5 * self.ss)))

    def _draw_forelimb(self, draw: ImageDraw.ImageDraw, cx: float, gy: float, breath_y: float):
        """Draws muscular front leg, bicep, wrist, and sharp claws gripping ground."""
        scale = self.state.body_scale
        shoulder_x = cx + (90 * self.ss * scale)
        shoulder_y = gy - (175 * self.ss * scale) + breath_y

        elbow_x = cx + (125 * self.ss * scale)
        elbow_y = gy - (95 * self.ss * scale) + breath_y * 0.5

        wrist_x = cx + (115 * self.ss * scale)
        wrist_y = gy - (25 * self.ss * scale)

        foot_x = cx + (125 * self.ss * scale)
        foot_y = gy - (4 * self.ss)

        # Upper arm
        arm_poly = [
            (shoulder_x - 20 * self.ss * scale, shoulder_y),
            (shoulder_x + 30 * self.ss * scale, shoulder_y + 10 * self.ss * scale),
            (elbow_x + 20 * self.ss * scale, elbow_y + 15 * self.ss * scale),
            (elbow_x - 15 * self.ss * scale, elbow_y + 10 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, arm_poly, self.c_body, self.c_ink, self.line_w)

        # Forearm
        fore_poly = [
            (elbow_x - 15 * self.ss * scale, elbow_y + 10 * self.ss * scale),
            (elbow_x + 20 * self.ss * scale, elbow_y + 15 * self.ss * scale),
            (wrist_x + 18 * self.ss * scale, wrist_y),
            (wrist_x - 16 * self.ss * scale, wrist_y),
        ]
        draw_polygon_with_outline(draw, fore_poly, self.c_body_dark, self.c_ink, self.line_w)

        # Gold forearm slash
        slash = [
            (elbow_x + 5 * self.ss * scale, elbow_y + 20 * self.ss * scale),
            (elbow_x + 16 * self.ss * scale, elbow_y + 35 * self.ss * scale),
            (wrist_x + 8 * self.ss * scale, wrist_y - 10 * self.ss * scale),
            (wrist_x, wrist_y - 8 * self.ss * scale),
        ]
        draw.polygon([(int(x), int(y)) for x, y in slash], fill=self.c_accent)

        # Front talons (3 sharp claws)
        claw_size = (16.0 + self.state.stage_level * 2.0) * self.ss * scale
        for ci, c_offset in enumerate([-12, 4, 18]):
            cx_pos = foot_x + (c_offset * self.ss * scale)
            claw = [
                (cx_pos - 5 * self.ss, foot_y - 6 * self.ss),
                (cx_pos + 5 * self.ss, foot_y - 6 * self.ss),
                (cx_pos + 10 * self.ss + claw_size * 0.45, foot_y + 3 * self.ss),
                (cx_pos - 1 * self.ss, foot_y),
            ]
            draw_polygon_with_outline(draw, claw, self.c_claws, self.c_ink, self.line_w_thin)

    def _draw_head_and_neck(
        self,
        draw: ImageDraw.ImageDraw,
        shoulder: Tuple[float, float],
        head_angle: float,
        head_nod: float,
        look_shift: float,
        blink_val: float,
        mouth_open_rad: float,
        jaw_drop: float,
        t: float,
    ):
        """
        Draws the fierce angular action-cartoon dragon head, sweeping horns,
        expressive amber eyes with eyelid animation, neck plates, and powerful jaw.
        """
        scale = self.state.body_scale
        sx, sy = shoulder

        # Neck base at shoulder, arching forward and up
        neck_base = (sx + 20 * self.ss * scale, sy - 10 * self.ss * scale)
        neck_crest = (sx + 80 * self.ss * scale, sy - 90 * self.ss * scale + head_nod * 0.5)
        throat = (sx + 45 * self.ss * scale, sy + 30 * self.ss * scale)
        chin_base = (sx + 120 * self.ss * scale, sy - 40 * self.ss * scale + head_nod * 0.7)

        # Arched neck curve
        neck_top = quadratic_bezier(neck_base, (sx + 40 * self.ss * scale, sy - 90 * self.ss * scale), neck_crest, steps=8)
        neck_bot = quadratic_bezier(chin_base, throat, neck_base, steps=8)
        neck_poly = neck_top + neck_bot
        draw_polygon_with_outline(draw, neck_poly, self.c_body, self.c_ink, self.line_w)

        # Neck scutes / throat plates
        throat_plates = [
            (throat[0] + 15 * self.ss * scale, throat[1] - 20 * self.ss * scale),
            (throat[0] + 45 * self.ss * scale, throat[1] - 50 * self.ss * scale),
            (chin_base[0] - 10 * self.ss * scale, chin_base[1] + 10 * self.ss * scale),
            (chin_base[0] - 25 * self.ss * scale, chin_base[1] + 25 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, throat_plates, self.c_belly, self.c_ink, self.line_w_thin)

        # Neck spikes (nape to skull base)
        if self.state.spike_level >= 1:
            for si in range(min(4, self.state.spike_level + 1)):
                nx = neck_top[si * 2][0]
                ny = neck_top[si * 2][1]
                nsp = [
                    (nx - 5 * self.ss, ny),
                    (nx - 14 * self.ss * scale, ny - (16.0 + si * 3.0) * self.ss * scale),
                    (nx + 5 * self.ss, ny + 3 * self.ss),
                ]
                draw_polygon_with_outline(draw, nsp, self.c_spikes, self.c_ink, self.line_w_thin)

        # Head origin
        head_cx = neck_crest[0] + (30 * self.ss * scale)
        head_cy = neck_crest[1] - (10 * self.ss * scale) + head_nod

        # --- UPPER CRANIUM & SNOUT ---
        # Sharp angular dragon skull (Dragon Booster aesthetic: sleek, aerodynamic, predatory)
        cranium_pts = [
            (head_cx - 45 * self.ss * scale, head_cy - 10 * self.ss * scale),  # Occipital crown
            (head_cx - 10 * self.ss * scale, head_cy - 35 * self.ss * scale),  # Brow ridge start
            (head_cx + 40 * self.ss * scale, head_cy - 22 * self.ss * scale),  # Eye brow hornlet
            (head_cx + 95 * self.ss * scale, head_cy - 10 * self.ss * scale),  # Snout bridge
            (head_cx + 140 * self.ss * scale, head_cy + 5 * self.ss * scale),  # Snout tip / nostril
            (head_cx + 120 * self.ss * scale, head_cy + 22 * self.ss * scale), # Upper lip anterior
            (head_cx + 50 * self.ss * scale, head_cy + 20 * self.ss * scale),  # Mouth corner
            (head_cx, head_cy + 30 * self.ss * scale),                         # Cheek / cheek spike base
        ]
        # Rotate head by head_angle
        cranium_rotated = [rotate_point(pt, (head_cx, head_cy), head_angle) for pt in cranium_pts]
        draw_polygon_with_outline(draw, cranium_rotated, self.c_body, self.c_ink, self.line_w_heavy)

        # Cel-shaded cranium highlight along top snout bridge
        snout_hi = [
            cranium_rotated[1],
            cranium_rotated[2],
            cranium_rotated[3],
            cranium_rotated[4],
            (cranium_rotated[3][0], cranium_rotated[3][1] + 8 * self.ss * scale),
            (cranium_rotated[2][0], cranium_rotated[2][1] + 10 * self.ss * scale),
        ]
        draw.polygon([(int(x), int(y)) for x, y in snout_hi], fill=self.c_body_light)

        # Bold Gold Snout & Brow Crest Markings
        crest_poly = [
            cranium_rotated[1],
            cranium_rotated[2],
            (cranium_rotated[2][0] + 15 * self.ss * scale, cranium_rotated[2][1] + 10 * self.ss * scale),
            (cranium_rotated[1][0] + 15 * self.ss * scale, cranium_rotated[1][1] + 18 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, crest_poly, self.c_accent, self.c_ink, self.line_w_thin)

        # Cheek Spike (angular mandibular hornlet)
        cheek_pt = cranium_rotated[7]
        cheek_spike = [
            (cheek_pt[0] - 10 * self.ss * scale, cheek_pt[1] - 5 * self.ss * scale),
            (cheek_pt[0] - 32 * self.ss * scale, cheek_pt[1] + 14 * self.ss * scale),
            (cheek_pt[0] + 10 * self.ss * scale, cheek_pt[1] + 5 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, cheek_spike, self.c_horns, self.c_ink, self.line_w_thin)

        # --- HORNS ---
        # Sweeping backwards over the neck.
        # Scales dramatically with horn_level (1 to 7) and PR count!
        h_lvl = self.state.horn_level
        horn_base = cranium_rotated[1]
        horn_curve_mult = self.state.horn_curvature
        horn_len = (55.0 + h_lvl * 24.0) * self.ss * scale

        # Main Horn (Swept curve)
        hp0 = horn_base
        hp1 = (horn_base[0] - horn_len * 0.45, horn_base[1] - horn_len * 0.55 * horn_curve_mult)
        hp2 = (horn_base[0] - horn_len * 0.95, horn_base[1] - horn_len * 0.35 * horn_curve_mult)
        main_horn_spine = quadratic_bezier(hp0, hp1, hp2, steps=10)
        horn_widths = [(16.0 * self.ss * scale) * (1.0 - (i / 9.0) * 0.9) for i in range(10)]
        draw_ribbon(draw, main_horn_spine, horn_widths, self.c_horns, self.c_ink, self.line_w)

        # Horn ridge gold stripe / highlight
        if h_lvl >= 2:
            horn_hi_pts = [main_horn_spine[i] for i in range(1, 8)]
            draw.line([(int(x), int(y)) for x, y in horn_hi_pts], fill=self.c_horns_hi, width=int(round(2.5 * self.ss)))

        # Secondary Brow Horns (Unlocked for Adult / Mature / Ancient / Legendary)
        if h_lvl >= 4:
            brow_base = cranium_rotated[2]
            b_len = horn_len * 0.45
            bp1 = (brow_base[0] - b_len * 0.4, brow_base[1] - b_len * 0.6)
            bp2 = (brow_base[0] - b_len * 0.9, brow_base[1] - b_len * 0.4)
            brow_spine = quadratic_bezier(brow_base, bp1, bp2, steps=8)
            b_widths = [(10.0 * self.ss * scale) * (1.0 - (i / 7.0) * 0.9) for i in range(8)]
            draw_ribbon(draw, brow_spine, b_widths, self.c_horns, self.c_ink, self.line_w_thin)

        # Tertiary Crown Spikes for Legendary
        if h_lvl >= 6:
            crown_base = cranium_rotated[0]
            c_len = horn_len * 0.35
            cp = [
                crown_base,
                (crown_base[0] - c_len * 0.8, crown_base[1] - c_len * 0.3),
                (crown_base[0] - 10 * self.ss, crown_base[1] + 15 * self.ss),
            ]
            draw_polygon_with_outline(draw, cp, self.c_spikes, self.c_ink, self.line_w_thin)

        # --- LOWER JAW & TEETH ---
        mouth_corner = cranium_rotated[6]
        jaw_tip = (cranium_rotated[4][0] - 15 * self.ss * scale, cranium_rotated[4][1] + 28 * self.ss * scale + jaw_drop)
        jaw_throat = (cranium_rotated[7][0] + 10 * self.ss * scale, cranium_rotated[7][1] + 15 * self.ss * scale + jaw_drop * 0.6)

        # If mouth open, render inner dark oral cavity and sharp teeth
        if jaw_drop > 4.0 or mouth_open_rad > 0.05:
            oral_cavity = [
                cranium_rotated[5],
                (cranium_rotated[4][0] - 10 * self.ss * scale, cranium_rotated[4][1] + 10 * self.ss * scale),
                jaw_tip,
                mouth_corner
            ]
            draw.polygon([(int(x), int(y)) for x, y in oral_cavity], fill=(40, 10, 15))
            # Upper teeth
            for ti in range(3):
                tx = cranium_rotated[5][0] + (ti * 16 * self.ss * scale)
                ty = cranium_rotated[5][1] + 5 * self.ss * scale
                t_poly = [(tx - 3 * self.ss, ty), (tx, ty + 8 * self.ss * scale), (tx + 3 * self.ss, ty)]
                draw.polygon([(int(x), int(y)) for x, y in t_poly], fill=self.c_claws)

        # Jaw polygon
        jaw_poly = [
            mouth_corner,
            (cranium_rotated[5][0] + 10 * self.ss * scale, cranium_rotated[5][1] + 18 * self.ss * scale + jaw_drop * 0.5),
            jaw_tip,
            (jaw_tip[0] - 25 * self.ss * scale, jaw_tip[1] + 15 * self.ss * scale),
            jaw_throat,
        ]
        draw_polygon_with_outline(draw, jaw_poly, self.c_body_dark, self.c_ink, self.line_w)

        # --- EYE & BLINK ANIMATION ---
        eye_center = (
            head_cx + (32 * self.ss * scale) + look_shift * 0.5,
            head_cy - (5 * self.ss * scale) + head_nod * 0.3
        )
        eye_w = (14.0 * self.ss * scale)
        eye_h = (9.0 * self.ss * scale)

        # Eye socket shadow
        draw.polygon([
            (eye_center[0] - eye_w * 1.3, eye_center[1] - eye_h * 0.8),
            (eye_center[0] + eye_w * 1.4, eye_center[1] - eye_h * 0.4),
            (eye_center[0] + eye_w * 0.8, eye_center[1] + eye_h * 1.2),
            (eye_center[0] - eye_w * 1.1, eye_center[1] + eye_h * 0.6),
        ], fill=(8, 9, 12))

        # Sharp almond eye shape
        eye_pts = [
            (eye_center[0] - eye_w, eye_center[1]),
            (eye_center[0] - eye_w * 0.2, eye_center[1] - eye_h),
            (eye_center[0] + eye_w, eye_center[1] - eye_h * 0.3),
            (eye_center[0] + eye_w * 0.4, eye_center[1] + eye_h * 0.8),
        ]

        if blink_val > 0.08:
            # Sclera / Glowing Iris
            draw.polygon([(int(x), int(y)) for x, y in eye_pts], fill=self.c_eyes)
            # Inner eye glow highlight
            draw.polygon([
                (int(eye_center[0] - eye_w * 0.5), int(eye_center[1] - eye_h * 0.5)),
                (int(eye_center[0] + eye_w * 0.6), int(eye_center[1] - eye_h * 0.2)),
                (int(eye_center[0] + eye_w * 0.1), int(eye_center[1] + eye_h * 0.4)),
            ], fill=self.c_accent_glow)

            # Slit pupil with slight horizontal tracking (look around)
            pupil_x = eye_center[0] + look_shift * 0.6
            pupil_pts = [
                (pupil_x, eye_center[1] - eye_h * 0.85),
                (pupil_x + 2.5 * self.ss, eye_center[1]),
                (pupil_x, eye_center[1] + eye_h * 0.7),
                (pupil_x - 2.5 * self.ss, eye_center[1]),
            ]
            draw.polygon([(int(x), int(y)) for x, y in pupil_pts], fill=self.c_pupil)

            # Eyelid clipping during blink
            if blink_val < 0.95:
                # Eyelid comes down from brow
                drop_y = eye_h * 2.0 * (1.0 - blink_val)
                eyelid = [
                    (eye_center[0] - eye_w * 1.2, eye_center[1] - eye_h * 1.2),
                    (eye_center[0] + eye_w * 1.2, eye_center[1] - eye_h * 1.2),
                    (eye_center[0] + eye_w * 1.2, eye_center[1] - eye_h + drop_y),
                    (eye_center[0] - eye_w * 1.2, eye_center[1] - eye_h + drop_y),
                ]
                draw.polygon([(int(x), int(y)) for x, y in eyelid], fill=self.c_body)
                draw.line([
                    (int(eye_center[0] - eye_w * 1.2), int(eye_center[1] - eye_h + drop_y)),
                    (int(eye_center[0] + eye_w * 1.2), int(eye_center[1] - eye_h + drop_y))
                ], fill=self.c_ink, width=self.line_w_thin)
        else:
            # Completely closed eye slit
            draw.line([
                (int(eye_center[0] - eye_w), int(eye_center[1])),
                (int(eye_center[0] + eye_w), int(eye_center[1] - eye_h * 0.2))
            ], fill=self.c_ink, width=self.line_w)

    def _draw_wing_far(self, draw: ImageDraw.ImageDraw, cx: float, gy: float, flare: float, y_bob: float):
        """Draws the far (left) wing behind the dragon's back."""
        scale = self.state.body_scale * self.state.wing_span_multiplier
        w_lvl = self.state.wing_level

        # Wing root anchor
        root_x = cx - (30 * self.ss * scale)
        root_y = gy - (170 * self.ss * scale) + y_bob

        # Elbow and wrist joints
        elbow_x = root_x - (70 * self.ss * scale)
        elbow_y = root_y - (130 * self.ss * scale) - flare * (80 * self.ss)

        wrist_x = elbow_x - (110 * self.ss * scale)
        wrist_y = elbow_y + (40 * self.ss * scale)

        # Digits / Wing struts
        s1 = (wrist_x - 60 * self.ss * scale, wrist_y + 110 * self.ss * scale)
        s2 = (wrist_x + 10 * self.ss * scale, wrist_y + 140 * self.ss * scale)
        s3 = (wrist_x + 80 * self.ss * scale, wrist_y + 130 * self.ss * scale)

        # Scalloped membrane behind body
        mem_pts = [
            (root_x, root_y),
            (elbow_x, elbow_y),
            (wrist_x, wrist_y),
            s1,
            (s1[0] + 35 * self.ss, s1[1] - 15 * self.ss),
            s2,
            (s2[0] + 35 * self.ss, s2[1] - 15 * self.ss),
            s3,
            (root_x + 20 * self.ss, root_y + 20 * self.ss)
        ]
        # Darker tone for far wing to create deep depth
        far_bone = blend_colors(self.c_wing_bone, (10, 10, 15), 0.4)
        far_mem = blend_colors(self.c_wing_mem, (10, 10, 15), 0.45)
        draw_polygon_with_outline(draw, mem_pts, far_mem, self.c_ink, self.line_w)

        # Bone structure
        draw.line([
            (int(root_x), int(root_y)),
            (int(elbow_x), int(elbow_y)),
            (int(wrist_x), int(wrist_y))
        ], fill=far_bone, width=int(round(6 * self.ss)))

    def _draw_wing_near(self, draw: ImageDraw.ImageDraw, cx: float, gy: float, flare: float, y_bob: float):
        """
        Draws the imposing, near (right) wing attached at the shoulder/back.
        Exhibits sharp action-cartoon anatomy:
        - Heavy humerus & radius bones
        - Carpal thumb claw
        - Elongated strut fingers
        - Dynamic scalloped leathery membranes
        - Bold gold racing markings and membrane folds!
        """
        scale = self.state.body_scale * self.state.wing_span_multiplier
        w_lvl = self.state.wing_level

        # Wing root at scapula
        root_x = cx + (20 * self.ss * scale)
        root_y = gy - (195 * self.ss * scale) + y_bob

        # Elbow joint: arches dramatically upwards and backwards
        elbow_x = root_x - (90 * self.ss * scale)
        elbow_y = root_y - (180 * self.ss * scale) - flare * (120 * self.ss)

        # Wrist joint: angles forward-downward
        wrist_x = elbow_x - (140 * self.ss * scale)
        wrist_y = elbow_y + (50 * self.ss * scale)

        # Wing struts (digits) spanning backward and downward:
        # Strut 1 (longest leading edge)
        d1 = (wrist_x - (100 * self.ss * scale), wrist_y + (160 * self.ss * scale))
        # Strut 2 (middle finger)
        d2 = (wrist_x - (15 * self.ss * scale), wrist_y + (210 * self.ss * scale))
        # Strut 3 (inner finger)
        d3 = (wrist_x + (75 * self.ss * scale), wrist_y + (190 * self.ss * scale))
        # Strut 4 (flank attachment for higher levels)
        d4 = (wrist_x + (150 * self.ss * scale), wrist_y + (150 * self.ss * scale))

        # Scalloped membrane curves between struts
        m1 = (d1[0] + (40 * self.ss * scale), d1[1] - (25 * self.ss * scale))
        m2 = (d2[0] + (45 * self.ss * scale), d2[1] - (25 * self.ss * scale))
        m3 = (d3[0] + (40 * self.ss * scale), d3[1] - (20 * self.ss * scale))

        wing_contour = [
            (root_x, root_y),
            (elbow_x, elbow_y),
            (wrist_x, wrist_y),
            d1,
            m1,
            d2,
            m2,
            d3,
            m3,
            d4,
            (root_x + 40 * self.ss * scale, root_y + 30 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, wing_contour, self.c_wing_mem, self.c_ink, self.line_w_heavy)

        # Cel-shaded inner membrane folds
        inner_fold_1 = [
            (wrist_x, wrist_y),
            (wrist_x - 30 * self.ss * scale, wrist_y + 80 * self.ss * scale),
            d1,
            m1,
            d2,
        ]
        draw.polygon([(int(x), int(y)) for x, y in inner_fold_1], fill=self.c_wing_mem_in)

        # Bold Gold Racing Chevron Markings on Wing Membrane (Dragon Booster aesthetic!)
        # Dynamic bio-stripes that scale with wing_level and stars!
        stripe_alpha = 1.0
        s_count = min(4, 1 + w_lvl // 2)
        for si in range(s_count):
            st_x = wrist_x + (si * 35.0 * self.ss * scale) - (20 * self.ss)
            st_y = wrist_y + (60.0 * self.ss * scale) + (si * 25.0 * self.ss * scale)
            sw = (18.0 * self.ss * scale)
            sh = (45.0 * self.ss * scale)

            chevron = [
                (st_x - sw, st_y),
                (st_x, st_y - sh * 0.4),
                (st_x + sw * 0.6, st_y),
                (st_x, st_y + sh * 0.5),
            ]
            draw_polygon_with_outline(draw, chevron, self.c_accent, self.c_ink, self.line_w_thin)

        # Wing Strut Bones (drawn over the membrane)
        draw.line([(int(wrist_x), int(wrist_y)), (int(d1[0]), int(d1[1]))], fill=self.c_wing_bone, width=int(round(3.5 * self.ss)))
        draw.line([(int(wrist_x), int(wrist_y)), (int(d2[0]), int(d2[1]))], fill=self.c_wing_bone, width=int(round(3.5 * self.ss)))
        draw.line([(int(wrist_x), int(wrist_y)), (int(d3[0]), int(d3[1]))], fill=self.c_wing_bone, width=int(round(3.0 * self.ss)))
        draw.line([(int(wrist_x), int(wrist_y)), (int(d4[0]), int(d4[1]))], fill=self.c_wing_bone, width=int(round(2.5 * self.ss)))

        # Heavy Main Arm Bones (Humerus & Radius)
        arm_pts = [(root_x, root_y), (elbow_x, elbow_y), (wrist_x, wrist_y)]
        draw.line([(int(x), int(y)) for x, y in arm_pts], fill=self.c_wing_bone, width=int(round(8.0 * self.ss)), joint="curve")
        draw.line([(int(x), int(y)) for x, y in arm_pts], fill=self.c_body_light, width=int(round(3.0 * self.ss)), joint="curve")

        # Thumb Carpal Claw on wrist joint
        thumb = [
            (wrist_x - 5 * self.ss, wrist_y - 8 * self.ss),
            (wrist_x - 22 * self.ss * scale, wrist_y - 25 * self.ss * scale),
            (wrist_x + 8 * self.ss, wrist_y - 5 * self.ss),
        ]
        draw_polygon_with_outline(draw, thumb, self.c_claws, self.c_ink, self.line_w_thin)

    def _draw_armor(self, draw: ImageDraw.ImageDraw, shoulder: Tuple[float, float], breath_y: float):
        """
        Draws heavy layered carapace armor plates on shoulders and chest.
        Unlocked and strengthened by merged pull requests!
        """
        scale = self.state.body_scale
        sx, sy = shoulder
        lvl = self.state.armor_level

        # Shoulder Pauldron / Carapace Guard
        p_x = sx + (10 * self.ss * scale)
        p_y = sy - (25 * self.ss * scale)

        pauldron = [
            (p_x - 35 * self.ss * scale, p_y - 15 * self.ss * scale),
            (p_x + 25 * self.ss * scale, p_y - 25 * self.ss * scale),
            (p_x + 40 * self.ss * scale, p_y + 15 * self.ss * scale),
            (p_x - 10 * self.ss * scale, p_y + 35 * self.ss * scale),
            (p_x - 40 * self.ss * scale, p_y + 10 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, pauldron, self.c_armor, self.c_ink, self.line_w)

        # Chiseled armor bevel edge
        draw.line([
            (int(p_x - 35 * self.ss * scale), int(p_y - 15 * self.ss * scale)),
            (int(p_x + 25 * self.ss * scale), int(p_y - 25 * self.ss * scale)),
            (int(p_x + 40 * self.ss * scale), int(p_y + 15 * self.ss * scale))
        ], fill=self.c_armor_edge, width=int(round(2.5 * self.ss)))

        # Gold armor trim / sigil
        sigil = [
            (p_x - 15 * self.ss * scale, p_y - 5 * self.ss * scale),
            (p_x + 15 * self.ss * scale, p_y - 12 * self.ss * scale),
            (p_x + 22 * self.ss * scale, p_y + 5 * self.ss * scale),
            (p_x - 5 * self.ss * scale, p_y + 15 * self.ss * scale),
        ]
        draw_polygon_with_outline(draw, sigil, self.c_accent, self.c_ink, self.line_w_thin)

        # Secondary Chest Carapace Plate for lvl >= 2
        if lvl >= 2:
            cp_x = sx + (35 * self.ss * scale)
            cp_y = sy + (20 * self.ss * scale)
            chest_plate = [
                (cp_x - 20 * self.ss * scale, cp_y - 10 * self.ss * scale),
                (cp_x + 25 * self.ss * scale, cp_y - 5 * self.ss * scale),
                (cp_x + 15 * self.ss * scale, cp_y + 25 * self.ss * scale),
                (cp_x - 25 * self.ss * scale, cp_y + 18 * self.ss * scale),
            ]
            draw_polygon_with_outline(draw, chest_plate, self.c_armor, self.c_ink, self.line_w_thin)

        # Knee Guards for lvl >= 3
        if lvl >= 3:
            k_x = sx - (210 * self.ss * scale)
            k_y = sy + (100 * self.ss * scale)
            knee_plate = [
                (k_x - 12 * self.ss * scale, k_y - 15 * self.ss * scale),
                (k_x + 18 * self.ss * scale, k_y - 8 * self.ss * scale),
                (k_x + 10 * self.ss * scale, k_y + 15 * self.ss * scale),
                (k_x - 15 * self.ss * scale, k_y + 8 * self.ss * scale),
            ]
            draw_polygon_with_outline(draw, knee_plate, self.c_armor, self.c_ink, self.line_w_thin)

