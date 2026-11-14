#!/usr/bin/env python3
"""Generate every Android #SWAG launcher, adaptive, picker and splash icon from assets/icon.svg."""

from pathlib import Path

import cairosvg
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "icon.svg"
ANDROID_RES = ROOT / "app" / "composeApp" / "src" / "androidMain" / "res"
COMPOSE_DRAWABLES = ROOT / "app" / "composeApp" / "src" / "commonMain" / "composeResources" / "drawable"

if not SOURCE.is_file():
    raise SystemExit(f"Canonical #SWAG logo not found: {SOURCE}")

# Render at high resolution, then turn the supplied dark wordmark into a clean
# white foreground mask. This keeps the actual supplied artwork unchanged.
rendered = cairosvg.svg2png(url=str(SOURCE), output_width=1470, output_height=1176)
import io
source_image = Image.open(io.BytesIO(rendered)).convert("RGB")
luminance = source_image.convert("L")
mask = ImageChops.invert(luminance)
mask = mask.point(lambda value: 0 if value < 10 else value)

bbox = mask.point(lambda value: 255 if value > 18 else 0).getbbox()
if not bbox:
    raise SystemExit("The supplied SVG rendered without a detectable logo.")
mask = mask.crop(bbox)

def logo_layer(canvas_size: int, width_fraction: float) -> Image.Image:
    target_width = int(canvas_size * width_fraction)
    target_height = max(1, round(mask.height * target_width / mask.width))
    if target_height > canvas_size * 0.72:
        target_height = int(canvas_size * 0.72)
        target_width = max(1, round(mask.width * target_height / mask.height))
    resized = mask.resize((target_width, target_height), Image.Resampling.LANCZOS)
    layer = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 0))
    x = (canvas_size - target_width) // 2
    y = (canvas_size - target_height) // 2
    layer.paste(Image.new("RGBA", resized.size, (255, 255, 255, 255)), (x, y), resized)
    return layer

def save_webp(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", lossless=True, method=6)

def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=True)

# Android legacy launcher bitmap sizes.
densities = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
icon_variants = ("", "_arctic_blue", "_copper", "_emerald", "_graphite", "_rose_gold")
for density, size in densities.items():
    folder = ANDROID_RES / f"mipmap-{density}"
    background = Image.new("RGBA", (size, size), (8, 8, 8, 255))
    layer = logo_layer(size, 0.80)
    icon = Image.alpha_composite(background, layer).convert("RGB")
    save_webp(icon, folder / "ic_launcher_round.webp")
    for variant in icon_variants:
        save_webp(icon, folder / f"ic_launcher{variant}.webp")

# Adaptive icon foregrounds use the Android safe zone; all old Nuvio variants
# are replaced so no alternate launcher alias can expose upstream branding.
adaptive_sizes = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}
for density, size in adaptive_sizes.items():
    folder = ANDROID_RES / f"mipmap-{density}"
    foreground = logo_layer(size, 0.64)
    save_webp(foreground, folder / "ic_launcher_foreground.webp")
    save_webp(foreground, folder / "ic_launcher_monochrome.webp")
    for variant in ("_arctic_blue", "_copper", "_emerald", "_graphite", "_rose_gold"):
        save_webp(foreground, folder / f"ic_launcher{variant}_foreground.webp")

# In-app branding uses the exact same mark on a transparent canvas, avoiding
# the opaque white page background in the supplied SVG.
brand_mark = Image.new("RGBA", mask.size, (255, 255, 255, 0))
brand_mark.paste(Image.new("RGBA", mask.size, (255, 255, 255, 255)), (0, 0), mask)
save_png(brand_mark, COMPOSE_DRAWABLES / "swag_icon_brand.png")

# Compose icon-picker previews use the same canonical mark, not Nuvio artwork.
preview = Image.alpha_composite(
    Image.new("RGBA", (256, 256), (8, 8, 8, 255)),
    logo_layer(256, 0.80),
).convert("RGB")
for variant in ("original", "arctic_blue", "copper", "emerald", "graphite", "rose_gold"):
    save_png(preview, COMPOSE_DRAWABLES / f"app_icon_{variant}.png")

# Android 12+ splash mark, transparent so the OS places it on the app's dark bg.
splash = logo_layer(512, 0.64)
for name in (
    "ic_splash_logo.webp",
    "ic_splash_logo_arctic_blue.webp",
    "ic_splash_logo_copper.webp",
    "ic_splash_logo_emerald.webp",
    "ic_splash_logo_graphite.webp",
    "ic_splash_logo_rose_gold.webp",
):
    save_webp(splash, ANDROID_RES / "drawable-nodpi" / name)

print("Generated #SWAG launcher, adaptive, picker and splash assets from assets/icon.svg")
