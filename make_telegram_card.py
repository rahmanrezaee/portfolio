#!/usr/bin/env python3
import argparse
import os
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

DEFAULT_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
]

DARK_PURPLE = (43, 11, 43, 255)
YELLOW_ACCENT = (255, 193, 7, 255)
WHITE = (255, 255, 255, 255)


def load_font(preferred_path: str | None, pixel_size: int) -> ImageFont.FreeTypeFont:
    candidate_paths = []
    if preferred_path:
        candidate_paths.append(preferred_path)
    candidate_paths.extend(DEFAULT_FONT_CANDIDATES)

    for path in candidate_paths:
        if path and os.path.exists(path):
            try:
                return ImageFont.truetype(path, pixel_size)
            except Exception:
                continue

    # Last resort: default PIL font (may not fully support Persian)
    return ImageFont.load_default()


def shape_rtl_text(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def draw_banner(
    image: Image.Image,
    text: str,
    banner_color: Tuple[int, int, int, int] = DARK_PURPLE,
    accent_color: Tuple[int, int, int, int] = YELLOW_ACCENT,
    font_path: str | None = None,
) -> Image.Image:
    base = image.convert("RGBA")
    width, height = base.size

    # Banner sizing
    margin = max(16, width // 60)
    banner_height = max(int(height * 0.2), 120)
    banner_radius = max(20, width // 80)

    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Banner rectangle
    left = margin
    right = width - margin
    top = height - margin - banner_height
    bottom = height - margin
    draw.rounded_rectangle(
        [left, top, right, bottom],
        radius=banner_radius,
        fill=banner_color,
    )

    # Accent stripe near the right edge inside the banner
    stripe_gap = max(12, width // 120)
    stripe_width = max(10, width // 180)
    stripe_right = right - stripe_gap
    stripe_left = stripe_right - stripe_width
    draw.rounded_rectangle(
        [stripe_left, top + banner_radius // 2, stripe_right, bottom - banner_radius // 2],
        radius=stripe_width // 2,
        fill=accent_color,
    )

    # Prepare text
    shaped_text = shape_rtl_text(text)

    # Determine max text area
    right_padding_after_stripe = stripe_gap + stripe_width + max(16, width // 80)
    left_padding = max(24, width // 40)
    max_text_width = (right - right_padding_after_stripe) - (left + left_padding)
    max_text_height = banner_height - max(24, banner_height // 4)

    # Adaptive font size
    font_size = max(24, banner_height // 2)
    font = load_font(font_path, font_size)
    text_bbox = draw.textbbox((0, 0), shaped_text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]

    while (text_w > max_text_width or text_h > max_text_height) and font_size > 10:
        font_size -= 2
        font = load_font(font_path, font_size)
        text_bbox = draw.textbbox((0, 0), shaped_text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]

    # Right-aligned text baseline
    text_x_right = right - right_padding_after_stripe
    text_y = top + (banner_height - text_h) // 2

    draw.text((text_x_right - text_w, text_y), shaped_text, font=font, fill=WHITE)

    composed = Image.alpha_composite(base, overlay)
    return composed.convert("RGB")


def process_image(input_path: str, output_path: str, text: str, font_path: str | None) -> None:
    with Image.open(input_path) as im:
        result = draw_banner(im, text=text, font_path=font_path)
        result.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Telegram-ready card with Persian caption banner.")
    parser.add_argument("input", help="Path to the input image (e.g., player photo)")
    parser.add_argument("output", help="Path to save the output image")
    parser.add_argument("--text", default="فوتبالیست قهوه خور", help="Persian text to place on the banner")
    parser.add_argument("--font", default=None, help="Optional font file path that supports Arabic/Persian glyphs")
    args = parser.parse_args()

    process_image(args.input, args.output, args.text, args.font)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()