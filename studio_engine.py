#!/usr/bin/env python3
"""
AI Webtoon Studio Engine (Full-Series Multi-Chapter + Character Consistency Pipeline)
-------------------------------------------------------------------------------------
Chỉ cần 1 câu Prompt (VD: "Hãy tạo cho tôi toàn bộ truyện tranh về Sơn Tinh Thủy Tinh"):
1. AI Director (LLM): Thiết kế trọn bộ kịch bản từ đầu đến cuối (nhiều Chương hoàn chỉnh)
   + Hồ sơ Nhân Vật Đồng Bộ (Character Visual DNA & Character Reference Sheets).
2. AI Character Artist: Vẽ bảng thiết kế nhân vật (Character Reference Sheets) trước.
3. AI Panel Artist: Vẽ toàn bộ các khung hình của TẤT CẢ các chương, tự động nhúng
   Visual DNA + ảnh tham chiếu nhân vật để giữ nét vẽ nhân vật đồng nhất xuyên suốt.
4. Auto-Typesetter (Pillow): Đóng hộp dẫn truyện, bóng thoại tiếng Việt, chữ tượng thanh (SFX),
   xuất dải ảnh dọc cho từng chương (chapter_X_strip.jpg), dải ảnh toàn bộ truyện
   (webtoon_full_strip.jpg) và đóng gói trọn bộ vào file .ZIP.
"""
import os
import re
import json
import math
import time
import base64
import zipfile
import urllib.parse
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")
os.makedirs(PROJECTS_DIR, exist_ok=True)

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_BOLD_ITALIC = "/usr/share/fonts/truetype/noto/NotoSans-BoldItalic.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", s)
    s = re.sub(r"[èéẹẻẽêềếệểễ]", "e", s)
    s = re.sub(r"[ìíịỉĩ]", "i", s)
    s = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", s)
    s = re.sub(r"[ùúụủũưừứựửữ]", "u", s)
    s = re.sub(r"[ỳýỵỷỹ]", "y", s)
    s = re.sub(r"[đ]", "d", s)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")[:40] or f"webtoon_{int(time.time())}"


# ==============================================================================
# 1. HẬU KỲ & TYPESETTING ENGINE (PILLOW)
# ==============================================================================

def wrap_vietnamese_text(text: str, max_chars_per_line: int = 32) -> str:
    """Tự động xuống dòng thông minh, giữ nguyên các dòng đã ngắt thủ công hợp lý."""
    has_manual_breaks = "\n" in text.strip()
    limit = max(max_chars_per_line, 58) if has_manual_breaks else max_chars_per_line
    lines = []
    for paragraph in text.split("\n"):
        if len(paragraph) <= limit:
            lines.append(paragraph)
            continue
        words = paragraph.split()
        if not words:
            continue
        current = words[0]
        for w in words[1:]:
            if len(current) + 1 + len(w) <= limit:
                current += " " + w
            else:
                lines.append(current)
                current = w
        lines.append(current)
    return "\n".join(lines)


def apply_vertical_fade(img: Image.Image, fade_top=145, fade_bottom=165) -> Image.Image:
    """
    Làm mờ mượt mà 2 đầu khung hình theo đường cong Cosine S-Curve (không gắt cạnh),
    kèm hiệu ứng dải sáng dẫn mắt dọc ở tâm giúp nối cảnh tự nhiên như Webtoon Hàn Quốc.
    """
    w, h = img.size
    result = img.convert("RGBA")
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for y in range(min(fade_top, h // 3)):
        t = 1.0 - (y / float(fade_top))
        # Đường cong S-curve cosine mượt mà từ 1.0 -> 0.0
        smooth = 0.5 * (1.0 - math.cos(math.pi * t))
        alpha = int(255 * (smooth ** 1.15))
        draw.line([(0, y), (w, y)], fill=(5, 5, 12, alpha))

    for y in range(max(0, h - fade_bottom), h):
        t = (y - (h - fade_bottom)) / float(fade_bottom)
        smooth = 0.5 * (1.0 - math.cos(math.pi * t))
        alpha = int(255 * (smooth ** 1.15))
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
    border_color=(250, 204, 21, 235),
    bg_color=(10, 12, 26, 228),
    text_color=(245, 245, 255, 255),
    font_size=22,
):
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = get_font(FONT_BOLD, font_size)

    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=7)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    width = max(width, tw + 54)
    height = max(height, th + 38)

    x0 = center_x - width // 2
    y0 = center_y - height // 2
    x1 = center_x + width // 2
    y1 = center_y + height // 2

    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.rounded_rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4], radius=10, outline=border_color, width=6)
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    overlay = Image.alpha_composite(overlay, glow)
    draw = ImageDraw.Draw(overlay)

    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=bg_color, outline=border_color, width=3)

    corner_len = 16
    c_col = (250, 204, 21, 255)
    draw.line([(x0 - 2, y0 + corner_len), (x0 - 2, y0 - 2), (x0 + corner_len, y0 - 2)], fill=c_col, width=3)
    draw.line([(x1 + 2, y1 - corner_len), (x1 + 2, y1 + 2), (x1 - corner_len, y1 + 2)], fill=c_col, width=3)

    draw.multiline_text(
        (center_x, center_y),
        text,
        font=font,
        fill=text_color,
        align="center",
        anchor="mm",
        spacing=7,
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
    font_size=23,
):
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = get_font(FONT_BOLD_ITALIC if dark_mode else FONT_BOLD, font_size)

    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=6)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    rx = max(rx, int(tw * 0.64) + 28)
    ry = max(ry, int(th * 0.68) + 24)

    bg = (14, 18, 36, 242) if dark_mode else (255, 255, 255, 248)
    outline = (56, 189, 248, 255) if dark_mode else (20, 20, 30, 255)
    fg = (224, 242, 254, 255) if dark_mode else (15, 15, 25, 255)

    draw.ellipse(
        [center_x - rx + 5, center_y - ry + 7, center_x + rx + 5, center_y + ry + 7],
        fill=(0, 0, 0, 135),
    )

    if tail_target:
        tx, ty = tail_target
        dx = tx - center_x
        dy = ty - center_y
        angle = math.atan2(dy, dx)
        perp = angle + math.pi / 2
        base_x = center_x + int(rx * 0.62 * math.cos(angle))
        base_y = center_y + int(ry * 0.62 * math.sin(angle))
        w_tail = 17
        p1 = (base_x + int(w_tail * math.cos(perp)), base_y + int(w_tail * math.sin(perp)))
        p2 = (base_x - int(w_tail * math.cos(perp)), base_y - int(w_tail * math.sin(perp)))
        draw.polygon([p1, p2, (tx, ty)], fill=bg, outline=outline)

    draw.ellipse(
        [center_x - rx, center_y - ry, center_x + rx, center_y + ry],
        fill=bg,
        outline=outline,
        width=4,
    )

    if tail_target:
        tx, ty = tail_target
        dx = tx - center_x
        dy = ty - center_y
        angle = math.atan2(dy, dx)
        perp = angle + math.pi / 2
        base_x = center_x + int(rx * 0.52 * math.cos(angle))
        base_y = center_y + int(ry * 0.52 * math.sin(angle))
        w_tail = 14
        p1 = (base_x + int(w_tail * math.cos(perp)), base_y + int(w_tail * math.sin(perp)))
        p2 = (base_x - int(w_tail * math.cos(perp)), base_y - int(w_tail * math.sin(perp)))
        draw.polygon([p1, p2, (tx, ty)], fill=bg)

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
    font_size=54,
    color=(250, 204, 21, 255),
    glow_color=(239, 68, 68, 255),
    angle=-8,
):
    txt_layer = Image.new("RGBA", (740, 220), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(txt_layer)
    font = get_font(FONT_BOLD_ITALIC, font_size)

    draw_text_with_outline(
        tdraw,
        (370, 110),
        text,
        font,
        fill=glow_color,
        outline_color=glow_color,
        outline_width=10,
    )
    txt_glow = txt_layer.filter(ImageFilter.GaussianBlur(8))

    tdraw2 = ImageDraw.Draw(txt_glow)
    draw_text_with_outline(
        tdraw2,
        (370, 110),
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


def render_character_sheet_card(raw_path: str, out_path: str, name: str, role: str):
    """Đóng khung thẻ Hồ Sơ Nhân Vật (Character Reference Sheet Card) chuyên nghiệp."""
    W = 800
    if not os.path.exists(raw_path):
        placeholder = Image.new("RGB", (W, 1000), (16, 18, 36))
        placeholder.save(raw_path, quality=92)

    img = Image.open(raw_path).convert("RGBA")
    pw, ph = img.size
    new_h = int(ph * (W / pw))
    img = img.resize((W, new_h), Image.LANCZOS)
    img = apply_vertical_fade(img, fade_top=70, fade_bottom=150)

    img = draw_narration_box(
        img,
        center_x=W // 2,
        center_y=new_h - 85,
        width=680,
        height=96,
        text=f"HỒ SƠ NHÂN VẬT: {name.upper()}\n{role}",
        border_color=(250, 204, 21, 245),
        text_color=(254, 249, 195, 255),
        font_size=22,
    )
    img.convert("RGB").save(out_path, quality=95)


def render_single_panel(raw_path: str, out_path: str, p_cfg: dict, W: int = 800) -> Image.Image:
    if not os.path.exists(raw_path):
        placeholder = Image.new("RGB", (W, 1200), (18, 18, 34))
        placeholder.save(raw_path, quality=92)

    img = Image.open(raw_path).convert("RGBA")
    pw, ph = img.size
    new_h = int(ph * (W / pw))
    img = img.resize((W, new_h), Image.LANCZOS)
    img = apply_vertical_fade(img, fade_top=110, fade_bottom=130)

    for nar in p_cfg.get("narrations", []):
        txt = wrap_vietnamese_text(nar.get("text", ""), nar.get("wrap", 38))
        if not txt.strip():
            continue
        cx = int(nar.get("x", 400))
        cy_raw = nar.get("y", 110)
        cy = int(new_h + cy_raw) if cy_raw < 0 else int(cy_raw)
        bw = int(nar.get("w", 660))
        bh = int(nar.get("h", 105))
        bcol = tuple(nar.get("border_color", [250, 204, 21, 235]))
        tcol = tuple(nar.get("text_color", [245, 245, 255, 255]))
        img = draw_narration_box(
            img,
            center_x=cx,
            center_y=cy,
            width=bw,
            height=bh,
            text=txt,
            border_color=bcol,
            text_color=tcol,
            font_size=int(nar.get("font_size", 22)),
        )

    for sfx in p_cfg.get("sfx", []):
        stxt = sfx.get("text", "").strip()
        if not stxt:
            continue
        sx = int(sfx.get("x", 400))
        sy_raw = sfx.get("y", 450)
        sy = int(new_h + sy_raw) if sy_raw < 0 else int(sy_raw)
        img = draw_sfx(
            img,
            pos=(sx, sy),
            text=stxt,
            font_size=int(sfx.get("font_size", 54)),
            color=tuple(sfx.get("color", [250, 204, 21, 255])),
            glow_color=tuple(sfx.get("glow_color", [239, 68, 68, 255])),
            angle=int(sfx.get("angle", -8)),
        )

    for bub in p_cfg.get("bubbles", []):
        txt = wrap_vietnamese_text(bub.get("text", ""), bub.get("wrap", 25))
        if not txt.strip():
            continue
        bx = int(bub.get("x", 240))
        by_raw = bub.get("y", 140)
        by = int(new_h + by_raw) if by_raw < 0 else int(by_raw)
        rx = int(bub.get("rx", 210))
        ry = int(bub.get("ry", 74))
        tail = bub.get("tail")
        if tail and len(tail) == 2:
            tx = int(tail[0])
            ty = int(new_h + tail[1]) if tail[1] < 0 else int(tail[1])
            tail = (tx, ty)
        else:
            tail = None
        img = draw_speech_bubble(
            img,
            center_x=bx,
            center_y=by,
            rx=rx,
            ry=ry,
            text=txt,
            tail_target=tail,
            dark_mode=bool(bub.get("dark_mode", False)),
            font_size=int(bub.get("font_size", 23)),
        )

    img.convert("RGB").save(out_path, quality=95)
    return img


def create_seamless_transition_bridge(
    panel_above: Image.Image,
    panel_below: Image.Image,
    gutter_text: str,
    W: int = 800,
    bridge_h: int = 230,
    style_idx: int = 0,
) -> Image.Image:
    """
    Tạo cầu nối chuyển cảnh mượt mà (Seamless Atmospheric Transition Bridge) giữa 2 khung hình:
    1. Trích xuất bảng màu (Ambient Color Bleed) từ đáy khung trên và đỉnh khung dưới,
       hòa trộn (cross-fade) qua Gaussian Blur và đường cong hình chuông (sin bell-curve)
       để khớp 100% điểm ảnh ở 2 mép nối (không còn vết cắt ngang đột ngột).
    2. Vẽ dải lụa ánh sáng dẫn mắt dọc (Vertical Scroll-Lead Light Stream) + hạt linh khí (Bokeh)
       dẫn thị giác người đọc trôi tự nhiên từ khung trên xuống khung dưới.
    3. Đặt lời dẫn chuyển cảnh (gutter_text) trên lớp sương mờ điện ảnh.
    """
    h1 = panel_above.size[1]
    h2 = panel_below.size[1]

    # Lấy vùng màu gần đáy khung trên (trước vùng tối hẳn) và vùng màu gần đỉnh khung dưới
    y1_a = max(0, h1 - 280)
    y1_b = max(y1_a + 20, h1 - 130)
    crop_above = panel_above.crop((0, y1_a, W, min(h1, y1_b))).convert("RGB").resize((W, bridge_h), Image.BILINEAR)

    y2_a = min(h2 - 20, 130)
    y2_b = min(h2, 280)
    if y2_b <= y2_a:
        y2_a, y2_b = 0, min(h2, 100)
    crop_below = panel_below.crop((0, y2_a, W, y2_b)).convert("RGB").resize((W, bridge_h), Image.BILINEAR)

    # Cross-fade dọc liên tục giữa bảng màu đáy khung trên và bảng màu đỉnh khung dưới
    grad_mask = Image.new("L", (1, bridge_h))
    for y in range(bridge_h):
        t = y / float(max(1, bridge_h - 1))
        smooth_t = 0.5 * (1.0 - math.cos(math.pi * t))
        grad_mask.putpixel((0, y), int(255 * smooth_t))
    grad_mask = grad_mask.resize((W, bridge_h), Image.NEAREST)
    blended_ambient = Image.composite(crop_below, crop_above, grad_mask).filter(ImageFilter.GaussianBlur(48))

    # Hòa trộn với nền (5, 5, 12) theo đường cong C1-continuous sin^2(pi * t):
    # Tại t=0 và t=1, cả giá trị lẫn đạo hàm đều bằng 0 -> triệt tiêu 100% vệt gãy thị giác ở mép!
    base_bg = Image.new("RGB", (W, bridge_h), (5, 5, 12))
    bell_mask = Image.new("L", (1, bridge_h))
    for y in range(bridge_h):
        t = y / float(max(1, bridge_h - 1))
        bell = (math.sin(math.pi * t) ** 2.0) * 0.44
        bell_mask.putpixel((0, y), int(255 * bell))
    bell_mask = bell_mask.resize((W, bridge_h), Image.NEAREST)
    bridge = Image.composite(blended_ambient, base_bg, bell_mask).convert("RGBA")

    # Lớp hiệu ứng Dải Sáng Dẫn Mắt Dọc (Scroll-Lead Light Trail) & Hạt Linh Khí (Bokeh)
    fx_layer = Image.new("RGBA", (W, bridge_h), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(fx_layer)

    is_gold = (style_idx % 2 == 1)
    primary_col = (253, 224, 71) if is_gold else (103, 232, 249)
    secondary_col = (245, 158, 11) if is_gold else (147, 51, 234)

    # Dải tia sáng dọc ở trục giữa dẫn mắt từ khung trên xuống khung dưới (mờ dần C1 ở 2 đầu)
    cx = W // 2
    for y in range(bridge_h):
        t = y / float(max(1, bridge_h - 1))
        text_gap = abs(t - 0.5) * 2.0
        edge_fade = math.sin(math.pi * t) ** 1.6
        alpha_beam = int(175 * edge_fade * (0.20 + 0.80 * (text_gap ** 1.5)))
        fdraw.line([(cx - 1, y), (cx + 1, y)], fill=(*primary_col, alpha_beam))

    # Các hạt linh khí (Bokeh orbs) trôi dọc theo cầu nối
    for p_i in range(18):
        px = int((W * 0.10) + ((p_i * 137 + style_idx * 53) % int(W * 0.80)))
        py = int(24 + ((p_i * 79 + style_idx * 29) % (bridge_h - 48)))
        pr = 2 + (p_i % 5)
        p_col = primary_col if (p_i % 2 == 0) else secondary_col
        t_py = py / float(max(1, bridge_h - 1))
        p_alpha = int((55 + (p_i % 4) * 32) * (math.sin(math.pi * t_py) ** 1.2))
        fdraw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(*p_col, p_alpha))

    fx_blurred = fx_layer.filter(ImageFilter.GaussianBlur(3))
    bridge = Image.alpha_composite(bridge, fx_blurred)
    bridge = Image.alpha_composite(bridge, fx_layer)

    # Vẽ lời dẫn chuyển cảnh (Gutter Text) cân đối dòng (không ngắt dòng lẻ chữ)
    clean_gutter = " ".join(gutter_text.split()) if gutter_text else ""
    gtxt = wrap_vietnamese_text(clean_gutter, 48) if clean_gutter else ""
    if gtxt and gtxt != "...":
        txt_backdrop = Image.new("RGBA", (W, bridge_h), (0, 0, 0, 0))
        tb_draw = ImageDraw.Draw(txt_backdrop)
        tb_draw.ellipse([W // 2 - 340, bridge_h // 2 - 56, W // 2 + 340, bridge_h // 2 + 56], fill=(5, 5, 14, 175))
        txt_backdrop = txt_backdrop.filter(ImageFilter.GaussianBlur(20))
        bridge = Image.alpha_composite(bridge, txt_backdrop)

        bdraw = ImageDraw.Draw(bridge)
        cy = bridge_h // 2
        orn_col = (*primary_col, 215)
        bdraw.polygon([(cx, cy - 58), (cx + 6, cy - 52), (cx, cy - 46), (cx - 6, cy - 52)], fill=orn_col)
        bdraw.polygon([(cx, cy + 46), (cx + 6, cy + 52), (cx, cy + 58), (cx - 6, cy + 52)], fill=orn_col)

        draw_text_with_outline(
            bdraw,
            (W // 2, cy),
            gtxt,
            get_font(FONT_BOLD_ITALIC, 21),
            fill=(254, 240, 138, 255) if is_gold else (186, 230, 253, 255),
            outline_color=(4, 4, 12, 255),
            outline_width=3,
        )

    return bridge


def stitch_chapter_strip(
    series_title: str,
    chapter_title: str,
    credits: str,
    footer_title: str,
    typeset_panels: list,
    gutter_texts: list,
    out_path: str,
    W: int = 800,
    bridges_out_paths: list = None,
) -> Image.Image:
    header_h = 260
    gutter_h = 240
    footer_h = 220

    n_panels = len(typeset_panels)
    total_h = (
        header_h
        + sum(p.size[1] for p in typeset_panels)
        + gutter_h * max(0, n_panels - 1)
        + footer_h
    )
    strip = Image.new("RGBA", (W, total_h), (5, 5, 12, 255))
    sdraw = ImageDraw.Draw(strip)

    draw_text_with_outline(
        sdraw,
        (W // 2, 72),
        series_title.upper(),
        get_font(FONT_BOLD, 34),
        fill=(250, 204, 21, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=4,
    )
    draw_text_with_outline(
        sdraw,
        (W // 2, 132),
        chapter_title.upper(),
        get_font(FONT_BOLD, 25),
        fill=(103, 232, 249, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=3,
    )
    draw_text_with_outline(
        sdraw,
        (W // 2, 185),
        credits,
        get_font(FONT_REGULAR, 17),
        fill=(160, 170, 195, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=2,
    )

    curr_y = header_h
    for i, panel in enumerate(typeset_panels):
        strip.paste(panel, (0, curr_y), panel)
        curr_y += panel.size[1]
        if i < len(typeset_panels) - 1:
            gtxt = gutter_texts[i] if i < len(gutter_texts) else ""
            bridge_img = create_seamless_transition_bridge(
                panel_above=panel,
                panel_below=typeset_panels[i + 1],
                gutter_text=gtxt,
                W=W,
                bridge_h=gutter_h,
                style_idx=i,
            )
            if bridges_out_paths and i < len(bridges_out_paths) and bridges_out_paths[i]:
                bridge_img.convert("RGB").save(bridges_out_paths[i], quality=94)

            strip.paste(bridge_img, (0, curr_y), bridge_img)
            curr_y += gutter_h

    sdraw = ImageDraw.Draw(strip)
    draw_text_with_outline(
        sdraw,
        (W // 2, curr_y + 80),
        footer_title,
        get_font(FONT_BOLD, 24),
        fill=(250, 204, 21, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=3,
    )
    draw_text_with_outline(
        sdraw,
        (W // 2, curr_y + 135),
        "Xuất bản tự động bằng AI Webtoon Studio • 100% Bản quyền Kịch bản & Hậu kỳ",
        get_font(FONT_REGULAR, 17),
        fill=(148, 163, 184, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=2,
    )

    strip.convert("RGB").save(out_path, quality=93)
    return strip


def normalize_storyboard_chapters(sb: dict) -> list:
    """Đảm bảo tương thích cả chuẩn mới (nhiều chương `chapters`) và chuẩn cũ (`panels`)."""
    if "chapters" in sb and isinstance(sb["chapters"], list) and len(sb["chapters"]) > 0:
        return sb["chapters"]
    return [
        {
            "chapter_index": 1,
            "chapter_title": sb.get("subtitle", "CHƯƠNG 1"),
            "footer_title": sb.get("footer_title", "— HẾT CHƯƠNG 1 —"),
            "panels": sb.get("panels", []),
        }
    ]


def render_project(project_id: str) -> dict:
    """
    Render toàn bộ một bộ truyện (gồm Hồ sơ nhân vật + Tất cả các chương + Cầu nối chuyển cảnh mượt + File ZIP trọn bộ).
    """
    proj_dir = os.path.join(PROJECTS_DIR, project_id)
    sb_path = os.path.join(proj_dir, "storyboard.json")
    if not os.path.exists(sb_path):
        raise FileNotFoundError(f"Không tìm thấy {sb_path}")

    with open(sb_path, "r", encoding="utf-8") as f:
        sb = json.load(f)

    # 1. Render Character Reference Sheet Cards
    characters = sb.get("characters", [])
    for c_cfg in characters:
        cid = c_cfg.get("id", "char")
        raw_c = os.path.join(proj_dir, f"char_{cid}_raw.jpg")
        card_c = os.path.join(proj_dir, f"char_{cid}_sheet.jpg")
        if os.path.exists(raw_c):
            render_character_sheet_card(
                raw_c,
                card_c,
                c_cfg.get("name", cid),
                c_cfg.get("role", "Nhân vật chính"),
            )

    # 2. Render Tất Cả Các Chương (Multi-Chapter) & Cầu Nối Chuyển Cảnh (Transition Bridges)
    chapters = normalize_storyboard_chapters(sb)
    multi_chapter_mode = "chapters" in sb and len(sb["chapters"]) > 0
    chapter_strips = []
    total_panels = 0

    for ch in chapters:
        ch_idx = int(ch.get("chapter_index", 1))
        ch_panels = ch.get("panels", [])
        typeset_imgs = []
        gutter_texts = []
        bridges_out_paths = []

        for p_idx, p_cfg in enumerate(ch_panels, start=1):
            total_panels += 1
            if multi_chapter_mode:
                raw_name = f"ch{ch_idx}_panel_{p_idx}_raw.jpg"
                typeset_name = f"ch{ch_idx}_panel_{p_idx}_typeset.jpg"
                bridge_name = f"ch{ch_idx}_bridge_{p_idx}.jpg"
            else:
                raw_name = f"panel_{p_idx}_raw.jpg"
                typeset_name = f"panel_{p_idx}_typeset.jpg"
                bridge_name = f"bridge_{p_idx}.jpg"

            raw_path = os.path.join(proj_dir, raw_name)
            # Fallback nếu chỉ có tên cũ panel_X_raw.jpg
            if not os.path.exists(raw_path) and os.path.exists(os.path.join(proj_dir, f"panel_{p_idx}_raw.jpg")):
                raw_path = os.path.join(proj_dir, f"panel_{p_idx}_raw.jpg")

            typeset_path = os.path.join(proj_dir, typeset_name)
            img = render_single_panel(raw_path, typeset_path, p_cfg)
            typeset_imgs.append(img)

            if p_idx < len(ch_panels):
                bridges_out_paths.append(os.path.join(proj_dir, bridge_name))
                if p_cfg.get("gutter_text"):
                    gutter_texts.append(p_cfg.get("gutter_text"))
                else:
                    gutter_texts.append("")

        ch_strip_path = os.path.join(proj_dir, f"chapter_{ch_idx}_strip.jpg")
        ch_strip = stitch_chapter_strip(
            series_title=sb.get("title", "WEBTOON STUDIO"),
            chapter_title=ch.get("chapter_title", f"CHƯƠNG {ch_idx}"),
            credits=sb.get("credits", "Nguyên tác Public Domain • AI Webtoon Studio"),
            footer_title=ch.get("footer_title", f"— HẾT CHƯƠNG {ch_idx} —"),
            typeset_panels=typeset_imgs,
            gutter_texts=gutter_texts,
            out_path=ch_strip_path,
            bridges_out_paths=bridges_out_paths,
        )
        chapter_strips.append(ch_strip)

    # 3. Ghép Dải Ảnh Tổng Hợp Toàn Bộ Các Chương (Full Series Strip)
    W = 800
    full_h = sum(s.size[1] for s in chapter_strips)
    full_strip = Image.new("RGBA", (W, max(1, full_h)), (5, 5, 12, 255))
    cy = 0
    for s in chapter_strips:
        full_strip.paste(s, (0, cy))
        cy += s.size[1]
    full_strip_path = os.path.join(proj_dir, "webtoon_full_strip.jpg")
    full_strip.convert("RGB").save(full_strip_path, quality=92)

    # 4. Đóng gói Trọn Bộ Bộ Truyện vào File .ZIP
    zip_filename = f"{project_id}_webtoon.zip"
    zip_path = os.path.join(proj_dir, zip_filename)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(sb_path, arcname="storyboard.json")
        zf.write(full_strip_path, arcname="webtoon_full_series_strip.jpg")

        for c_cfg in characters:
            cid = c_cfg.get("id", "char")
            raw_c = os.path.join(proj_dir, f"char_{cid}_raw.jpg")
            card_c = os.path.join(proj_dir, f"char_{cid}_sheet.jpg")
            if os.path.exists(raw_c):
                zf.write(raw_c, arcname=f"characters/char_{cid}_raw.jpg")
            if os.path.exists(card_c):
                zf.write(card_c, arcname=f"characters/char_{cid}_sheet.jpg")

        for ch in chapters:
            ch_idx = int(ch.get("chapter_index", 1))
            ch_strip_p = os.path.join(proj_dir, f"chapter_{ch_idx}_strip.jpg")
            if os.path.exists(ch_strip_p):
                zf.write(ch_strip_p, arcname=f"chapter_{ch_idx}/chapter_{ch_idx}_strip.jpg")

            for p_idx in range(1, len(ch.get("panels", [])) + 1):
                if multi_chapter_mode:
                    r_p = os.path.join(proj_dir, f"ch{ch_idx}_panel_{p_idx}_raw.jpg")
                    t_p = os.path.join(proj_dir, f"ch{ch_idx}_panel_{p_idx}_typeset.jpg")
                    b_p = os.path.join(proj_dir, f"ch{ch_idx}_bridge_{p_idx}.jpg")
                else:
                    r_p = os.path.join(proj_dir, f"panel_{p_idx}_raw.jpg")
                    t_p = os.path.join(proj_dir, f"panel_{p_idx}_typeset.jpg")
                    b_p = os.path.join(proj_dir, f"bridge_{p_idx}.jpg")
                if os.path.exists(r_p):
                    zf.write(r_p, arcname=f"chapter_{ch_idx}/raw/panel_{p_idx}_raw.jpg")
                if os.path.exists(t_p):
                    zf.write(t_p, arcname=f"chapter_{ch_idx}/typeset/panel_{p_idx}_typeset.jpg")
                if os.path.exists(b_p):
                    zf.write(b_p, arcname=f"chapter_{ch_idx}/bridges/bridge_{p_idx}.jpg")

    return {
        "project_id": project_id,
        "title": sb.get("title"),
        "subtitle": sb.get("subtitle"),
        "chapter_count": len(chapters),
        "panel_count": total_panels,
        "character_count": len(characters),
        "strip_url": f"/projects/{project_id}/webtoon_full_strip.jpg",
        "zip_url": f"/projects/{project_id}/{zip_filename}",
    }


# ==============================================================================
# 2. AI MULTI-CHAPTER STORYBOARD & CONSISTENT CHARACTER GENERATION PIPELINE
# ==============================================================================

FULL_SERIES_SYSTEM_PROMPT = """Bạn là Tổng Đạo Diễn Webtoon Hàn Quốc (Manhwa Series Showrunner) chuyên chuyển thể truyện cổ tích, dã sử, thần thoại, tiểu thuyết sang trọn bộ Webtoon hành động/kỳ ảo (như Solo Leveling, Omniscient Reader).
Nhiệm vụ: Khi người dùng yêu cầu tạo một bộ truyện, hãy thiết kế TRỌN BỘ TRUYỆN ĐẦY ĐỦ TỪ ĐẦU ĐẾN CUỐI gồm:
1. Hồ sơ các nhân vật chính (`characters`) với `visual_dna` bằng tiếng Anh cực kỳ chi tiết và cố định (kiểu tóc, màu mắt, giáp trụ/trang phục, vũ khí, màu hào quang) để AI vẽ đồng bộ khuôn mặt và trang phục xuyên suốt mọi chương. Tự động xác định số lượng nhân vật cốt lõi cần có trong truyện.
2. Tất cả các chương (`chapters`) bao trọn toàn bộ cốt truyện từ Mở đầu -> Phát triển -> Biến cố/Cao trào -> Đại kết cục. Nếu người dùng để chế độ Tự động (AI Quyết định), bạn hãy tự phân tích độ dài, nhịp độ kịch tính của cốt truyện để tự quyết định số lượng chương hợp lý nhất VÀ số lượng khung hình (panels) linh hoạt cho từng chương.
3. CHUYỂN CẢNH MƯỢT MÀ GIỮA CÁC PANEL (SEAMLESS PANEL-TO-PANEL TRANSITIONS):
   - Thiết kế góc máy nối tiếp điện ảnh (Action-to-Action & Match-Cut Continuity): Cảnh toàn (Establishing Wide Shot) -> Trung cảnh hành động (Medium Action Shot) -> Cận cảnh biểu cảm/ánh mắt (Extreme Close-Up) -> Góc máy từ dưới lên uy nghi (Dramatic Low Angle).
   - Ở mỗi khung hình (trừ khung cuối chương), LUÔN viết `gutter_text` (câu dẫn chuyển cảnh giàu cảm xúc/nhịp điệu nối liền hành động hoặc thời gian sang khung kế tiếp) để hệ thống vẽ Cầu nối chuyển cảnh sương mù & dải sáng (Seamless Transition Bridge).

Trả về DUY NHẤT một chuỗi JSON hợp lệ (không bọc trong markdown ```json) theo cấu trúc:
{
  "title": "TÊN BỘ TRUYỆN (IN HOA)",
  "subtitle": "TRỌN BỘ WEBTOON HOÀN CHỈNH",
  "credits": "Nguyên tác: Public Domain • AI Webtoon Studio",
  "ai_pacing_note": "Giải thích ngắn gọn vì sao AI chia bộ truyện này thành X chương và tổng cộng Y khung hình theo nhịp độ cốt truyện",
  "characters": [
    {
      "id": "son_tinh",
      "name": "Sơn Tinh (Thánh Tản Viên)",
      "role": "Nam chính • Thần Núi Tản Viên",
      "visual_dna": "22-year-old noble Vietnamese Mountain Deity, sharp heroic jawline, raven-black hair tied in a high warrior topknot with a golden hairpin, glowing amber-gold eyes, wearing dark forest-green and bronze scale armor etched with glowing golden Dong Son sun patterns, flowing dark green cape.",
      "sheet_prompt": "Korean Fantasy Manhwa Character Reference Sheet (full-body pose on left + close-up portrait on right), dark studio background with golden particles, NO TEXT."
    }
  ],
  "chapters": [
    {
      "chapter_index": 1,
      "chapter_title": "CHƯƠNG 1: TÊN CHƯƠNG MỞ ĐẦU",
      "footer_title": "— ĐÓN ĐỌC CHƯƠNG 2: ... —",
      "panels": [
        {
          "panel_index": 1,
          "scene_title": "Tên phân cảnh",
          "characters_present": ["son_tinh"],
          "image_prompt": "Detailed English prompt for a vertical Korean action fantasy manhwa panel (Solo Leveling style, sharp line art, cel-shaded digital illustration). Describe action, camera angle, lighting, background. DO NOT include any text, letters, or speech bubbles.",
          "narrations": [
            {
              "text": "Lời dẫn truyện tiếng Việt",
              "x": 400, "y": 100, "w": 660, "h": 95,
              "border_color": [250, 204, 21, 235],
              "text_color": [245, 245, 255, 255],
              "font_size": 21
            }
          ],
          "sfx": [
            {
              "text": "ẦM ĐOÀNG!!",
              "x": 500, "y": 460,
              "font_size": 52,
              "color": [250, 204, 21, 255],
              "glow_color": [239, 68, 68, 255],
              "angle": -10
            }
          ],
          "bubbles": [
            {
              "text": "Lời thoại nhân vật tiếng Việt!",
              "x": 230, "y": -115,
              "rx": 215, "ry": 72,
              "tail": [360, -280],
              "dark_mode": false,
              "font_size": 22
            }
          ],
          "gutter_text": "Câu dẫn chuyển cảnh đầy kịch tính nằm ở khoảng đen giữa 2 khung hình..."
        }
      ]
    }
  ]
}
"""


def generate_storyboard_via_ai(
    prompt: str,
    num_chapters="auto",
    panels_per_chapter="auto",
    provider: str = "gemini",
    api_key: str = "",
) -> dict:
    auto_chapters = str(num_chapters).lower() in ("auto", "0", "", "none")
    auto_panels = str(panels_per_chapter).lower() in ("auto", "0", "", "none")

    if auto_chapters and auto_panels:
        pacing_instruction = (
            "Hãy TỰ QUYẾT ĐỊNH số lượng chương (thường từ 3 đến 5 chương tùy độ dài cốt truyện) "
            "VÀ TỰ QUYẾT ĐỊNH số lượng khung hình (panels) trong mỗi chương (mỗi chương có thể có từ 3 đến 6 khung hình "
            "khác nhau tùy theo độ kịch tính/cao trào của chương đó) sao cho truyền tải trọn vẹn, đầy đủ nhất toàn bộ cốt truyện từ đầu đến cuối."
        )
    elif auto_chapters:
        pacing_instruction = (
            f"Hãy TỰ QUYẾT ĐỊNH số lượng chương phù hợp nhất với cốt truyện, "
            f"mỗi chương gồm khoảng {panels_per_chapter} khung hình."
        )
    elif auto_panels:
        pacing_instruction = (
            f"Hãy chia bộ truyện thành {num_chapters} chương, và TỰ QUYẾT ĐỊNH số khung hình (panels) "
            f"linh hoạt cho từng chương (từ 3 đến 6 khung/chương tùy độ cao trào)."
        )
    else:
        pacing_instruction = (
            f"Hãy thiết kế TRỌN BỘ truyện hoàn chỉnh từ đầu đến kết thúc gồm {num_chapters} chương "
            f"(mỗi chương có {panels_per_chapter} khung hình)."
        )

    user_msg = (
        f"Yêu cầu của độc giả: {prompt}\n"
        f"Chỉ đạo phân chương & khung hình: {pacing_instruction}\n"
        f"Đồng thời tự động lập hồ sơ thiết kế đồng bộ (`characters` + `visual_dna`) cho toàn bộ các nhân vật chính xuất hiện trong truyện."
    )

    # Danh sách các model có sẵn & còn hạn mức (Quota) trên tài khoản của người dùng:
    # - gemini-3.5-flash-lite (15 RPM, 250K TPM, 500 RPD)
    # - gemini-3.8-flash (5 RPM, 250K TPM, 20 RPD)
    # - gemini-3.1-flash-lite (15 RPM, 250K TPM, 500 RPD)
    # - gemini-3-flash-preview (5 RPM, 250K TPM, 20 RPD)
    # - gemma-4-31b-it (30 RPM, 16K TPM, 14.4K RPD)
    if provider.startswith("gemini") and api_key:
        default_chain = [
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash-lite",
            "gemini-3-flash-preview",
            "gemini-3.8-flash",
            "gemma-4-31b-it",
        ]
        preferred = provider.split(":", 1)[1] if ":" in provider else "gemini-3.1-flash-lite"
        model_chain = [preferred] + [m for m in default_chain if m != preferred]

        last_err = None
        for model_name in model_chain:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                if model_name.startswith("gemma-"):
                    payload = {
                        "contents": [{"parts": [{"text": FULL_SERIES_SYSTEM_PROMPT + "\n\n" + user_msg}]}],
                        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 16384},
                    }
                else:
                    payload = {
                        "systemInstruction": {"parts": [{"text": FULL_SERIES_SYSTEM_PROMPT}]},
                        "contents": [{"parts": [{"text": user_msg}]}],
                        "generationConfig": {
                            "responseMimeType": "application/json",
                            "temperature": 0.7,
                            "maxOutputTokens": 16384,
                        },
                    }
                resp = requests.post(url, json=payload, timeout=60)
                if resp.status_code == 200:
                    parts = resp.json()["candidates"][0]["content"]["parts"]
                    raw_text = "".join(p.get("text", "") for p in parts if "text" in p).strip()
                    raw_text = re.sub(r"^```json\s*|\s*```$", "", raw_text.strip())
                    data = json.loads(raw_text)
                    data["model_used"] = model_name
                    return data
                else:
                    last_err = f"{model_name} HTTP {resp.status_code}: {resp.text[:200]}"
                    print(f"[Warn] Gemini model {model_name} failed ({resp.status_code}), trying next model...")
            except Exception as e:
                last_err = f"{model_name} Error: {e}"
                print(f"[Warn] Exception on {model_name}: {e}")

        raise RuntimeError(f"Tất cả model Gemini đều không phản hồi. Chi tiết: {last_err}")

    elif provider == "openai" and api_key:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": FULL_SERIES_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=90)
        resp.raise_for_status()
        raw_text = resp.json()["choices"][0]["message"]["content"]
        return json.loads(raw_text)

    else:
        url = "https://text.pollinations.ai/openai"
        payload = {
            "model": "openai",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": FULL_SERIES_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
        }
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        content = re.sub(r"^```json\s*|\s*```$", "", content.strip())
        return json.loads(content)


# Cờ nhớ tạm để nếu tài khoản Gemini ở gói Free (0/0 quota cho Nano Banana Image)
# thì không lặp lại request lỗi ở các khung hình tiếp theo
_GEMINI_IMAGE_QUOTA_AVAILABLE = True


def generate_image_with_consistency(
    prompt_text: str,
    out_path: str,
    provider: str,
    api_key: str,
    reference_image_paths: list = None,
    seed: int = 42,
):
    """
    Sinh ảnh nhân vật hoặc khung hình Webtoon.
    - Nếu tài khoản Gemini có mở quota Nano Banana Image (gemini-3.1-flash-image / gemini-3.1-flash-lite-image),
      dùng Multimodal Image Generation kèm ảnh tham chiếu.
    - Nếu tài khoản Gemini có quota Image = 0/0 (Gói Free), tự động chuyển thẳng sang Flux AI
      với Visual DNA đồng bộ để không bao giờ bị lỗi 404/429.
    """
    global _GEMINI_IMAGE_QUOTA_AVAILABLE

    # 1. Gemini Nano Banana 2 (gemini-3.1-flash-image / gemini-3.1-flash-lite-image) nếu có quota
    if provider.startswith("gemini") and api_key and _GEMINI_IMAGE_QUOTA_AVAILABLE:
        for img_model in ["gemini-3.1-flash-image", "gemini-3.1-flash-lite-image"]:
            try:
                parts = []
                if reference_image_paths:
                    for ref_p in reference_image_paths[:2]:
                        if os.path.exists(ref_p):
                            with open(ref_p, "rb") as rf:
                                b64_ref = base64.b64encode(rf.read()).decode("utf-8")
                            parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64_ref}})
                parts.append(
                    {
                        "text": (
                            "Keep the exact character face, hair, and outfit design from the reference. "
                            + prompt_text
                        )
                    }
                )
                url_mm = f"https://generativelanguage.googleapis.com/v1beta/models/{img_model}:generateContent?key={api_key}"
                payload_mm = {
                    "contents": [{"parts": parts}],
                    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
                }
                r_mm = requests.post(url_mm, json=payload_mm, timeout=45)
                if r_mm.status_code == 200:
                    for part in r_mm.json()["candidates"][0]["content"]["parts"]:
                        if "inlineData" in part:
                            with open(out_path, "wb") as f:
                                f.write(base64.b64decode(part["inlineData"]["data"]))
                            return True
                elif r_mm.status_code in (404, 429, 403):
                    # Tài khoản có quota 0/0 cho Nano Banana Image -> tắt thử lại để tăng tốc
                    _GEMINI_IMAGE_QUOTA_AVAILABLE = False
                    break
            except Exception as e:
                print(f"[Warn] {img_model} fallback: {e}")
                _GEMINI_IMAGE_QUOTA_AVAILABLE = False
                break

    # 2. OpenAI DALL-E 3
    if provider == "openai" and api_key:
        try:
            url = "https://api.openai.com/v1/images/generations"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "dall-e-3",
                "prompt": prompt_text[:3800],
                "size": "1024x1792",
                "response_format": "b64_json",
                "n": 1,
            }
            r = requests.post(url, headers=headers, json=payload, timeout=90)
            if r.status_code == 200:
                b64 = r.json()["data"][0]["b64_json"]
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                return True
        except Exception as e:
            print(f"[Warn] OpenAI DALL-E 3 fallback: {e}")

    # 3. Flux AI Webtoon Renderer (kèm Visual DNA đồng bộ & tự động thử lại nếu nghẽn mạng)
    short_prompt = " ".join(prompt_text.split())[:620]
    encoded = urllib.parse.quote(short_prompt)
    for attempt in range(3):
        try:
            flux_url = f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=1344&seed={seed + attempt}&nologo=true&model=flux"
            r = requests.get(flux_url, timeout=75)
            if r.status_code == 200 and len(r.content) > 1000:
                with open(out_path, "wb") as f:
                    f.write(r.content)
                return True
        except Exception as e:
            print(f"[Warn] Flux attempt {attempt + 1} error: {e}")
        time.sleep(1.5)

    # Nếu mạng chập chờn sau 3 lần thử, tạo khung nền gradient nghệ thuật để không làm gãy pipeline
    fallback_img = Image.new("RGB", (800, 1344), (16, 18, 38))
    fallback_img.save(out_path, quality=92)
    return True


def create_full_webtoon_from_prompt(
    prompt: str,
    num_chapters="auto",
    panels_per_chapter="auto",
    provider: str = "gemini",
    api_key: str = "",
) -> dict:
    """
    Quy trình End-to-End cho Toàn Bộ Bộ Truyện:
    1. Gọi Gemini 3.5 Flash Lite / 3.8 Flash sinh Storyboard nhiều chương + Character Visual DNA.
    2. Vẽ song song (đa luồng) toàn bộ Character Reference Sheets & các Khung hình của các chương.
    3. Tự động Typeset tiếng Việt, tạo Cầu nối chuyển cảnh mượt & đóng gói trọn bộ .ZIP.
    """
    from concurrent.futures import ThreadPoolExecutor

    sb = generate_storyboard_via_ai(
        prompt=prompt,
        num_chapters=num_chapters,
        panels_per_chapter=panels_per_chapter,
        provider=provider,
        api_key=api_key,
    )
    project_id = slugify(sb.get("title", prompt))
    proj_dir = os.path.join(PROJECTS_DIR, project_id)
    os.makedirs(proj_dir, exist_ok=True)

    sb_path = os.path.join(proj_dir, "storyboard.json")
    with open(sb_path, "w", encoding="utf-8") as f:
        json.dump(sb, f, ensure_ascii=False, indent=2)

    char_map = {}
    char_ref_paths = {}
    base_seed = int(time.time()) % 10000
    tasks = []

    # Bước 1: Chuẩn bị tác vụ vẽ Bảng Thiết Kế Nhân Vật Đồng Bộ (Character Reference Sheets)
    for idx, c_cfg in enumerate(sb.get("characters", []), start=1):
        cid = c_cfg.get("id", f"char_{idx}")
        visual_dna = c_cfg.get("visual_dna", "")
        char_map[cid] = visual_dna
        raw_char_path = os.path.join(proj_dir, f"char_{cid}_raw.jpg")
        char_ref_paths[cid] = raw_char_path
        sheet_prompt = (
            f"Korean Fantasy Manhwa Character Reference Sheet (Solo Leveling / Redice Studio cel-shaded style, "
            f"full-body standing pose on the left and close-up facial portrait on the right, NO TEXT, NO LABELS). "
            f"Character Visual DNA: {visual_dna}. {c_cfg.get('sheet_prompt', '')}"
        )
        tasks.append((sheet_prompt, raw_char_path, None, base_seed + idx))

    # Bước 2: Chuẩn bị tác vụ vẽ Toàn Bộ Khung Hình Của Tất Cả Các Chương
    chapters = normalize_storyboard_chapters(sb)
    for ch in chapters:
        ch_idx = int(ch.get("chapter_index", 1))
        for p_idx, p_cfg in enumerate(ch.get("panels", []), start=1):
            present_ids = p_cfg.get("characters_present", [])
            dna_list = [char_map[cid] for cid in present_ids if cid in char_map]
            if not dna_list and char_map:
                dna_list = list(char_map.values())[:2]
            dna_context = " | ".join(dna_list)

            ref_imgs = [char_ref_paths[cid] for cid in present_ids if cid in char_ref_paths]

            full_panel_prompt = (
                f"Vertical Korean Action Manhwa Webtoon panel (Solo Leveling / Redice Studio style, "
                f"sharp line art, cel-shaded digital illustration, dramatic glowing lighting, "
                f"NO TEXT, NO SPEECH BUBBLES, NO WATERMARK). "
                f"STRICT CHARACTER VISUAL CONSISTENCY: {dna_context}. "
                f"Scene description: {p_cfg.get('image_prompt', '')}"
            )
            raw_panel_path = os.path.join(proj_dir, f"ch{ch_idx}_panel_{p_idx}_raw.jpg")
            tasks.append((full_panel_prompt, raw_panel_path, ref_imgs, base_seed + ch_idx * 100 + p_idx))

    # Thực thi song song 4 luồng để tăng tốc độ tạo trọn bộ truyện gấp 4 lần
    def _worker(item):
        p_txt, o_path, r_imgs, s_val = item
        generate_image_with_consistency(
            prompt_text=p_txt,
            out_path=o_path,
            provider=provider,
            api_key=api_key,
            reference_image_paths=r_imgs,
            seed=s_val,
        )

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(_worker, tasks))

    # Bước 3: Hậu kỳ Typeset toàn bộ các chương, vẽ Cầu nối chuyển cảnh & đóng gói .ZIP
    return render_project(project_id)
