"""
Geometry and rendering primitives for Drago vector cartoon engine.
Provides Bezier curve generation, polygon transforms, antialiased polygon drawing,
and color shading utilities.
"""

import math
from typing import List, Tuple, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageColor

Point = Tuple[float, float]

def rotate_point(pt: Point, origin: Point, angle_rad: float) -> Point:
    """Rotates a 2D point around an origin by angle in radians."""
    ox, oy = origin
    px, py = pt
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    qx = ox + cos_a * (px - ox) - sin_a * (py - oy)
    qy = oy + sin_a * (px - ox) + cos_a * (py - oy)
    return (qx, qy)

def translate_point(pt: Point, dx: float, dy: float) -> Point:
    return (pt[0] + dx, pt[1] + dy)

def scale_point(pt: Point, origin: Point, scale_x: float, scale_y: float) -> Point:
    ox, oy = origin
    return (ox + (pt[0] - ox) * scale_x, oy + (pt[1] - oy) * scale_y)

def quadratic_bezier(p0: Point, p1: Point, p2: Point, steps: int = 12) -> List[Point]:
    """Generates points along a quadratic Bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1.0 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts

def cubic_bezier(p0: Point, p1: Point, p2: Point, p3: Point, steps: int = 16) -> List[Point]:
    """Generates points along a cubic Bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1.0 - t
        tt = t * t
        uu = u * u
        uui = 3 * uu * t
        utt = 3 * u * tt
        x = uu * u * p0[0] + uui * p1[0] + utt * p2[0] + tt * t * p3[0]
        y = uu * u * p0[1] + uui * p1[1] + utt * p2[1] + tt * t * p3[1]
        pts.append((x, y))
    return pts

def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code.lstrip('#')
    if len(hex_code) == 3:
        hex_code = "".join([c * 2 for c in hex_code])
    return (
        int(hex_code[0:2], 16),
        int(hex_code[2:4], 16),
        int(hex_code[4:6], 16),
    )

def hex_to_rgba(hex_code: str, alpha: int = 255) -> Tuple[int, int, int, int]:
    r, g, b = hex_to_rgb(hex_code)
    return (r, g, b, alpha)

def blend_colors(c1: Tuple[int, int, int], c2: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """Linear blend between two RGB colors (factor 0.0 to 1.0)."""
    factor = max(0.0, min(1.0, factor))
    return (
        int(c1[0] * (1.0 - factor) + c2[0] * factor),
        int(c1[1] * (1.0 - factor) + c2[1] * factor),
        int(c1[2] * (1.0 - factor) + c2[2] * factor),
    )

def draw_polygon_with_outline(
    draw: ImageDraw.ImageDraw,
    points: List[Point],
    fill_color: Any,
    outline_color: Optional[Any] = None,
    outline_width: int = 3,
):
    """Draws a polygon with optional thick cartoon outline."""
    if len(points) < 3:
        return
    int_pts = [(int(round(x)), int(round(y))) for x, y in points]
    draw.polygon(int_pts, fill=fill_color)
    if outline_color and outline_width > 0:
        # Draw closed loop line
        draw.line(int_pts + [int_pts[0]], fill=outline_color, width=outline_width, joint="curve")

def draw_ribbon(
    draw: ImageDraw.ImageDraw,
    center_curve: List[Point],
    half_widths: List[float],
    fill_color: Any,
    outline_color: Optional[Any] = None,
    outline_width: int = 2,
):
    """
    Constructs a smooth 2D ribbon/strip polygon along a center curve with varying widths.
    Ideal for tail segments, horns, claws, and limbs.
    """
    if len(center_curve) < 2:
        return

    left_pts = []
    right_pts = []

    for i in range(len(center_curve)):
        curr = center_curve[i]
        w = half_widths[i] if i < len(half_widths) else half_widths[-1]

        if i == 0:
            nxt = center_curve[i + 1]
            dx, dy = nxt[0] - curr[0], nxt[1] - curr[1]
        elif i == len(center_curve) - 1:
            prev = center_curve[i - 1]
            dx, dy = curr[0] - prev[0], curr[1] - prev[1]
        else:
            prev = center_curve[i - 1]
            nxt = center_curve[i + 1]
            dx, dy = nxt[0] - prev[0], nxt[1] - prev[1]

        length = math.hypot(dx, dy)
        if length < 1e-4:
            nx, ny = 0.0, 1.0
        else:
            # Normal perpendicular vector (-dy, dx)
            nx, ny = -dy / length, dx / length

        left_pts.append((curr[0] + nx * w, curr[1] + ny * w))
        right_pts.append((curr[0] - nx * w, curr[1] - ny * w))

    # Join left going forward and right going backward to form closed polygon
    poly = left_pts + list(reversed(right_pts))
    draw_polygon_with_outline(draw, poly, fill_color, outline_color, outline_width)

