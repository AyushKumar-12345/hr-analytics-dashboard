#!/usr/bin/env python3
"""
HR Analytics - Executive Canvas Generator
=========================================
Generates a polished 1920x1080 (16:9) dark-mode canvas with smooth
radial glows, micro-dithering to prevent color banding, and corporate
executive styling (Teal / Amber-Orange / Deep Slate) for Power BI.
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def generate_hr_canvas(
    width: int = 1920,
    height: int = 1080,
    output_filename: str = "HR_Analytics_Background.png"
) -> Path:
    """Generate high-fidelity, band-free executive HR background canvas."""
    print(f"Rendering HR executive canvas at {width}x{height} resolution...")

    # 1. Base Gradient: Vertical Vignette (#0A0E17 to #111827)
    y_coords, x_coords = np.ogrid[:height, :width]
    vertical_ratio = y_coords / height

    base_r = 10 + (7 * vertical_ratio)
    base_g = 14 + (10 * vertical_ratio)
    base_b = 23 + (16 * vertical_ratio)

    canvas = np.zeros((height, width, 3), dtype=np.float32)
    canvas[:, :, 0] = base_r
    canvas[:, :, 1] = base_g
    canvas[:, :, 2] = base_b

    # 2. Executive Focal Lighting Glows
    glows = [
        # Glow 1: Deep Workforce Teal / Cyan (Top Left: Header & KPI Area)
        {
            "center": (280, 240),
            "radius": 560.0,
            "color": np.array([14.0, 116.0, 144.0]),
            "intensity": 0.42
        },
        # Glow 2: Strategic Attrition Rust-Orange / Amber (Bottom Right: Charts)
        {
            "center": (1650, 820),
            "radius": 650.0,
            "color": np.array([194.0, 65.0, 12.0]),
            "intensity": 0.38
        },
        # Glow 3: Subtle Center Atmospheric Indigo (Soft Ambient Fill)
        {
            "center": (960, 540),
            "radius": 850.0,
            "color": np.array([30.0, 41.0, 59.0]),
            "intensity": 0.25
        }
    ]

    # 3. Apply Multi-Point Radial Gaussian Falloffs
    for glow in glows:
        gx, gy = glow["center"]
        radius = glow["radius"]
        color = glow["color"]
        strength = glow["intensity"]

        dist_sq = (x_coords - gx) ** 2 + (y_coords - gy) ** 2
        falloff = np.exp(-dist_sq / (2.0 * (radius ** 2)))

        for c in range(3):
            canvas[:, :, c] += falloff * color[c] * strength

    # 4. Anti-Banding Subtle Dither (Micro-noise eliminates dark gradient steps)
    rng = np.random.default_rng(seed=42)
    dither_noise = rng.normal(loc=0.0, scale=0.45, size=(height, width, 3))
    canvas += dither_noise

    # 5. Clamp and convert to uint8 image
    canvas_uint8 = np.clip(canvas, 0, 255).astype(np.uint8)
    image = Image.fromarray(canvas_uint8, mode="RGB")

    # 6. Smooth Blending via Dual Gaussian Filtering
    image = image.filter(ImageFilter.GaussianBlur(radius=10))

    # 7. Export file
    output_path = Path(__file__).resolve().parent / output_filename
    image.save(output_path, format="PNG", optimize=True)
    print(f"Canvas successfully saved to: {output_path.name}")
    return output_path


if __name__ == "__main__":
    generate_hr_canvas()
