#!/usr/bin/env python3
"""
Khởi tạo sẵn 2 bộ truyện mẫu hoàn chỉnh trong thư mục projects/:
1. son_tinh_thuy_tinh (Sơn Tinh - Thủy Tinh: Đại Chiến Thần Linh - 5 khung hình)
2. thach_sanh (Dã Sử Dị Giới: Thạch Sanh - 4 khung hình)
"""
import os
import json
import shutil
from studio_engine import PROJECTS_DIR, render_project

ARTIFACT_DIR = "/home/nghia/.gemini/antigravity-cli/brain/736e78f7-050d-4df0-a16c-7165f93d1f37"


def seed_son_tinh_thuy_tinh():
    proj_id = "son_tinh_thuy_tinh"
    proj_dir = os.path.join(PROJECTS_DIR, proj_id)
    os.makedirs(proj_dir, exist_ok=True)

    raw_sources = [
        "storm_approaches_phong_chau_panel1_1792034376060.jpg",
        "thuy_tinh_wrath_panel2_1792034361901.jpg",
        "son_tinh_panel_3_1792034364921.jpg",
        "webtoon_panel4_clash_mountain_sea_1792034361636.jpg",
        "son_tinh_panel_5_dawn_1792034362941.jpg",
    ]
    for i, src_name in enumerate(raw_sources, start=1):
        shutil.copyfile(
            os.path.join(ARTIFACT_DIR, src_name),
            os.path.join(proj_dir, f"panel_{i}_raw.jpg"),
        )

    storyboard = {
        "title": "SƠN TINH - THỦY TINH: ĐẠI CHIẾN THẦN LINH",
        "subtitle": "CHƯƠNG 1: ĐẠI HỒNG THỦY PHONG CHÂU",
        "credits": "Nguyên tác: Truyền thuyết Việt Nam (Public Domain) • AI Webtoon Studio",
        "footer_title": "— MỖI NĂM BÃO LŨ QUAY VỀ: ĐÓN ĐỌC CHƯƠNG 2 —",
        "character_bible": (
            "Sơn Tinh: Noble 22-year-old Vietnamese Mountain Deity, raven-black hair in warrior knot, "
            "glowing amber-gold eyes, dark green & bronze armor with glowing golden Dong Son sun patterns. "
            "Thủy Tinh: Wrathful Sea Deity, flowing silver-white hair, glowing icy-blue eyes, "
            "dark abyssal dragon-scale armor with cyan runes, wielding a crackling lightning trident."
        ),
        "panels": [
            {
                "panel_index": 1,
                "scene_title": "Biến Cố Ngày Rước Dâu",
                "image_prompt": "Ancient Vietnamese royal citadel Phong Chau wedding procession overshadowed by a colossal black-and-cyan tsunami wave and lightning vortex.",
                "narrations": [
                    {
                        "text": "[KINH THÀNH PHONG CHÂU - NIÊN HIỆU HÙNG VƯƠNG THỨ 18]\nLễ vật sính lễ đã đủ. Sơn Tinh chính thức rước Mị Nương về núi Tản Viên.",
                        "x": 400,
                        "y": 95,
                        "w": 710,
                        "h": 100,
                        "border_color": [56, 189, 248, 235],
                        "text_color": [240, 249, 255, 255],
                        "font_size": 21,
                        "wrap": 44,
                    },
                    {
                        "text": "Nhưng ngay khoảnh khắc đoàn rước dâu bước qua cổng thành...\nCả bầu trời biển Đông bỗng nhiên sụp đổ!",
                        "x": 400,
                        "y": -95,
                        "w": 680,
                        "h": 95,
                        "border_color": [250, 204, 21, 235],
                        "text_color": [254, 249, 195, 255],
                        "font_size": 21,
                        "wrap": 42,
                    },
                ],
                "sfx": [
                    {
                        "text": "ẦM ĐOÀNGGG!!",
                        "x": 280,
                        "y": 460,
                        "font_size": 52,
                        "color": [103, 232, 249, 255],
                        "glow_color": [2, 132, 199, 255],
                        "angle": -10,
                    }
                ],
                "bubbles": [],
                "gutter_text": "Biển gầm thét... Vạn dặm sóng thần nuốt chửng cả chân trời!\nVị Thần Biển Cả đến muộn một bước đã hóa thành Cuồng Nộ!",
            },
            {
                "panel_index": 2,
                "scene_title": "Thủy Tinh Cưỡi Giao Long",
                "image_prompt": "Thủy Tinh with silver hair and cyan eyes in abyssal dragon armor standing atop a roaring sea dragon holding a lightning trident.",
                "narrations": [],
                "sfx": [
                    {
                        "text": "GÀOOOO—!!",
                        "x": 230,
                        "y": 760,
                        "font_size": 52,
                        "color": [165, 243, 252, 255],
                        "glow_color": [37, 99, 235, 255],
                        "angle": 8,
                    }
                ],
                "bubbles": [
                    {
                        "text": "SƠN TINH!!\nGiao Mị Nương ra đây!!",
                        "x": 235,
                        "y": 115,
                        "rx": 195,
                        "ry": 66,
                        "tail": [400, 290],
                        "dark_mode": True,
                        "font_size": 23,
                        "wrap": 22,
                    },
                    {
                        "text": "Bằng không, ta sẽ nhấn chìm\ncả giang sơn Phong Châu này\nxuống đáy biển sâu!!",
                        "x": 510,
                        "y": -110,
                        "rx": 245,
                        "ry": 82,
                        "tail": [455, -340],
                        "dark_mode": True,
                        "font_size": 22,
                        "wrap": 26,
                    },
                ],
                "gutter_text": "Trước cơn thịnh nộ muốn hủy diệt bách tính của Thủy Tinh...\nThánh Tản Viên bước lên vách đá, ánh mắt rực sáng kim quang!",
            },
            {
                "panel_index": 3,
                "scene_title": "Sơn Tinh Kích Hoạt Thần Trận",
                "image_prompt": "Sơn Tinh in Dong Son bronze sun armor kneeling on a cliff slamming his glowing golden hand into a runic circle cracking the earth.",
                "narrations": [
                    {
                        "text": "[THẦN THÔNG THỨC TỈNH: THÁI SƠN DI NHẠC TRẬN!]",
                        "x": 400,
                        "y": -85,
                        "w": 630,
                        "h": 76,
                        "border_color": [250, 204, 21, 255],
                        "text_color": [254, 240, 138, 255],
                        "font_size": 22,
                        "wrap": 45,
                    }
                ],
                "sfx": [
                    {
                        "text": "RẦMMM!!",
                        "x": 205,
                        "y": 825,
                        "font_size": 52,
                        "color": [253, 224, 71, 255],
                        "glow_color": [217, 119, 6, 255],
                        "angle": -10,
                    }
                ],
                "bubbles": [
                    {
                        "text": "Thủy Tinh! Ngươi vì tư tình\nmà gieo tai ương cho muôn dân...",
                        "x": 230,
                        "y": 100,
                        "rx": 215,
                        "ry": 66,
                        "tail": [390, 240],
                        "dark_mode": False,
                        "font_size": 21,
                        "wrap": 26,
                    },
                    {
                        "text": "Nước của ngươi dâng cao một trượng,\nNÚI CỦA TA SẼ VƯƠN CAO MƯỜI TRƯỢNG!",
                        "x": 555,
                        "y": 530,
                        "rx": 225,
                        "ry": 74,
                        "tail": [490, 350],
                        "dark_mode": False,
                        "font_size": 20,
                        "wrap": 26,
                    },
                ],
                "gutter_text": "Đại địa chấn động! Hồn thiêng sông núi Lạc Việt thức giấc!",
            },
            {
                "panel_index": 4,
                "scene_title": "Đại Chiến Dời Non Lấp Biển",
                "image_prompt": "Colossal golden rune mountain peaks erupting upward to block a monstrous dark tsunami wave and sea-serpent.",
                "narrations": [
                    {
                        "text": "Hàng vạn dãy núi đá khắc cổ tự Đông Sơn phá đất vươn lên,\nhóa thành bức tường thành bất khả xâm phạm!",
                        "x": 380,
                        "y": 100,
                        "w": 680,
                        "h": 95,
                        "border_color": [250, 204, 21, 240],
                        "text_color": [255, 251, 235, 255],
                        "font_size": 21,
                        "wrap": 44,
                    }
                ],
                "sfx": [
                    {
                        "text": "ĐOÀNGGG—!!",
                        "x": 450,
                        "y": 730,
                        "font_size": 62,
                        "color": [254, 240, 138, 255],
                        "glow_color": [234, 88, 12, 255],
                        "angle": -12,
                    }
                ],
                "bubbles": [
                    {
                        "text": "KHÔNG THỂ NÀO!!\nSức mạnh của đại địa...!!",
                        "x": 225,
                        "y": -110,
                        "rx": 200,
                        "ry": 66,
                        "tail": [290, -450],
                        "dark_mode": True,
                        "font_size": 22,
                        "wrap": 22,
                    }
                ],
                "gutter_text": "Cuộc đại chiến kéo dài suốt nhiều ngày đêm...\nCuối cùng, thủy triều kiệt sức phải rút về biển Đông.",
            },
            {
                "panel_index": 5,
                "scene_title": "Bình Minh Trên Đỉnh Tản Viên",
                "image_prompt": "Heroic back-view of Sơn Tinh standing on the highest peak of Mount Tản Viên at golden sunrise looking over the valley and receding ocean.",
                "narrations": [
                    {
                        "text": "Ánh bình minh chiếu rạng non sông Văn Lang.\nNhưng oán hận của Thủy Tinh vẫn chưa bao giờ dập tắt...",
                        "x": 400,
                        "y": 100,
                        "w": 670,
                        "h": 95,
                        "border_color": [250, 204, 21, 235],
                        "text_color": [254, 249, 195, 255],
                        "font_size": 21,
                        "wrap": 42,
                    },
                    {
                        "text": "Mỗi năm, khi mùa mưa bão kéo về, trận chiến giữa Núi và Biển\nlại một lần nữa tái diễn!",
                        "x": 400,
                        "y": -95,
                        "w": 670,
                        "h": 95,
                        "border_color": [56, 189, 248, 235],
                        "text_color": [224, 242, 254, 255],
                        "font_size": 21,
                        "wrap": 42,
                    },
                ],
                "sfx": [],
                "bubbles": [
                    {
                        "text": "Dù ngươi có quay lại bao nhiêu lần...\nTản Viên Sơn vẫn sẽ bảo vệ mảnh đất này!",
                        "x": 270,
                        "y": 350,
                        "rx": 240,
                        "ry": 72,
                        "tail": [450, 480],
                        "dark_mode": False,
                        "font_size": 21,
                        "wrap": 28,
                    }
                ],
                "gutter_text": "",
            },
        ],
    }

    with open(os.path.join(proj_dir, "storyboard.json"), "w", encoding="utf-8") as f:
        json.dump(storyboard, f, ensure_ascii=False, indent=2)

    res = render_project(proj_id)

    # Copy sang ARTIFACT_DIR để hiển thị ngay trong Artifact cho người dùng xem
    for i in range(1, 6):
        shutil.copyfile(
            os.path.join(proj_dir, f"panel_{i}_typeset.jpg"),
            os.path.join(ARTIFACT_DIR, f"sttt_panel_{i}_typeset.jpg"),
        )
    shutil.copyfile(
        os.path.join(proj_dir, "webtoon_full_strip.jpg"),
        os.path.join(ARTIFACT_DIR, "sttt_webtoon_full_strip.jpg"),
    )
    print("Seeded son_tinh_thuy_tinh:", res)


def seed_thach_sanh():
    proj_id = "thach_sanh"
    proj_dir = os.path.join(PROJECTS_DIR, proj_id)
    os.makedirs(proj_dir, exist_ok=True)

    raw_sources = [
        "panel_1_scenery_1792033368471.jpg",
        "panel_2_monster_reveal_1792033348260.jpg",
        "panel_3_1792033344292.jpg",
        "panel_4_1792033374641.jpg",
    ]
    for i, src_name in enumerate(raw_sources, start=1):
        shutil.copyfile(
            os.path.join(ARTIFACT_DIR, src_name),
            os.path.join(proj_dir, f"panel_{i}_raw.jpg"),
        )

    storyboard = {
        "title": "DÃ SỬ DỊ GIỚI: THẠCH SANH",
        "subtitle": "CHƯƠNG 1: HUYẾT XÀ TRONG MIẾU CỔ",
        "credits": "Nguyên tác: Cổ tích Việt Nam (Public Domain) • AI Webtoon Studio",
        "footer_title": "— ĐÓN ĐỌC CHƯƠNG 2: ÂM MƯU CỦA LÝ THÔNG —",
        "character_bible": "Thạch Sanh: 20-year-old Vietnamese warrior, raven-black hair, glowing cyan-gold eyes, dark indigo sleeveless tunic, wielding a battle axe with glowing cyan-gold runes.",
        "panels": [
            {
                "panel_index": 1,
                "scene_title": "Miếu Thần Đêm Mưa Bão",
                "image_prompt": "Ancient stone shrine in dark jungle thunderstorm with purple demonic aura.",
                "narrations": [
                    {
                        "text": "[MIẾU THẦN LINH - ĐÊM ĐINH DẬU]\nMỗi năm một mạng người... Đêm nay là kỳ hạn hiến tế.",
                        "x": 400,
                        "y": 110,
                        "w": 680,
                        "h": 105,
                        "border_color": [168, 85, 247, 230],
                        "text_color": [240, 240, 255, 255],
                        "font_size": 22,
                        "wrap": 42,
                    },
                    {
                        "text": "Kẻ lẽ ra phải nộp mạng là Lý Thông...\nNhưng người đang ngồi trong miếu lại là THẠCH SANH.",
                        "x": 400,
                        "y": -105,
                        "w": 640,
                        "h": 95,
                        "border_color": [56, 189, 248, 220],
                        "text_color": [240, 240, 255, 255],
                        "font_size": 21,
                        "wrap": 42,
                    },
                ],
                "sfx": [
                    {
                        "text": "ẦM ĐOÀNG!!",
                        "x": 240,
                        "y": 410,
                        "font_size": 50,
                        "color": [216, 180, 254, 255],
                        "glow_color": [126, 34, 206, 255],
                        "angle": -10,
                    }
                ],
                "bubbles": [],
                "gutter_text": "Bóng tối nuốt chửng ánh trăng...\nMột luồng sát khí thượng cổ trỗi dậy!",
            },
            {
                "panel_index": 2,
                "scene_title": "Chằn Tinh Xuất Hiện",
                "image_prompt": "Colossal demonic serpent-ogre monster Chằn Tinh with six glowing red eyes over ruined temple roof.",
                "narrations": [],
                "sfx": [
                    {
                        "text": "GRÀOOOOO—!!",
                        "x": 400,
                        "y": 110,
                        "font_size": 56,
                        "color": [254, 202, 202, 255],
                        "glow_color": [220, 38, 38, 255],
                        "angle": 5,
                    }
                ],
                "bubbles": [
                    {
                        "text": "Mùi máu phàm nhân...\nNgươi là vật tế đêm nay sao,\ncôn trùng nhỏ bé?!",
                        "x": 235,
                        "y": 835,
                        "rx": 205,
                        "ry": 82,
                        "tail": [330, 560],
                        "dark_mode": True,
                        "font_size": 22,
                        "wrap": 25,
                    }
                ],
                "gutter_text": "Đứng trước Đại Yêu khiến cả kinh thành khiếp đảm...\nChàng tiều phu trẻ chỉ khẽ nhếch môi.",
            },
            {
                "panel_index": 3,
                "scene_title": "Thạch Sanh Thức Tỉnh",
                "image_prompt": "Close-up of Thạch Sanh in pouring rain with glowing cyan-gold eyes and runic battle axe.",
                "narrations": [],
                "sfx": [
                    {
                        "text": "XẸT—!",
                        "x": 615,
                        "y": 575,
                        "font_size": 46,
                        "color": [103, 232, 249, 255],
                        "glow_color": [6, 182, 212, 255],
                        "angle": -14,
                    }
                ],
                "bubbles": [
                    {
                        "text": "Vật tế ư?\nTa e là ngươi nhầm rồi...",
                        "x": 205,
                        "y": 105,
                        "rx": 185,
                        "ry": 64,
                        "tail": [295, 225],
                        "dark_mode": False,
                        "font_size": 22,
                        "wrap": 22,
                    },
                    {
                        "text": "Đêm nay, ta đến để LẤY ĐẦU NGƯƠI!",
                        "x": 300,
                        "y": -100,
                        "rx": 255,
                        "ry": 68,
                        "tail": [415, 555],
                        "dark_mode": False,
                        "font_size": 23,
                        "wrap": 30,
                    },
                ],
                "gutter_text": "Một nhát rìu — Phân định sinh tử!",
            },
            {
                "panel_index": 4,
                "scene_title": "Tuyệt Kỹ Lôi Phủ Trảm",
                "image_prompt": "Thạch Sanh leaping through stormy sky swinging glowing cyan-gold lightning axe down at serpent monster.",
                "narrations": [
                    {
                        "text": "[THẦN KỸ KÍCH HOẠT]\nLÔI PHỦ TRẢM!",
                        "x": 195,
                        "y": 110,
                        "w": 340,
                        "h": 96,
                        "border_color": [34, 211, 238, 255],
                        "text_color": [165, 243, 252, 255],
                        "font_size": 23,
                        "wrap": 22,
                    }
                ],
                "sfx": [
                    {
                        "text": "ĐOÀNGGG!!",
                        "x": 530,
                        "y": 880,
                        "font_size": 60,
                        "color": [253, 224, 71, 255],
                        "glow_color": [6, 182, 212, 255],
                        "angle": -12,
                    }
                ],
                "bubbles": [],
                "gutter_text": "",
            },
        ],
    }

    with open(os.path.join(proj_dir, "storyboard.json"), "w", encoding="utf-8") as f:
        json.dump(storyboard, f, ensure_ascii=False, indent=2)

    res = render_project(proj_id)
    print("Seeded thach_sanh:", res)


if __name__ == "__main__":
    seed_son_tinh_thuy_tinh()
    seed_thach_sanh()
