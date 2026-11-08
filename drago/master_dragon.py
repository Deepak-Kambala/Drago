"""
Master Procedural Vector Engine for Drago.
Constructs and renders the exact dragon character from the high-res reference art
with mathematical bezier curves, cel-shading, bold cartoon linework,
and parameterized evolution states (from Egg to Mythic Dragon).
"""

import math
from typing import List, Tuple, Dict, Any, Optional
from PIL import Image, ImageDraw
import numpy as np

Point = Tuple[float, float]

def rot_pt(pt: Point, origin: Point, rad: float) -> Point:
    ox, oy = origin
    px, py = pt
    c, s = math.cos(rad), math.sin(rad)
    return (ox + c * (px - ox) - s * (py - oy), oy + s * (px - ox) + c * (py - oy))

def bez_quad(p0: Point, p1: Point, p2: Point, steps: int = 12) -> List[Point]:
    res = []
    for i in range(steps + 1):
        t = i / steps
        u = 1.0 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        res.append((x, y))
    return res

def bez_cubic(p0: Point, p1: Point, p2: Point, p3: Point, steps: int = 16) -> List[Point]:
    res = []
    for i in range(steps + 1):
        t = i / steps
        u = 1.0 - t
        tt, uu = t * t, u * u
        x = uu * u * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + tt * t * p3[0]
        y = uu * u * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + tt * t * p3[1]
        res.append((x, y))
    return res

class MasterDragonModel:
    """
    Renders every polygon, outline, cel-shade, and marking of the Drago master design.
    """
    def __init__(self, stage_level: int = 6, palette: Optional[Dict[str, str]] = None, ss: int = 2):
        self.stage_level = stage_level  # 1 (Egg) to 13 (Mythic)
        self.ss = ss

        # Authentic palette exact from high-res reference
        self.c_body = (47, 45, 59)         # #2F2D3B Charcoal
        self.c_body_dark = (24, 23, 31)    # #18171F Deep Shadow
        self.c_body_hi = (68, 65, 84)      # #444154 Rim highlight
        self.c_gold = (252, 180, 43)       # #FCB42B Brilliant Gold
        self.c_gold_dark = (201, 134, 22)  # #C98616 Shaded Gold
        self.c_gold_hi = (255, 215, 85)    # #FFD755 Gold highlight
        self.c_belly = (115, 112, 131)     # #737083 Slate throat scutes
        self.c_belly_dark = (75, 72, 88)
        self.c_ink = (0, 0, 0)             # Crisp Black Cartoon Outline
        self.c_eye_red = (230, 25, 55)     # Piercing Crimson Eye
        self.c_teeth = (250, 250, 255)     # Ivory white teeth

        # Line widths
        self.lw_heavy = int(round(4.0 * self.ss))
        self.lw_mid = int(round(2.6 * self.ss))
        self.lw_fine = int(round(1.6 * self.ss))

    def _draw_poly(self, draw: ImageDraw.ImageDraw, pts: List[Point], fill, outline=None, width=None):
        if len(pts) < 3:
            return
        int_pts = [(int(round(x)), int(round(y))) for x, y in pts]
        draw.polygon(int_pts, fill=fill)
        if outline:
            w = width or self.lw_mid
            draw.line(int_pts + [int_pts[0]], fill=outline, width=w, joint="curve")

    def _draw_ribbon(self, draw: ImageDraw.ImageDraw, curve: List[Point], widths: List[float], fill, outline=None, width=None):
        if len(curve) < 2:
            return
        left, right = [], []
        n = len(curve)
        for i in range(n):
            curr = curve[i]
            w = widths[i] if i < len(widths) else widths[-1]
            if i == 0:
                dx, dy = curve[1][0] - curr[0], curve[1][1] - curr[1]
            elif i == n - 1:
                dx, dy = curr[0] - curve[n - 2][0], curr[1] - curve[n - 2][1]
            else:
                dx, dy = curve[i + 1][0] - curve[i - 1][0], curve[i + 1][1] - curve[i - 1][1]
            dist = math.hypot(dx, dy)
            if dist < 1e-4:
                nx, ny = 0.0, 1.0
            else:
                nx, ny = -dy / dist, dx / dist
            left.append((curr[0] + nx * w, curr[1] + ny * w))
            right.append((curr[0] - nx * w, curr[1] - ny * w))
        poly = left + list(reversed(right))
        self._draw_poly(draw, poly, fill, outline, width)

    def render(self, width: int, height: int, t: float = 0.0, action: str = "idle") -> Image.Image:
        """
        Renders the full procedural dragon frame at supersampled resolution.
        """
        w = width * self.ss
        h = height * self.ss

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Base scale factor: normalized to 1024x682 reference canvas
        ref_w, ref_h = 1024.0, 682.0
        # Fit comfortably in the frame
        scale = min(w / ref_w, h / ref_h) * 1.15
        
        # Center anchor (grounded)
        ox = (w - ref_w * scale) * 0.5 + (10 * self.ss)
        oy = (h - ref_h * scale) * 0.5 + (35 * self.ss)

        # Transformation helper
        def p(rx: float, ry: float) -> Point:
            return (ox + rx * scale, oy + ry * scale)

        t_rad = 2.0 * math.pi * t

        # Kinematic Motion Variables
        # 1. Breathing
        breath_y = math.sin(t_rad) * (3.5 * self.ss)
        breath_chest = 1.0 + math.sin(t_rad) * 0.025

        # 2. Tail wave
        tail_wave = [math.sin(t_rad - i * 0.6) * (6.0 * self.ss * (1.0 + i * 0.3)) for i in range(8)]

        # 3. Wing flap
        wing_flare = math.sin(t_rad + 0.8) * 0.05
        wing_y = math.sin(t_rad + 0.8) * (5.0 * self.ss)

        # 4. Head nod
        head_nod = math.sin(t_rad + 0.4) * (3.0 * self.ss)

        # 5. Eye blink (at t in [0.65, 0.78])
        blink = 1.0
        if 0.65 <= t <= 0.78:
            rel = (t - 0.65) / 0.13
            blink = abs(math.cos(rel * math.pi))

        # --- EGG FORM (Level 1) ---
        if self.stage_level == 1:
            self._render_egg(draw, p, t_rad)
            return img

        # --- DRAGON FORMS (Levels 2 - 13) ---
        # Draw in precise Z-order (Back to Front):
        # 1. Cosmic Aura Background (Levels 12 & 13)
        if self.stage_level >= 12:
            self._draw_cosmic_aura(draw, p, t_rad)

        # 2. Far Wing (Left Wing, behind body)
        self._draw_far_wing(draw, p, wing_y, wing_flare)

        # 3. Tail & Tail Blade
        self._draw_tail(draw, p, tail_wave)

        # 4. Hind Leg & Golden Claws
        self._draw_hind_leg(draw, p)

        # 5. Torso & Slate Throat Scutes
        self._draw_torso(draw, p, breath_y, breath_chest)

        # 6. Dorsal Spine Spikes
        self._draw_dorsal_spikes(draw, p, breath_y)

        # 7. Forelimb & Front Golden Talons
        self._draw_forelimb(draw, p, breath_y)

        # 8. Neck, Head, Horns, Jaws & Crimson Eye
        self._draw_head_and_neck(draw, p, head_nod, blink, breath_y)

        # 9. Near Wing (Right Wing, magnificent arched gold membrane)
        self._draw_near_wing(draw, p, wing_y, wing_flare)

        # 10. Foreground Energy Crystals (Level 12 & 13)
        if self.stage_level >= 12:
            self._draw_floating_crystals(draw, p, t_rad)

        return img

    def _render_egg(self, draw: ImageDraw.ImageDraw, p, t_rad: float):
        """Draws the obsidian dragon egg with glowing gold veins and rocking motion."""
        rock = math.sin(t_rad) * 0.08
        center = p(512, 380)
        ew, eh = (60 * self.ss), (85 * self.ss)

        # Rocking transform
        pts = []
        for a in np.linspace(0, 2 * math.pi, 36):
            ex = math.cos(a) * ew
            ey = math.sin(a) * eh
            rx = ex * math.cos(rock) - ey * math.sin(rock) + center[0]
            ry = ex * math.sin(rock) + ey * math.cos(rock) + center[1]
            pts.append((rx, ry))

        # Shadow
        draw.ellipse([center[0] - ew * 1.2, center[1] + eh * 0.7, center[0] + ew * 1.2, center[1] + eh * 1.0], fill=(5, 6, 8, 140))
        # Egg shell
        self._draw_poly(draw, pts, self.c_body_dark, self.c_ink, self.lw_heavy)
        # Gold veins
        pulse = 0.5 + 0.5 * math.sin(t_rad)
        v_color = (int(252 * pulse), int(180 * pulse), int(43 * pulse))
        v1 = [p(500, 340), p(515, 370), p(490, 400), p(520, 430)]
        draw.line(v1, fill=v_color, width=self.lw_mid, joint="curve")

    def _draw_far_wing(self, draw: ImageDraw.ImageDraw, p, wy: float, flare: float):
        """Draws the rear (left) wing behind the neck and chest."""
        # Scale with stage
        w_scale = 0.65 + (self.stage_level / 13.0) * 0.45
        root = p(650, 240 + wy)
        elbow = p(600 - 40 * w_scale, 80 - 60 * w_scale - flare * 50)
        wrist = p(480 - 80 * w_scale, 120 - 40 * w_scale)
        tip = p(380 - 100 * w_scale, 200)

        # Darker shaded tone for rear wing
        c_far_bone = (24, 23, 31)
        c_far_mem = (180, 125, 20)

        mem = [root, elbow, wrist, tip, p(460, 220), p(550, 240)]
        self._draw_poly(draw, mem, c_far_mem, self.c_ink, self.lw_mid)
        self._draw_ribbon(draw, [root, elbow, wrist], [12 * self.ss, 10 * self.ss, 7 * self.ss], c_far_bone, self.c_ink, self.lw_mid)

    def _draw_tail(self, draw: ImageDraw.ImageDraw, p, waves: List[float]):
        """
        Draws the long sinuous tail matching the master reference:
        curves downward to ground level and swoops upward into a golden crescent blade.
        """
        # Tail spine control points from hip (480, 480) down-left to tip
        w0, w1, w2, w3, w4 = waves[0], waves[1], waves[2], waves[3], waves[4]
        
        c0 = p(450, 480)
        c1 = p(350 + w0, 520 + w0 * 0.4)
        c2 = p(240 + w1, 540 + w1 * 0.6)
        c3 = p(160 + w2, 510 + w2 * 0.8)
        c4 = p(100 + w3, 460 + w3)

        tail_curve = bez_cubic(c0, c1, c2, c3, steps=12) + bez_quad(c3, p(120 + w4, 480), c4, steps=8)
        n = len(tail_curve)

        # Widths: muscular hip (42px) tapering to agile whip tip (6px)
        widths = [(40.0 * self.ss) * (1.0 - (i / n) * 0.82) for i in range(n)]

        # Tail body
        self._draw_ribbon(draw, tail_curve, widths, self.c_body, self.c_ink, self.lw_heavy)

        # Dynamic Gold Racing Stripe along the side of the tail
        gold_stripe = [tail_curve[i] for i in range(2, n - 3)]
        gold_widths = [w * 0.45 for w in widths[2:n-3]]
        self._draw_ribbon(draw, gold_stripe, gold_widths, self.c_gold, self.c_ink, self.lw_fine)

        # Dorsal Spikes along the tail top ridge (Yellow with dark bases)
        for ti in range(3, n - 3, 2):
            pt = tail_curve[ti]
            w_val = widths[ti]
            sp_len = (18.0 + (n - ti) * 0.8) * self.ss
            # Perpendicular spike angle pointing up-left
            sp_poly = [
                (pt[0] - 8 * self.ss, pt[1] - w_val * 0.5),
                (pt[0] - 14 * self.ss, pt[1] - w_val - sp_len),
                (pt[0] + 6 * self.ss, pt[1] - w_val * 0.8),
            ]
            self._draw_poly(draw, sp_poly, self.c_gold, self.c_ink, self.lw_fine)

        # --- CRESCENT BLADE TAIL FIN AT TIP ---
        tip = tail_curve[-1]
        fin_poly = [
            tip,
            (tip[0] + 15 * self.ss, tip[1] - 25 * self.ss),
            (tip[0] - 45 * self.ss, tip[1] - 5 * self.ss),
            (tip[0] - 65 * self.ss, tip[1] + 20 * self.ss),
            (tip[0] - 15 * self.ss, tip[1] + 12 * self.ss),
        ]
        self._draw_poly(draw, fin_poly, self.c_gold, self.c_ink, self.lw_mid)
        # Inner black blade core
        fin_core = [
            tip,
            (tip[0] + 5 * self.ss, tip[1] - 12 * self.ss),
            (tip[0] - 30 * self.ss, tip[1]),
            (tip[0] - 10 * self.ss, tip[1] + 8 * self.ss),
        ]
        self._draw_poly(draw, fin_core, self.c_body_dark, None, 0)

    def _draw_hind_leg(self, draw: ImageDraw.ImageDraw, p):
        """
        Draws the muscular dragon hind leg with the signature gold hook tribal marking,
        golden lower leg, and 3 sharp curved golden talons.
        """
        hip = p(490, 440)
        knee = p(430, 520)
        hock = p(465, 580)
        foot = p(440, 630)

        # Massive muscular thigh
        thigh = [
            hip,
            p(545, 480),
            p(510, 555),
            (knee[0] + 30 * self.ss, knee[1] + 20 * self.ss),
            knee,
            p(450, 460),
        ]
        self._draw_poly(draw, thigh, self.c_body, self.c_ink, self.lw_heavy)

        # Signature Gold Tribal Hook / Flame Marking on Thigh
        flame = [
            p(485, 490),
            p(535, 520),
            p(515, 560),
            p(485, 545),
            p(500, 525),
            p(475, 510),
        ]
        self._draw_poly(draw, flame, self.c_gold, self.c_ink, self.lw_fine)

        # Hock & Lower Leg (Brilliant Gold)
        hock_poly = [
            knee,
            (knee[0] + 45 * self.ss, knee[1] + 15 * self.ss),
            (foot[0] + 35 * self.ss, foot[1] - 12 * self.ss),
            foot,
            hock,
        ]
        self._draw_poly(draw, hock_poly, self.c_gold, self.c_ink, self.lw_mid)

        # Foot with 3 Golden Talons
        for ci, cx_off in enumerate([-20, 5, 30]):
            claw_base = (foot[0] + cx_off * self.ss, foot[1] - 10 * self.ss)
            claw = [
                (claw_base[0] - 8 * self.ss, claw_base[1]),
                (claw_base[0] + 8 * self.ss, claw_base[1]),
                (claw_base[0] + 16 * self.ss, claw_base[1] + 24 * self.ss),
                (claw_base[0] - 2 * self.ss, claw_base[1] + 20 * self.ss),
            ]
            self._draw_poly(draw, claw, self.c_gold, self.c_ink, self.lw_fine)

    def _draw_torso(self, draw: ImageDraw.ImageDraw, p, by: float, bc: float):
        """Draws the muscular arched torso, segmented slate throat scutes, and flank markings."""
        pelvis = p(450, 460)
        chest = p(650, 470 + by * 0.5)
        shoulder = p(720, 420 + by)

        # Muscular back line
        spine = bez_cubic(pelvis, p(520, 390 + by), p(620, 380 + by), shoulder, steps=10)
        # Belly curve
        belly = bez_cubic(shoulder, p(680, 560 * bc), p(530, 550 * bc), pelvis, steps=10)

        torso = spine + belly
        self._draw_poly(draw, torso, self.c_body, self.c_ink, self.lw_heavy)

        # Segmented Throat & Underbelly Scutes (Slate #737083)
        throat_pts = [
            p(740, 320 + by),
            p(785, 370 + by),
            p(770, 430 + by),
            p(745, 510),
            p(715, 540),
            p(700, 460),
            p(720, 380 + by),
        ]
        self._draw_poly(draw, throat_pts, self.c_belly, self.c_ink, self.lw_mid)

        # Transverse plate ridges across throat scutes
        for ti in range(4):
            y_pos = 360 + ti * 40 + by * 0.6
            p1 = p(725 + ti * 5, y_pos)
            p2 = p(775 - ti * 8, y_pos + 12)
            draw.line([p1, p2], fill=self.c_ink, width=self.lw_mid)

        # Flank Gold Chevron / Tribal Lightning Strike
        flank = [
            p(590, 420 + by),
            p(655, 450 + by),
            p(630, 495),
            p(605, 475),
            p(625, 455 + by),
            p(595, 440 + by),
        ]
        self._draw_poly(draw, flank, self.c_gold, self.c_ink, self.lw_fine)

    def _draw_dorsal_spikes(self, draw: ImageDraw.ImageDraw, p, by: float):
        """Draws the prominent yellow triangular dorsal crest spikes along back and neck."""
        # Spikes along back between shoulder and pelvis
        for i in range(7):
            x_b = 680 - i * 36
            y_b = 390 - i * 3 + by
            h_sp = (26.0 - i * 1.5) * self.ss
            spike = [
                p(x_b - 12, y_b),
                p(x_b - 20, y_b - h_sp / self.ss),
                p(x_b + 6, y_b + 4),
            ]
            self._draw_poly(draw, spike, self.c_gold, self.c_ink, self.lw_fine)

    def _draw_forelimb(self, draw: ImageDraw.ImageDraw, p, by: float):
        """
        Draws muscular front leg, massive black shoulder pauldron with gold V-chevron,
        and 3 sharp golden talons.
        """
        shoulder = p(710, 410 + by)
        elbow = p(730, 500 + by * 0.5)
        wrist = p(750, 580)
        foot = p(740, 630)

        # Arm musculature
        arm = [
            shoulder,
            p(765, 430 + by),
            p(780, 510),
            p(775, 590),
            (foot[0] + 45 * self.ss, foot[1] - 8 * self.ss),
            foot,
            wrist,
            elbow,
        ]
        self._draw_poly(draw, arm, self.c_body, self.c_ink, self.lw_heavy)

        # Shoulder Pauldron Armor with Bold Gold V-Chevron
        pauldron = [
            p(690, 415 + by),
            p(745, 405 + by),
            p(760, 465 + by),
            p(715, 490 + by),
            p(685, 455 + by),
        ]
        self._draw_poly(draw, pauldron, self.c_body_dark, self.c_ink, self.lw_mid)

        # Gold V-Chevron on Shoulder
        v_chev = [
            p(705, 425 + by),
            p(745, 435 + by),
            p(730, 470 + by),
            p(715, 455 + by),
        ]
        self._draw_poly(draw, v_chev, self.c_gold, self.c_ink, self.lw_fine)

        # Gold Forearm Armor Stripe
        fore_stripe = [
            p(725, 515),
            p(765, 530),
            p(750, 575),
            p(725, 560),
        ]
        self._draw_poly(draw, fore_stripe, self.c_gold, self.c_ink, self.lw_fine)

        # 3 Sharp Curved Golden Talons
        for ci, cx_off in enumerate([-25, 8, 42]):
            c_base = (foot[0] + cx_off * self.ss, foot[1] - 8 * self.ss)
            claw = [
                (c_base[0] - 10 * self.ss, c_base[1]),
                (c_base[0] + 10 * self.ss, c_base[1]),
                (c_base[0] + 20 * self.ss, c_base[1] + 28 * self.ss),
                (c_base[0] - 2 * self.ss, c_base[1] + 22 * self.ss),
            ]
            self._draw_poly(draw, claw, self.c_gold, self.c_ink, self.lw_fine)

    def _draw_head_and_neck(self, draw: ImageDraw.ImageDraw, p, h_nod: float, blink: float, by: float):
        """
        Draws the majestic dragon skull: long snout, sweeping golden horns,
        parted jaws with sharp ivory teeth, and fierce crimson eye.
        """
        # Neck curving up and forward
        n_base = p(680, 360 + by)
        n_crest = p(760, 220 + h_nod)
        throat = p(755, 340 + by)
        chin = p(830, 260 + h_nod)

        neck_top = bez_quad(n_base, p(710, 240 + h_nod), n_crest, steps=8)
        neck_bot = bez_quad(chin, throat, p(720, 390 + by), steps=8)
        self._draw_poly(draw, neck_top + neck_bot, self.c_body, self.c_ink, self.lw_heavy)

        # Gold Neck Crest Spikes (along back of neck)
        for si in range(4):
            nx, ny = n_base[0] + (n_crest[0] - n_base[0]) * (si / 4.0), n_base[1] + (n_crest[1] - n_base[1]) * (si / 4.0)
            nsp = [
                (nx - 8 * self.ss, ny),
                (nx - 24 * self.ss, ny - (20.0 + si * 4.0) * self.ss),
                (nx + 8 * self.ss, ny + 2 * self.ss),
            ]
            self._draw_poly(draw, nsp, self.c_gold, self.c_ink, self.lw_fine)

        # --- HEAD / CRANIUM ---
        c_x, c_y = n_crest[0], n_crest[1]

        # Angular dragon cranium
        snout_tip = (c_x + 130 * self.ss, c_y + 35 * self.ss)
        jaw_corner = (c_x + 55 * self.ss, c_y + 55 * self.ss)
        brow_ridge = (c_x + 40 * self.ss, c_y - 25 * self.ss)

        cranium = [
            (c_x - 30 * self.ss, c_y - 5 * self.ss),
            brow_ridge,
            (c_x + 85 * self.ss, c_y - 5 * self.ss),
            snout_tip,
            (snout_tip[0] - 20 * self.ss, snout_tip[1] + 20 * self.ss),
            jaw_corner,
            (c_x + 15 * self.ss, c_y + 40 * self.ss),
        ]
        self._draw_poly(draw, cranium, self.c_body, self.c_ink, self.lw_heavy)

        # Gold Forehead Crest & Snout Markings
        crest = [
            brow_ridge,
            (c_x + 75 * self.ss, c_y - 8 * self.ss),
            (c_x + 65 * self.ss, c_y + 10 * self.ss),
            (c_x + 20 * self.ss, c_y + 5 * self.ss),
        ]
        self._draw_poly(draw, crest, self.c_gold, self.c_ink, self.lw_fine)

        # --- HORNS ---
        # Sweeping Main Horn (Bright Gold with black base, pointing back-upwards)
        h_len = (85.0 + self.stage_level * 12.0) * self.ss
        h0 = brow_ridge
        h1 = (brow_ridge[0] - h_len * 0.45, brow_ridge[1] - h_len * 0.55)
        h2 = (brow_ridge[0] - h_len * 0.95, brow_ridge[1] - h_len * 0.35)
        horn_spine = bez_quad(h0, h1, h2, steps=10)
        horn_widths = [(18.0 * self.ss) * (1.0 - (i / 10.0) * 0.88) for i in range(11)]
        self._draw_ribbon(draw, horn_spine, horn_widths, self.c_gold, self.c_ink, self.lw_mid)
        # Horn black base root
        self._draw_ribbon(draw, horn_spine[:4], horn_widths[:4], self.c_body_dark, self.c_ink, self.lw_fine)

        # Secondary Brow Horn
        b_len = h_len * 0.42
        bp0 = (brow_ridge[0] + 15 * self.ss, brow_ridge[1] + 5 * self.ss)
        bp1 = (bp0[0] - b_len * 0.5, bp0[1] - b_len * 0.6)
        bp2 = (bp0[0] - b_len * 0.9, bp0[1] - b_len * 0.35)
        brow_spine = bez_quad(bp0, bp1, bp2, steps=8)
        self._draw_ribbon(draw, brow_spine, [(11 * self.ss) * (1.0 - i/8.0 * 0.85) for i in range(9)], self.c_gold, self.c_ink, self.lw_fine)

        # Cheek Spike (Mandibular hornlet)
        cheek_spike = [
            (c_x + 20 * self.ss, c_y + 30 * self.ss),
            (c_x - 15 * self.ss, c_y + 50 * self.ss),
            (c_x + 35 * self.ss, c_y + 45 * self.ss),
        ]
        self._draw_poly(draw, cheek_spike, self.c_gold, self.c_ink, self.lw_fine)

        # Lower Jaw & Sharp Teeth
        jaw_tip = (snout_tip[0] - 15 * self.ss, snout_tip[1] + 25 * self.ss)
        jaw = [
            jaw_corner,
            (snout_tip[0] - 10 * self.ss, snout_tip[1] + 15 * self.ss),
            jaw_tip,
            (jaw_tip[0] - 25 * self.ss, jaw_tip[1] + 18 * self.ss),
            (c_x + 35 * self.ss, c_y + 55 * self.ss),
        ]
        self._draw_poly(draw, jaw, self.c_body_dark, self.c_ink, self.lw_mid)

        # Sharp White Teeth
        for ti in range(3):
            tx = jaw_corner[0] + 20 * self.ss + ti * 16 * self.ss
            ty = jaw_corner[1] - 5 * self.ss
            tooth = [(tx - 3 * self.ss, ty), (tx, ty + 8 * self.ss), (tx + 3 * self.ss, ty)]
            draw.polygon([(int(x), int(y)) for x, y in tooth], fill=self.c_teeth)

        # Golden Chin Crest
        chin_crest = [
            (jaw_tip[0] - 15 * self.ss, jaw_tip[1] + 10 * self.ss),
            (jaw_tip[0] - 35 * self.ss, jaw_tip[1] + 32 * self.ss),
            (jaw_tip[0] - 5 * self.ss, jaw_tip[1] + 18 * self.ss),
        ]
        self._draw_poly(draw, chin_crest, self.c_gold, self.c_ink, self.lw_fine)

        # --- PIERCING CRIMSON EYE & BLINK ---
        eye_cx = c_x + 55 * self.ss
        eye_cy = c_y - 2 * self.ss
        ew, eh = 12 * self.ss, 7 * self.ss

        if blink > 0.1:
            eye_poly = [
                (eye_cx - ew, eye_cy),
                (eye_cx - ew * 0.2, eye_cy - eh),
                (eye_cx + ew, eye_cy - eh * 0.3),
                (eye_cx + ew * 0.4, eye_cy + eh * 0.8),
            ]
            self._draw_poly(draw, eye_poly, self.c_eye_red, self.c_ink, self.lw_fine)
            # Slit Pupil
            pupil = [
                (eye_cx, eye_cy - eh * 0.8),
                (eye_cx + 2 * self.ss, eye_cy),
                (eye_cx, eye_cy + eh * 0.7),
                (eye_cx - 2 * self.ss, eye_cy),
            ]
            draw.polygon([(int(x), int(y)) for x, y in pupil], fill=(0, 0, 0))
            if blink < 0.95:
                # Eyelid closure
                drop = eh * 2.0 * (1.0 - blink)
                eyelid = [
                    (eye_cx - ew * 1.2, eye_cy - eh * 1.2),
                    (eye_cx + ew * 1.2, eye_cy - eh * 1.2),
                    (eye_cx + ew * 1.2, eye_cy - eh + drop),
                    (eye_cx - ew * 1.2, eye_cy - eh + drop),
                ]
                draw.polygon([(int(x), int(y)) for x, y in eyelid], fill=self.c_body)
        else:
            draw.line([(int(eye_cx - ew), int(eye_cy)), (int(eye_cx + ew), int(eye_cy))], fill=self.c_ink, width=self.lw_mid)

    def _draw_near_wing(self, draw: ImageDraw.ImageDraw, p, wy: float, flare: float):
        """
        Draws the magnificent foreground wing:
        Heavy curved black humerus/radius leading arm with gold racing stripe,
        3 deep scalloped gold wing membranes, and thumb carpal spike.
        """
        # Wing root at shoulder/back
        root = p(670, 280 + wy)
        elbow = p(650, 80 + wy * 0.5 - flare * 60)
        wrist = p(460, 110 - flare * 30)

        # 3 elongated strut fingers arching downward-backward
        d1 = p(100, 360)  # Longest leading strut tip
        d2 = p(260, 480)  # Middle strut tip
        d3 = p(400, 470)  # Inner strut tip
        d4 = p(580, 410)  # Body attachment

        # Scalloped membrane arches
        m1 = p(180, 430)
        m2 = p(330, 490)
        m3 = p(490, 450)

        # Full wing membrane polygon
        wing_mem = [
            root, elbow, wrist,
            d1, m1, d2, m2, d3, m3, d4
        ]
        self._draw_poly(draw, wing_mem, self.c_gold, self.c_ink, self.lw_heavy)

        # Inner membrane shading folds (Gold Shade #C98616)
        fold1 = [wrist, p(180, 240), d1, m1, d2]
        self._draw_poly(draw, fold1, self.c_gold_dark, None, 0)
        fold2 = [wrist, p(320, 290), d2, m2, d3]
        self._draw_poly(draw, fold2, self.c_gold_dark, None, 0)

        # Wing Struts (Dark Bones running to finger tips)
        draw.line([wrist, d1], fill=self.c_body_dark, width=self.lw_mid)
        draw.line([wrist, d2], fill=self.c_body_dark, width=self.lw_mid)
        draw.line([wrist, d3], fill=self.c_body_dark, width=self.lw_fine)

        # Heavy Main Arm Bone (Curved black spar from root to wrist)
        arm_pts = bez_quad(root, elbow, wrist, steps=12)
        arm_widths = [(22.0 * self.ss) * (1.0 - (i / 12.0) * 0.5) for i in range(13)]
        self._draw_ribbon(draw, arm_pts, arm_widths, self.c_body, self.c_ink, self.lw_heavy)

        # Gold Racing Stripe along the top edge of the wing spar
        gold_arm = [arm_pts[i] for i in range(1, 11)]
        self._draw_ribbon(draw, gold_arm, [w * 0.4 for w in arm_widths[1:11]], self.c_gold, self.c_ink, self.lw_fine)

        # Thumb Carpal Claw on wrist joint
        thumb = [
            (wrist[0] - 6 * self.ss, wrist[1] - 8 * self.ss),
            (wrist[0] - 30 * self.ss, wrist[1] - 25 * self.ss),
            (wrist[0] + 8 * self.ss, wrist[1] - 5 * self.ss),
        ]
        self._draw_poly(draw, thumb, self.c_gold, self.c_ink, self.lw_fine)

    def _draw_cosmic_aura(self, draw: ImageDraw.ImageDraw, p, t_rad: float):
        """Radiant celestial energy rings and shimmering flames for Mythic form."""
        center = p(512, 380)
        pulse = 1.0 + math.sin(t_rad * 2.0) * 0.08
        rad_x = (320 * self.ss) * pulse
        rad_y = (190 * self.ss) * pulse

        # Multi-layer golden celestial ring
        draw.ellipse([center[0] - rad_x, center[1] - rad_y, center[0] + rad_x, center[1] + rad_y], outline=(252, 180, 43, 160), width=int(round(4 * self.ss)))
        draw.ellipse([center[0] - rad_x * 0.9, center[1] - rad_y * 0.9, center[0] + rad_x * 0.9, center[1] + rad_y * 0.9], outline=(255, 230, 120, 110), width=int(round(2 * self.ss)))

    def _draw_floating_crystals(self, draw: ImageDraw.ImageDraw, p, t_rad: float):
        """Floating celestial diamond star crystals orbiting the dragon."""
        c_pos = [
            (180, 420, 0.0),
            (280, 560, 1.8),
            (760, 480, 3.2),
            (880, 390, 4.5),
        ]
        for bx, by, phase in c_pos:
            cy_shift = math.sin(t_rad * 1.5 + phase) * (14.0 * self.ss)
            c_center = p(bx, by)
            c_y = c_center[1] + cy_shift
            cw, ch = 10 * self.ss, 22 * self.ss
            crystal = [
                (c_center[0], c_y - ch),
                (c_center[0] + cw, c_y),
                (c_center[0], c_y + ch),
                (c_center[0] - cw, c_y),
            ]
            self._draw_poly(draw, crystal, (255, 240, 160), self.c_ink, self.lw_fine)
