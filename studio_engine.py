#!/usr/bin/env python3
"""
AI Webtoon Studio Engine (Core Pipeline)
----------------------------------------
Từ 1 câu yêu cầu (Prompt) + API Key:
1. Gọi LLM (Gemini / OpenAI) sinh kịch bản phân cảnh (Storyboard JSON) + Character Bible.
2. Gọi AI Image API (Gemini Imagen / Gemini Flash Image / OpenAI DALL-E 3 / Pollinations Flux)
   để vẽ từng khung hình dọc (Vertical Manhwa Panels) không chứa chữ rác.
3. Tự động hậu kỳ (Auto-Typesetting): Làm tối viền chuyển cảnh, đóng hộp dẫn truyện,
   vẽ bóng thoại tiếng Việt có đuôi trỏ, vẽ chữ tượng thanh (SFX) phát sáng.
4. Xuất ra trọn bộ file ảnh từng khung, ảnh cuộn dọc nguyên cột (Full Strip) và gói .ZIP.
"""
import os
import re
import json
import math
import time
import shutil
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


def apply_vertical_fade(img: Image.Image, fade_top=115, fade_bottom=135) -> Image.Image:
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
    border_color=(250, 204, 21, 235),
    bg_color=(10, 12, 26, 228),
    text_color=(245, 245, 255, 255),
    font_size=22,
):
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = get_font(FONT_BOLD, font_size)

    # Auto-measure text bounding box so text never overflows box
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

    # Auto-measure text bounding box so text fits comfortably inside ellipse
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


def render_project(project_id: str) -> dict:
    """
    Đọc storyboard.json và các ảnh panel_X_raw.jpg trong thư mục project,
    sau đó tự động render:
      - panel_X_typeset.jpg
      - webtoon_full_strip.jpg
      - <project_id>_webtoon.zip (chứa đầy đủ toàn bộ file ảnh để tải về)
    """
    proj_dir = os.path.join(PROJECTS_DIR, project_id)
    sb_path = os.path.join(proj_dir, "storyboard.json")
    if not os.path.exists(sb_path):
        raise FileNotFoundError(f"Không tìm thấy {sb_path}")

    with open(sb_path, "r", encoding="utf-8") as f:
        sb = json.load(f)

    W = 800
    typeset_panels = []
    gutter_texts = []

    for idx, p_cfg in enumerate(sb.get("panels", []), start=1):
        raw_path = os.path.join(proj_dir, f"panel_{idx}_raw.jpg")
        if not os.path.exists(raw_path):
            # Tạo ảnh placeholder nếu chưa có
            placeholder = Image.new("RGB", (W, 1200), (18, 18, 34))
            placeholder.save(raw_path, quality=92)

        img = Image.open(raw_path).convert("RGBA")
        pw, ph = img.size
        new_h = int(ph * (W / pw))
        img = img.resize((W, new_h), Image.LANCZOS)
        img = apply_vertical_fade(img, fade_top=110, fade_bottom=130)

        # 1. Vẽ Narration Boxes
        for nar in p_cfg.get("narrations", []):
            txt = wrap_vietnamese_text(nar.get("text", ""), nar.get("wrap", 38))
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

        # 2. Vẽ SFX
        for sfx in p_cfg.get("sfx", []):
            sx = int(sfx.get("x", 400))
            sy_raw = sfx.get("y", 450)
            sy = int(new_h + sy_raw) if sy_raw < 0 else int(sy_raw)
            img = draw_sfx(
                img,
                pos=(sx, sy),
                text=sfx.get("text", "ẦM ĐOÀNG!!"),
                font_size=int(sfx.get("font_size", 54)),
                color=tuple(sfx.get("color", [250, 204, 21, 255])),
                glow_color=tuple(sfx.get("glow_color", [239, 68, 68, 255])),
                angle=int(sfx.get("angle", -8)),
            )

        # 3. Vẽ Speech Bubbles
        for bub in p_cfg.get("bubbles", []):
            txt = wrap_vietnamese_text(bub.get("text", ""), bub.get("wrap", 25))
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

        typeset_path = os.path.join(proj_dir, f"panel_{idx}_typeset.jpg")
        img.convert("RGB").save(typeset_path, quality=95)
        typeset_panels.append(img)
        if p_cfg.get("gutter_text"):
            gutter_texts.append(p_cfg.get("gutter_text"))
        elif idx < len(sb.get("panels", [])):
            gutter_texts.append("...")

    # --- GHÉP FILE WEBTOON DỌC NGUYÊN CỘT (FULL VERTICAL STRIP) ---
    header_h = 260
    gutter_h = 185
    footer_h = 220

    total_h = (
        header_h
        + sum(p.size[1] for p in typeset_panels)
        + gutter_h * max(0, len(typeset_panels) - 1)
        + footer_h
    )
    strip = Image.new("RGBA", (W, total_h), (5, 5, 12, 255))
    sdraw = ImageDraw.Draw(strip)

    draw_text_with_outline(
        sdraw,
        (W // 2, 72),
        sb.get("title", "WEBTOON STUDIO").upper(),
        get_font(FONT_BOLD, 36),
        fill=(250, 204, 21, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=4,
    )
    draw_text_with_outline(
        sdraw,
        (W // 2, 132),
        sb.get("subtitle", "CHƯƠNG 1").upper(),
        get_font(FONT_BOLD, 25),
        fill=(103, 232, 249, 255),
        outline_color=(0, 0, 0, 255),
        outline_width=3,
    )
    draw_text_with_outline(
        sdraw,
        (W // 2, 185),
        sb.get("credits", "Nguyên tác Public Domain • Sản xuất bởi AI Webtoon Studio"),
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
            if gtxt:
                draw_text_with_outline(
                    sdraw,
                    (W // 2, curr_y + gutter_h // 2),
                    gtxt,
                    get_font(FONT_BOLD_ITALIC, 23),
                    fill=(253, 224, 71, 255) if i % 2 == 1 else (165, 243, 252, 255),
                    outline_color=(0, 0, 0, 255),
                    outline_width=3,
                )
            curr_y += gutter_h

    draw_text_with_outline(
        sdraw,
        (W // 2, curr_y + 80),
        sb.get("footer_title", "— HẾT CHƯƠNG 1: ĐÓN ĐỌC CHƯƠNG TIẾP THEO —"),
        get_font(FONT_BOLD, 25),
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

    strip_path = os.path.join(proj_dir, "webtoon_full_strip.jpg")
    strip.convert("RGB").save(strip_path, quality=94)

    # --- ĐÓNG GÓI TRỌN BỘ ẢNH THÀNH FILE .ZIP ĐỂ TẢI VỀ ---
    zip_filename = f"{project_id}_webtoon.zip"
    zip_path = os.path.join(proj_dir, zip_filename)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(sb_path, arcname="storyboard.json")
        zf.write(strip_path, arcname="webtoon_full_strip.jpg")
        for idx in range(1, len(typeset_panels) + 1):
            r_p = os.path.join(proj_dir, f"panel_{idx}_raw.jpg")
            t_p = os.path.join(proj_dir, f"panel_{idx}_typeset.jpg")
            if os.path.exists(r_p):
                zf.write(r_p, arcname=f"raw/panel_{idx}_raw.jpg")
            if os.path.exists(t_p):
                zf.write(t_p, arcname=f"typeset/panel_{idx}_typeset.jpg")

    return {
        "project_id": project_id,
        "title": sb.get("title"),
        "subtitle": sb.get("subtitle"),
        "panel_count": len(typeset_panels),
        "strip_url": f"/projects/{project_id}/webtoon_full_strip.jpg",
        "zip_url": f"/projects/{project_id}/{zip_filename}",
    }


# ==============================================================================
# 2. AI STORYBOARD & IMAGE GENERATION PIPELINE (GEMINI / OPENAI / POLLINATIONS)
# ==============================================================================

STORYBOARD_SYSTEM_PROMPT = """Bạn là Đạo diễn Webtoon Hàn Quốc (Manhwa Director) chuyên chuyển thể truyện cổ tích, dã sử, tiểu thuyết sang phong cách hành động thần thoại (như Solo Leveling, Omniscient Reader).
Nhiệm vụ: Dựa trên yêu cầu của người dùng, hãy thiết kế 1 chương Webtoon hoàn chỉnh và trả về DUY NHẤT một chuỗi JSON hợp lệ (không bọc trong markdown ```json) theo cấu trúc sau:
{
  "title": "Tên Bộ Truyện (In hoa, ngắn gọn, hấp dẫn)",
  "subtitle": "CHƯƠNG 1: Tên chương kịch tính",
  "credits": "Nguyên tác: Public Domain • AI-Assisted Manhwa Studio",
  "footer_title": "— ĐÓN ĐỌC CHƯƠNG 2: ... —",
  "character_bible": "Mô tả ngoại hình nhân vật chính bằng tiếng Anh để giữ đồng nhất nét vẽ",
  "panels": [
    {
      "panel_index": 1,
      "scene_title": "Tên phân cảnh",
      "image_prompt": "Detailed English prompt for a vertical Korean action fantasy manhwa panel (Solo Leveling style, sharp line art, cel-shaded digital illustration, dramatic glowing lighting). Describe the characters, outfits, action, camera angle, background. DO NOT include any text, letters, or speech bubbles.",
      "narrations": [
        {
          "text": "Lời dẫn truyện tiếng Việt ngắn gọn, hào hùng",
          "x": 400, "y": 110, "w": 660, "h": 105,
          "border_color": [250, 204, 21, 235],
          "text_color": [245, 245, 255, 255],
          "font_size": 22
        }
      ],
      "sfx": [
        {
          "text": "ẦM ĐOÀNG!!",
          "x": 520, "y": 460,
          "font_size": 52,
          "color": [250, 204, 21, 255],
          "glow_color": [239, 68, 68, 255],
          "angle": -10
        }
      ],
      "bubbles": [
        {
          "text": "Lời thoại nhân vật tiếng Việt!",
          "x": 230, "y": -120,
          "rx": 215, "ry": 72,
          "tail": [360, -280],
          "dark_mode": false,
          "font_size": 23
        }
      ],
      "gutter_text": "Câu dẫn chuyển cảnh đầy kịch tính nằm ở khoảng đen giữa 2 khung hình..."
    }
  ]
}
Lưu ý tọa độ (chiều rộng khung chuẩn W=800, chiều cao khoảng 1200-1400):
- y dương (ví dụ 110) là tính từ mép trên xuống; y âm (ví dụ -115) là tính từ mép dưới lên.
- Đảm bảo không đặt bóng thoại che giữa tâm mặt nhân vật (ưu tiên góc trên x=220, y=115 hoặc góc dưới x=280, y=-115).
"""


def generate_storyboard_via_ai(prompt: str, num_panels: int, provider: str, api_key: str) -> dict:
    user_msg = f"Yêu cầu: {prompt}. Hãy thiết kế đúng {num_panels} khung hình (panels) liên kết chặt chẽ từ mở đầu, cao trào đến kết chương."

    if provider == "gemini" and api_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = {
            "systemInstruction": {"parts": [{"text": STORYBOARD_SYSTEM_PROMPT}]},
            "contents": [{"parts": [{"text": user_msg}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7},
        }
        resp = requests.post(url, json=payload, timeout=60)
        if resp.status_code != 200:
            # Fallback to gemini-2.0-flash if 2.5 not available
            url2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
            resp = requests.post(url2, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(raw_text)

    elif provider == "openai" and api_key:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": STORYBOARD_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        raw_text = resp.json()["choices"][0]["message"]["content"]
        return json.loads(raw_text)

    else:
        # Fallback thông minh qua Pollinations Text API (OpenAI-compatible miễn phí) nếu chưa nhập key
        url = "https://text.pollinations.ai/openai"
        payload = {
            "model": "openai",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": STORYBOARD_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
        }
        resp = requests.post(url, json=payload, timeout=90)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        content = re.sub(r"^```json\s*|\s*```$", "", content.strip())
        return json.loads(content)


def generate_panel_image_via_ai(
    image_prompt: str, character_bible: str, out_path: str, provider: str, api_key: str
):
    full_prompt = (
        f"Vertical Korean Action Manhwa Webtoon panel (Solo Leveling / Redice Studio style, "
        f"cel-shaded digital art, dramatic lighting, NO TEXT, NO SPEECH BUBBLES, NO WATERMARK). "
        f"Character reference: {character_bible}. Scene: {image_prompt}"
    )

    # 1. Thử dùng Gemini Imagen 3 nếu có Gemini API Key
    if provider == "gemini" and api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
            payload = {
                "instances": [{"prompt": full_prompt}],
                "parameters": {"sampleCount": 1, "aspectRatio": "9:16"},
            }
            r = requests.post(url, json=payload, timeout=90)
            if r.status_code == 200:
                b64 = r.json()["predictions"][0]["bytesBase64Encoded"]
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                return True
        except Exception as e:
            print(f"[Warn] Gemini Imagen fallback: {e}")

    # 2. Thử dùng OpenAI DALL-E 3 nếu có OpenAI API Key
    if provider == "openai" and api_key:
        try:
            url = "https://api.openai.com/v1/images/generations"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "dall-e-3",
                "prompt": full_prompt,
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

    # 3. Fallback tự động qua Pollinations Flux Image API (miễn phí, hỗ trợ ảnh dọc 800x1344)
    encoded = urllib.parse.quote(full_prompt)
    seed = int(time.time() * 1000) % 100000
    flux_url = f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=1344&seed={seed}&nologo=true&model=flux"
    r = requests.get(flux_url, timeout=90)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)
    return True


def create_full_webtoon_from_prompt(
    prompt: str, num_panels: int = 4, provider: str = "gemini", api_key: str = ""
) -> dict:
    """Hàm End-to-End: Từ 1 câu yêu cầu -> Sinh Storyboard -> Vẽ toàn bộ ảnh -> Typeset & Đóng gói ZIP."""
    sb = generate_storyboard_via_ai(prompt, num_panels, provider, api_key)
    project_id = slugify(sb.get("title", prompt))
    proj_dir = os.path.join(PROJECTS_DIR, project_id)
    os.makedirs(proj_dir, exist_ok=True)

    sb_path = os.path.join(proj_dir, "storyboard.json")
    with open(sb_path, "w", encoding="utf-8") as f:
        json.dump(sb, f, ensure_ascii=False, indent=2)

    char_bible = sb.get("character_bible", "")
    for idx, p_cfg in enumerate(sb.get("panels", []), start=1):
        raw_path = os.path.join(proj_dir, f"panel_{idx}_raw.jpg")
        generate_panel_image_via_ai(
            p_cfg.get("image_prompt", ""),
            char_bible,
            raw_path,
            provider,
            api_key,
        )

    return render_project(project_id)
