#!/usr/bin/env python3
"""
AI-Assisted Webtoon Post-Processing & Typesetting Pipeline
Chuyển thể cổ tích Public Domain "Thạch Sanh" -> Manhwa Hàn Quốc hiện đại
"""
import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ARTIFACT_DIR = "/home/nghia/.gemini/antigravity-cli/brain/736e78f7-050d-4df0-a16c-7165f93d1f37"
WORKSPACE_DIR = "/home/nghia/Documents/truyen"
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

RAW_FILES = {
    "panel_1": os.path.join(ARTIFACT_DIR, "panel_1_scenery_1792033368471.jpg"),
    "panel_2": os.path.join(ARTIFACT_DIR, "panel_2_monster_reveal_1792033348260.jpg"),
    "panel_3": os.path.join(ARTIFACT_DIR, "panel_3_1792033344292.jpg"),
    "panel_4": os.path.join(ARTIFACT_DIR, "panel_4_1792033374641.jpg"),
}

for k, src in RAW_FILES.items():
    shutil.copyfile(src, os.path.join(ASSETS_DIR, f"{k}_raw.jpg"))

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_BOLD_ITALIC = "/usr/share/fonts/truetype/noto/NotoSans-BoldItalic.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def apply_vertical_fade(img: Image.Image, fade_top=120, fade_bottom=140) -> Image.Image:
    """Làm mờ chuyển cảnh đen ở đầu và cuối mỗi panel theo chuẩn Webtoon Hàn Quốc."""
    w, h = img.size
    result = img.convert("RGBA")
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for y in range(fade_top):
        alpha = int(255 * (1.0 - (y / fade_top)) ** 1.6)
        draw.line([(0, y), (w, y)], fill=(5, 5, 12, alpha))

    for y in range(h - fade_bottom, h):
        progress = (y - (h - fade_bottom)) / fade_bottom
        alpha = int(255 * (progress ** 1.6))
        draw.line([(0, y), (w, y)], fill=(5, 5, 12, alpha))

    return Image.alpha_composite(result, overlay)


def draw_text_with_outline(
    draw: ImageDraw.ImageDraw,
    pos,
    text,
    font,
    fill=(255, 255, 255, 255),
    outline_color=(0, 0, 0, 255),
    outline_width=4,
    align="center",
):
    x, y = pos
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width + 1:
                draw.multiline_text(
                    (x + dx, y + dy), text, font=font, fill=outline_color, align=align, anchor="mm"
                )
    draw.multiline_text((x, y), text, font=font, fill=fill, align=align, anchor="mm")


def draw_narration_box(
    canvas: Image.Image,
    center_x: int,
    center_y: int,
    width: int,
    height: int,
    text: str,
    border_color=(168, 85, 247, 230),
    bg_color=(12, 10, 24, 225),
    text_color=(240, 240, 255, 255),
    font_size=24,
):
    """Vẽ hộp dẫn truyện (System / Lore Box) chuẩn Manhwa Dark Fantasy."""
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    x0 = center_x - width // 2
    y0 = center_y - height // 2
    x1 = center_x + width // 2
    y1 = center_y + height // 2

    # Outer glow
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.rounded_rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4], radius=10, outline=border_color, width=6)
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    overlay = Image.alpha_composite(overlay, glow)
    draw = ImageDraw.Draw(overlay)

    # Box body
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=bg_color, outline=border_color, width=3)
    # Corner accents
    corner_len = 16
    c_col = (250, 204, 21, 255)
    # Top-left
    draw.line([(x0 - 2, y0 + corner_len), (x0 - 2, y0 - 2), (x0 + corner_len, y0 - 2)], fill=c_col, width=3)
    # Bottom-right
    draw.line([(x1 + 2, y1 - corner_len), (x1 + 2, y1 + 2), (x1 - corner_len, y1 + 2)], fill=c_col, width=3)

    font = get_font(FONT_BOLD, font_size)
    draw.multiline_text(
        (center_x, center_y),
        text,
        font=font,
        fill=text_color,
        align="center",
        anchor="mm",
        spacing=8,
    )
    return Image.alpha_composite(canvas, overlay)


def draw_speech_bubble(
    canvas: Image.Image,
    center_x: int,
    center_y: int,
    rx: int,
    ry: int,
    text: str,
    tail_target=None,
    dark_mode=False,
    font_size=25,
):
    """Vẽ bóng thoại chuẩn truyện tranh có đuôi trỏ về nhân vật."""
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    bg = (18, 12, 28, 240) if dark_mode else (255, 255, 255, 248)
    outline = (239, 68, 68, 255) if dark_mode else (20, 20, 30, 255)
    fg = (255, 230, 230, 255) if dark_mode else (15, 15, 25, 255)

    # Drop shadow
    draw.ellipse(
        [center_x - rx + 5, center_y - ry + 7, center_x + rx + 5, center_y + ry + 7],
        fill=(0, 0, 0, 130),
    )

    # Tail
    if tail_target:
        tx, ty = tail_target
        dx = tx - center_x
        dy = ty - center_y
        angle = math.atan2(dy, dx)
        perp = angle + math.pi / 2
        base_x = center_x + int(rx * 0.65 * math.cos(angle))
        base_y = center_y + int(ry * 0.65 * math.sin(angle))
        w_tail = 18
        p1 = (base_x + int(w_tail * math.cos(perp)), base_y + int(w_tail * math.sin(perp)))
        p2 = (base_x - int(w_tail * math.cos(perp)), base_y - int(w_tail * math.sin(perp)))
        draw.polygon([p1, p2, (tx, ty)], fill=bg, outline=outline)

    # Main ellipse
    draw.ellipse(
        [center_x - rx, center_y - ry, center_x + rx, center_y + ry],
        fill=bg,
        outline=outline,
        width=4,
    )

    # Re-fill inner tail seam
    if tail_target:
        tx, ty = tail_target
        dx = tx - center_x
        dy = ty - center_y
        angle = math.atan2(dy, dx)
        perp = angle + math.pi / 2
        base_x = center_x + int(rx * 0.55 * math.cos(angle))
        base_y = center_y + int(ry * 0.55 * math.sin(angle))
        w_tail = 14
        p1 = (base_x + int(w_tail * math.cos(perp)), base_y + int(w_tail * math.sin(perp)))
        p2 = (base_x - int(w_tail * math.cos(perp)), base_y - int(w_tail * math.sin(perp)))
        draw.polygon([p1, p2, (tx, ty)], fill=bg)

    font = get_font(FONT_BOLD_ITALIC if dark_mode else FONT_BOLD, font_size)
    draw.multiline_text(
        (center_x, center_y),
        text,
        font=font,
        fill=fg,
        align="center",
        anchor="mm",
        spacing=6,
    )
    return Image.alpha_composite(canvas, overlay)


def draw_sfx(
    canvas: Image.Image,
    pos,
    text: str,
    font_size=56,
    color=(250, 204, 21, 255),
    glow_color=(239, 68, 68, 255),
    angle=8,
):
    """Vẽ chữ tượng thanh (SFX) nghiêng có hào quang phát sáng."""
    txt_layer = Image.new("RGBA", (700, 220), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(txt_layer)
    font = get_font(FONT_BOLD_ITALIC, font_size)

    # Glow
    draw_text_with_outline(
        tdraw,
        (350, 110),
        text,
        font,
        fill=glow_color,
        outline_color=glow_color,
        outline_width=10,
    )
    txt_glow = txt_layer.filter(ImageFilter.GaussianBlur(8))

    # Crisp text on top
    tdraw2 = ImageDraw.Draw(txt_glow)
    draw_text_with_outline(
        tdraw2,
        (350, 110),
        text,
        font,
        fill=color,
        outline_color=(10, 10, 18, 255),
        outline_width=6,
    )

    rotated = txt_glow.rotate(angle, expand=True, resample=Image.BICUBIC)
    rw, rh = rotated.size
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay.paste(rotated, (pos[0] - rw // 2, pos[1] - rh // 2), rotated)
    return Image.alpha_composite(canvas, overlay)


def build_webtoon():
    W = 800  # Chuẩn chiều rộng Webtoon Mobile HD

    # Load & resize panels to width=800
    panels = []
    for i in range(1, 5):
        p = Image.open(os.path.join(ASSETS_DIR, f"panel_{i}_raw.jpg")).convert("RGBA")
        pw, ph = p.size
        new_h = int(ph * (W / pw))
        p = p.resize((W, new_h), Image.LANCZOS)
        p = apply_vertical_fade(p, fade_top=110, fade_bottom=130)
        panels.append(p)

    # --- TYPESET INDIVIDUAL PANELS ---
    # Panel 1: Establishing Shrine
    p1 = panels[0].copy()
    p1 = draw_narration_box(
        p1,
        center_x=400,
        center_y=115,
        width=680,
        height=115,
        text="[MIẾU THẦN LINH - ĐÊM Đinh Dậu]\nMỗi năm một mạng người... Đêm nay là kỳ hạn hiến tế.",
        border_color=(168, 85, 247, 230),
        font_size=23,
    )
    p1 = draw_sfx(
        p1,
        pos=(240, 410),
        text="ẦM ĐOÀNG!!",
        font_size=50,
        color=(216, 180, 254, 255),
        glow_color=(126, 34, 206, 255),
        angle=-10,
    )
    p1 = draw_narration_box(
        p1,
        center_x=400,
        center_y=p1.size[1] - 110,
        width=620,
        height=95,
        text="Kẻ lẽ ra phải nộp mạng là Lý Thông...\nNhưng người đang ngồi trong miếu lại là THẠCH SANH.",
        border_color=(56, 189, 248, 220),
        font_size=22,
    )
    p1.convert("RGB").save(os.path.join(ASSETS_DIR, "panel_1_typeset.jpg"), quality=95)

    # Panel 2: Monster Reveal
    p2 = panels[1].copy()
    p2 = draw_sfx(
        p2,
        pos=(400, 110),
        text="GRÀOOOOO—!!",
        font_size=58,
        color=(254, 202, 202, 255),
        glow_color=(220, 38, 38, 255),
        angle=5,
    )
    p2 = draw_speech_bubble(
        p2,
        center_x=235,
        center_y=835,
        rx=205,
        ry=82,
        text="Mùi máu phàm nhân...\nNgươi là vật tế đêm nay sao,\ncôn trùng nhỏ bé?!",
        tail_target=(330, 560),
        dark_mode=True,
        font_size=23,
    )
    p2.convert("RGB").save(os.path.join(ASSETS_DIR, "panel_2_typeset.jpg"), quality=95)

    # Panel 3: Thạch Sanh Awakening
    p3 = panels[2].copy()
    p3 = draw_speech_bubble(
        p3,
        center_x=205,
        center_y=105,
        rx=185,
        ry=64,
        text="Vật tế ư?\nTa e là ngươi nhầm rồi...",
        tail_target=(295, 225),
        dark_mode=False,
        font_size=22,
    )
    p3 = draw_sfx(
        p3,
        pos=(615, 575),
        text="XẸT—!",
        font_size=46,
        color=(103, 232, 249, 255),
        glow_color=(6, 182, 212, 255),
        angle=-14,
    )
    p3 = draw_speech_bubble(
        p3,
        center_x=300,
        center_y=p3.size[1] - 100,
        rx=255,
        ry=68,
        text="Đêm nay, ta đến để LẤY ĐẦU NGƯƠI!",
        tail_target=(415, 555),
        dark_mode=False,
        font_size=24,
    )
    p3.convert("RGB").save(os.path.join(ASSETS_DIR, "panel_3_typeset.jpg"), quality=95)

    # Panel 4: Climax Action Slash
    p4 = panels[3].copy()
    p4 = draw_narration_box(
        p4,
        center_x=195,
        center_y=110,
        width=340,
        height=96,
        text="[THẦN KỸ KÍCH HOẠT]\nLÔI PHỦ TRẢM!",
        border_color=(34, 211, 238, 255),
        text_color=(165, 243, 252, 255),
        font_size=23,
    )
    p4 = draw_sfx(
        p4,
        pos=(530, 880),
        text="ĐOÀNGGG!!",
        font_size=62,
        color=(253, 224, 71, 255),
        glow_color=(6, 182, 212, 255),
        angle=-12,
    )
    p4.convert("RGB").save(os.path.join(ASSETS_DIR, "panel_4_typeset.jpg"), quality=95)

    # --- BUILD FULL VERTICAL WEBTOON STRIP (CHUẨN SOLO LEVELING SCROLL) ---
    header_h = 260
    gutter_h = 180
    footer_h = 220

    typeset_panels = [p1, p2, p3, p4]
    total_h = (
        header_h
        + sum(p.size[1] for p in typeset_panels)
        + gutter_h * (len(typeset_panels) - 1)
        + footer_h
    )

    strip = Image.new("RGBA", (W, total_h), (5, 5, 12, 255))
    sdraw = ImageDraw.Draw(strip)

    # Header Title Card
    draw_text_with_outline(
        sdraw,
        (W // 2, 70),
        "DÃ SỬ DỊ GIỚI: THẠCH SANH",
        get_font(FONT_BOLD, 38),
        fill=(250, 204, 21, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=4,
    )
    draw_text_with_outline(
        sdraw,
        (W // 2, 130),
        "CHƯƠNG 1: HUYẾT XÀ TRONG MIẾU CỔ",
        get_font(FONT_BOLD, 26),
        fill=(103, 232, 249, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=3,
    )
    draw_text_with_outline(
        sdraw,
        (W // 2, 185),
        "Nguyên tác: Cổ tích Việt Nam (Public Domain)  •  AI-Assisted Manhwa Studio",
        get_font(FONT_REGULAR, 17),
        fill=(160, 170, 195, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=2,
    )

    gutter_texts = [
        "Bóng tối nuốt chửng ánh trăng...\nMột luồng sát khí thượng cổ trỗi dậy!",
        "Đứng trước Đại Yêu khiến cả kinh thành khiếp đảm...\nChàng tiều phu trẻ chỉ khẽ nhếch môi.",
        "Một nhát rìu — Phân định sinh tử!",
    ]

    curr_y = header_h
    for idx, panel in enumerate(typeset_panels):
        strip.paste(panel, (0, curr_y), panel)
        curr_y += panel.size[1]
        if idx < len(gutter_texts):
            # Pacing text inside the black gutter between panels
            draw_text_with_outline(
                sdraw,
                (W // 2, curr_y + gutter_h // 2),
                gutter_texts[idx],
                get_font(FONT_BOLD_ITALIC, 23),
                fill=(216, 180, 254, 255) if idx == 0 else (165, 243, 252, 255),
                outline_color=(0, 0, 0, 255),
                outline_width=3,
            )
            curr_y += gutter_h

    # Footer Cliffhanger
    draw_text_with_outline(
        sdraw,
        (W // 2, curr_y + 80),
        "— ĐÓN ĐỌC CHƯƠNG 2: ÂM MƯU CỦA LÝ THÔNG —",
        get_font(FONT_BOLD, 26),
        fill=(250, 204, 21, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=3,
    )
    draw_text_with_outline(
        sdraw,
        (W // 2, curr_y + 135),
        "Bản quyền kịch bản & biên tập thuộc về Webapp của bạn (100% hợp pháp thương mại)",
        get_font(FONT_REGULAR, 17),
        fill=(148, 163, 184, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=2,
    )

    strip_out = os.path.join(ASSETS_DIR, "webtoon_chapter1_strip.jpg")
    strip.convert("RGB").save(strip_out, quality=94)

    # Also copy typeset files & strip to ARTIFACT_DIR so we can embed in artifact
    for f in [
        "panel_1_typeset.jpg",
        "panel_2_typeset.jpg",
        "panel_3_typeset.jpg",
        "panel_4_typeset.jpg",
        "webtoon_chapter1_strip.jpg",
    ]:
        shutil.copyfile(os.path.join(ASSETS_DIR, f), os.path.join(ARTIFACT_DIR, f))

    print("Typesetting completed successfully!")


if __name__ == "__main__":
    build_webtoon()
