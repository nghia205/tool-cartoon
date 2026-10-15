#!/usr/bin/env python3
"""
Khởi tạo sẵn TRỌN BỘ truyện tranh Webtoon hoàn chỉnh trong thư mục projects/:
1. son_tinh_thuy_tinh:
   - 4 Hồ sơ Nhân vật đồng bộ (Sơn Tinh, Thủy Tinh, Công chúa Mị Nương, Vua Hùng thứ 18)
   - Chương 1: Hội Kén Rể Thành Phong Châu (4 khung hình)
   - Chương 2: Sính Lễ Thần Kỳ & Cơn Thịnh Nộ Biển Đông (4 khung hình)
   - Chương 3: Đại Chiến Dời Non Lấp Biển & Hồi Kết Nghìn Năm (5 khung hình)
2. thach_sanh:
   - Chương 1: Huyết Xà Trong Miếu Cổ (4 khung hình)
"""
import os
import json
import shutil
from studio_engine import PROJECTS_DIR, render_project

ARTIFACT_DIR = "/home/nghia/.gemini/antigravity-cli/brain/736e78f7-050d-4df0-a16c-7165f93d1f37"


def seed_son_tinh_thuy_tinh_full_series():
    proj_id = "son_tinh_thuy_tinh"
    proj_dir = os.path.join(PROJECTS_DIR, proj_id)
    os.makedirs(proj_dir, exist_ok=True)

    # 1. Copy 4 Character Reference Sheets
    char_files = {
        "son_tinh": "son_tinh_character_sheet_1792036383809.jpg",
        "thuy_tinh": "thuy_tinh_character_sheet_1792036389062.jpg",
        "mi_nuong": "mi_nuong_character_sheet_1792036383817.jpg",
        "hung_vuong": "hung_vuong_character_sheet_1792036386892.jpg",
    }
    for cid, fname in char_files.items():
        shutil.copyfile(
            os.path.join(ARTIFACT_DIR, fname),
            os.path.join(proj_dir, f"char_{cid}_raw.jpg"),
        )

    # 2. Copy Raw Panels cho cả 3 Chương (Tổng cộng 13 khung hình xuyên suốt bộ truyện)
    chapter_raw_sources = {
        1: [
            "chapter1_panel1_royal_decree_1792036385352.jpg",
            "chapter1_panel2_arrival_two_gods_1792036392159.jpg",
            "phong_chau_contest_of_gods_1792036424266.jpg",
            "hung_vuong_decree_panel_1792036430019.jpg",
        ],
        2: [
            "son_tinh_sacred_beasts_dawn_1792036432079.jpg",
            "son_tinh_mi_nuong_ch2_p2_1792036428789.jpg",
            "thuy_tinh_fury_gate_1792036423186.jpg",
            "thuy_tinh_ocean_army_panel4_1792036420743.jpg",
        ],
        3: [
            "storm_approaches_phong_chau_panel1_1792034376060.jpg",
            "thuy_tinh_wrath_panel2_1792034361901.jpg",
            "son_tinh_panel_3_1792034364921.jpg",
            "webtoon_panel4_clash_mountain_sea_1792034361636.jpg",
            "son_tinh_panel_5_dawn_1792034362941.jpg",
        ],
    }

    for ch_idx, files in chapter_raw_sources.items():
        for p_idx, fname in enumerate(files, start=1):
            shutil.copyfile(
                os.path.join(ARTIFACT_DIR, fname),
                os.path.join(proj_dir, f"ch{ch_idx}_panel_{p_idx}_raw.jpg"),
            )

    storyboard = {
        "title": "SƠN TINH - THỦY TINH: ĐẠI CHIẾN THẦN LINH",
        "subtitle": "TRỌN BỘ TRUYỀN THUYẾT LẠC VIỆT (3 CHƯƠNG HOÀN CHỈNH)",
        "credits": "Nguyên tác: Truyền thuyết Việt Nam (Public Domain) • AI Webtoon Studio",
        "characters": [
            {
                "id": "son_tinh",
                "name": "Sơn Tinh (Thánh Tản Viên)",
                "role": "Chúa Tể Núi Tản Viên • Thần Hệ Kim - Thổ",
                "visual_dna": (
                    "22-year-old noble Vietnamese Mountain Deity, sharp heroic jawline, raven-black hair tied "
                    "in a high warrior topknot with a golden hairpin, glowing amber-gold eyes, wearing dark "
                    "forest-green and bronze scale armor etched with glowing golden Dong Son sun-drum patterns, "
                    "flowing dark green cape."
                ),
            },
            {
                "id": "thuy_tinh",
                "name": "Thủy Tinh (Thần Biển Đông)",
                "role": "Chúa Tể Đại Dương • Thần Hệ Thủy - Lôi",
                "visual_dna": (
                    "Fierce handsome Sea Deity, long flowing silver-white hair, glowing icy-blue eyes, "
                    "wearing dark abyssal black-blue dragon-scale armor etched with glowing cyan runes, "
                    "holding a crackling blue lightning trident."
                ),
            },
            {
                "id": "mi_nuong",
                "name": "Công Chúa Mị Nương",
                "role": "Ngọc Nữ Kinh Thành Phong Châu",
                "visual_dna": (
                    "Breathtakingly beautiful 18-year-old ancient Vietnamese royal princess, long silky "
                    "raven-black hair adorned with an ornate golden Lac bird phoenix crown, warm golden-brown eyes, "
                    "wearing regal crimson-and-ivory silk royal robes embroidered with golden lotus motifs."
                ),
            },
            {
                "id": "hung_vuong",
                "name": "Hùng Vương Thứ 18",
                "role": "Quốc Vương Nước Văn Lang",
                "visual_dna": (
                    "Majestic 55-year-old warrior-king with a long silver-streaked beard, sharp wise eyes, "
                    "wearing an ornate golden feathered Lac Viet royal crown and grand black-red-and-gold "
                    "bronze-armored royal robes, holding a golden dragon scepter."
                ),
            },
        ],
        "chapters": [
            # ==================================================================
            # CHƯƠNG 1: HỘI KÉN RỂ THÀNH PHONG CHÂU
            # ==================================================================
            {
                "chapter_index": 1,
                "chapter_title": "CHƯƠNG 1: HỘI KÉN RỂ THÀNH PHONG CHÂU",
                "footer_title": "— HẾT CHƯƠNG 1: ĐÓN ĐỌC CHƯƠNG 2 - SÍNH LỄ THẦN KỲ —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Chiếu Chỉ Của Vua Hùng",
                        "characters_present": ["hung_vuong", "mi_nuong"],
                        "image_prompt": "Grand ancient Vietnamese throne hall with King Hùng Vương on bronze throne and Princess Mị Nương standing beside him.",
                        "narrations": [
                            {
                                "text": "[KINH THÀNH PHONG CHÂU - NƯỚC VĂN LANG]\nVua Hùng thứ 18 có người con gái tuyệt sắc tên là Mị Nương.",
                                "x": 400,
                                "y": 95,
                                "w": 680,
                                "h": 95,
                                "border_color": [250, 204, 21, 240],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 21,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Ái nữ của ta đã đến tuổi cập kê.\nTa muốn tìm một bậc kỳ tài xứng đáng\nđể gả Mị Nương!",
                                "x": 270,
                                "y": -115,
                                "rx": 240,
                                "ry": 78,
                                "tail": [380, -380],
                                "dark_mode": False,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "Chiếu kén rể vừa ban ra, anh hào khắp bốn phương nô nức kéo về.\nNhưng nổi bật nhất là sự xuất hiện của HAI VỊ THẦN!",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Nhất Sơn Nhất Hải Tươngùng",
                        "characters_present": ["son_tinh", "thuy_tinh"],
                        "image_prompt": "Split-aura face-off between Sơn Tinh (left, golden aura) and Thủy Tinh (right, cyan lightning aura).",
                        "narrations": [
                            {
                                "text": "Một người là SƠN TINH — Chúa tể vùng núi Tản Viên.\nMột người là THỦY TINH — Bá chủ vùng biển Đông thẳm sâu!",
                                "x": 400,
                                "y": 95,
                                "w": 690,
                                "h": 95,
                                "border_color": [56, 189, 248, 235],
                                "text_color": [240, 249, 255, 255],
                                "font_size": 21,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "XẸT ĐOÀNG!!",
                                "x": 400,
                                "y": 245,
                                "font_size": 48,
                                "color": [253, 224, 71, 255],
                                "glow_color": [6, 182, 212, 255],
                                "angle": -6,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Mị Nương phải thuộc về\nChúa tể biển khơi!",
                                "x": 570,
                                "y": -105,
                                "rx": 195,
                                "ry": 65,
                                "tail": [630, -320],
                                "dark_mode": True,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "Để phân định cao thấp trước điện rồng...\nCả hai vị thần lập tức thi triển đại thần thông!",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Tỷ Thí Đại Thần Thông",
                        "characters_present": ["son_tinh", "thuy_tinh"],
                        "image_prompt": "Sơn Tinh summoning golden jade pillars vs Thủy Tinh summoning cyan water dragons in palace courtyard.",
                        "narrations": [
                            {
                                "text": "Thủy Tinh hô gió gọi mưa, triệu hồi Thủy Long rung chuyển đất trời.\nSơn Tinh vẫy tay dựng vách ngọc, dời non chặn đứng cuồng phong!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [250, 204, 21, 235],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "ẦMMM—!!",
                                "x": 410,
                                "y": -110,
                                "font_size": 56,
                                "color": [103, 232, 249, 255],
                                "glow_color": [37, 99, 235, 255],
                                "angle": -8,
                            }
                        ],
                        "bubbles": [],
                        "gutter_text": "Kẻ tám lạng, người nửa cân! Cả hai đều mang sức mạnh kinh thiên động địa.\nVua Hùng đành đưa ra một thử thách cuối cùng...",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Thách Cưới Tam Linh Thú",
                        "characters_present": ["hung_vuong"],
                        "image_prompt": "King Hùng Vương raising golden dragon scepter with glowing visions of Nine-Tusked Elephant, Nine-Spurred Rooster, Nine-Maned Horse.",
                        "narrations": [
                            {
                                "text": "[THÁNH CHỈ THÁCH CƯỚI]\nVoi chín ngà • Gà chín cựa • Ngựa chín hồng mao!",
                                "x": 400,
                                "y": 85,
                                "w": 640,
                                "h": 92,
                                "border_color": [250, 204, 21, 255],
                                "text_color": [254, 240, 138, 255],
                                "font_size": 22,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Ngày mai, ai mang đủ sính lễ Tam Linh Thú\nđến trước sẽ được rước Mị Nương về dinh!",
                                "x": 400,
                                "y": -95,
                                "rx": 280,
                                "ry": 72,
                                "tail": [430, -340],
                                "dark_mode": False,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "",
                    },
                ],
            },
            # ==================================================================
            # CHƯƠNG 2: SÍNH LỄ THẦN KỲ & CƠN THỊNH NỘ BIỂN ĐÔNG
            # ==================================================================
            {
                "chapter_index": 2,
                "chapter_title": "CHƯƠNG 2: SÍNH LỄ THẦN KỲ & CƠN THỊNH NỘ BIỂN ĐÔNG",
                "footer_title": "— HẾT CHƯƠNG 2: ĐÓN ĐỌC CHƯƠNG 3 - ĐẠI CHIẾN DỜI NON LẤP BIỂN —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Sơn Tinh Dâng Tam Linh Thú",
                        "characters_present": ["son_tinh"],
                        "image_prompt": "Sơn Tinh at golden dawn before Phong Châu gates leading Nine-Tusked Elephant, Nine-Spurred Rooster, Nine-Maned Red Horse.",
                        "narrations": [
                            {
                                "text": "[CANH NĂM SÁNG HÔM SAU - CỔNG THÀNH PHONG CHÂU]\nKhi sương sớm còn chưa tan, Sơn Tinh đã dẫn Tam Linh Thú tiến vào thành!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [250, 204, 21, 240],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Bẩm Quốc Vương! Sơn Tinh đã mang đủ\nVoi chín ngà, Gà chín cựa, Ngựa chín hồng mao\nđến nghinh đón Công chúa!",
                                "x": 400,
                                "y": -100,
                                "rx": 285,
                                "ry": 82,
                                "tail": [420, -360],
                                "dark_mode": False,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "Giữ đúng lời hứa vàng ngọc của bậc quân vương,\nVua Hùng bằng lòng cho Sơn Tinh rước Mị Nương về núi Tản Viên!",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Rước Nàng Về Dinh Núi Tản",
                        "characters_present": ["son_tinh", "mi_nuong"],
                        "image_prompt": "Romantic shot of Sơn Tinh holding Princess Mị Nương's hand on mountain path with floating blossoms.",
                        "narrations": [],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Từ nay núi Tản Viên sẽ là nhà của nàng.\nTa thề dùng cả sinh mệnh bảo vệ nàng bình yên!",
                                "x": 280,
                                "y": 100,
                                "rx": 255,
                                "ry": 72,
                                "tail": [390, 260],
                                "dark_mode": False,
                                "font_size": 20,
                            },
                            {
                                "text": "Thiếp nguyện cùng chàng\nđi đến chân trời góc bể...",
                                "x": 540,
                                "y": -100,
                                "rx": 205,
                                "ry": 65,
                                "tail": [620, -380],
                                "dark_mode": False,
                                "font_size": 21,
                            },
                        ],
                        "gutter_text": "Thế nhưng... đúng lúc đoàn rước dâu vừa khuất bóng sau rặng núi,\nmột kẻ đến muộn đã đặt chân tới cổng thành Phong Châu!",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Cơn Thịnh Nộ Của Kẻ Đến Muộn",
                        "characters_present": ["thuy_tinh"],
                        "image_prompt": "Close-up of Thủy Tinh before closed gates of Phong Châu, eyes exploding with cyan-crimson rage shattering the stone floor.",
                        "narrations": [
                            {
                                "text": "Đến muộn chỉ một khắc... Cổng thành đã khép, người thương đã thuộc về kẻ khác!",
                                "x": 400,
                                "y": 90,
                                "w": 700,
                                "h": 88,
                                "border_color": [56, 189, 248, 240],
                                "text_color": [224, 242, 254, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "RẮC RẦMMM!!",
                                "x": 520,
                                "y": 860,
                                "font_size": 52,
                                "color": [103, 232, 249, 255],
                                "glow_color": [37, 99, 235, 255],
                                "angle": -10,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "SƠN TINH!! Ngươi dám cướp Mị Nương\ncủa ta sao?!",
                                "x": 285,
                                "y": -95,
                                "rx": 245,
                                "ry": 68,
                                "tail": [430, -450],
                                "dark_mode": True,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "Uất hận ngút trời! Thủy Tinh hóa giải phong ấn biển sâu,\ntriệu hồi đại quân thủy tộc truy sát đoàn rước dâu!",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Hiệu Lệnh Vạn Quân Thủy Tộc",
                        "characters_present": ["thuy_tinh"],
                        "image_prompt": "Thủy Tinh floating in stormy sky raising lightning trident commanding giant sea serpents, krakens, and abyssal water army.",
                        "narrations": [
                            {
                                "text": "[THỦY THẦN HIỆU LỆNH: VẠN HẢI TRIỀU DÂNG!]",
                                "x": 400,
                                "y": 85,
                                "w": 580,
                                "h": 76,
                                "border_color": [56, 189, 248, 255],
                                "text_color": [165, 243, 252, 255],
                                "font_size": 22,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "CUỘN TRÀO!!",
                                "x": 240,
                                "y": 630,
                                "font_size": 50,
                                "color": [103, 232, 249, 255],
                                "glow_color": [2, 132, 199, 255],
                                "angle": 8,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Hỡi vạn quân biển Đông!\nHãy dâng sóng thần nuốt chửng núi Tản Viên cho ta!!",
                                "x": 400,
                                "y": -95,
                                "rx": 290,
                                "ry": 72,
                                "tail": [460, -550],
                                "dark_mode": True,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "",
                    },
                ],
            },
            # ==================================================================
            # CHƯƠNG 3: ĐẠI CHIẾN DỜI NON LẤP BIỂN & HỒI KẾT NGHÌN NĂM
            # ==================================================================
            {
                "chapter_index": 3,
                "chapter_title": "CHƯƠNG 3: ĐẠI CHIẾN DỜI NON LẤP BIỂN & HỒI KẾT NGHÌN NĂM",
                "footer_title": "— ĐẠI KẾT CỤC: TRỌN BỘ SƠN TINH - THỦY TINH —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Đại Hồng Thủy Ập Tới",
                        "characters_present": ["son_tinh", "thuy_tinh"],
                        "image_prompt": "Ancient Vietnamese royal citadel Phong Chau overshadowed by a colossal black-and-cyan tsunami wave and lightning vortex.",
                        "narrations": [
                            {
                                "text": "[ĐƯỜNG VỀ NÚI TẢN VIÊN]\nSóng thần cao hàng trăm trượng bất ngờ dựng đứng phía chân trời!",
                                "x": 400,
                                "y": 95,
                                "w": 690,
                                "h": 95,
                                "border_color": [56, 189, 248, 235],
                                "text_color": [240, 249, 255, 255],
                                "font_size": 21,
                            },
                            {
                                "text": "Mưa đổ như trút nước, sấm chớp rạch ngang bầu trời.\nCả vùng đồng bằng phút chốc chìm trong biển nước mênh mông!",
                                "x": 400,
                                "y": -95,
                                "w": 690,
                                "h": 95,
                                "border_color": [250, 204, 21, 235],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 21,
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
                        "gutter_text": "Giữa tâm bão tối tăm mù mịt...\nThủy Tinh cưỡi Giao Long khổng lồ xuất hiện!",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Thủy Tinh Cưỡi Giao Long",
                        "characters_present": ["thuy_tinh"],
                        "image_prompt": "Thủy Tinh in abyssal dragon armor standing atop a roaring sea dragon holding a lightning trident.",
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
                            },
                            {
                                "text": "Bằng không, ta sẽ nhấn chìm cả giang sơn này\nxuống đáy biển sâu!!",
                                "x": 510,
                                "y": -110,
                                "rx": 245,
                                "ry": 78,
                                "tail": [455, -340],
                                "dark_mode": True,
                                "font_size": 21,
                            },
                        ],
                        "gutter_text": "Trước cơn thịnh nộ muốn hủy diệt bách tính của Thủy Tinh...\nThánh Tản Viên bước lên vách đá, ánh mắt rực sáng kim quang!",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Sơn Tinh Kích Hoạt Thần Trận",
                        "characters_present": ["son_tinh"],
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
                            },
                        ],
                        "gutter_text": "Đại địa chấn động! Hồn thiêng sông núi Lạc Việt thức giấc!",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Đại Chiến Dời Non Lấp Biển",
                        "characters_present": ["son_tinh", "thuy_tinh"],
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
                            }
                        ],
                        "gutter_text": "Cuộc đại chiến kéo dài suốt nhiều ngày đêm...\nCuối cùng, thủy triều kiệt sức phải rút về biển Đông.",
                    },
                    {
                        "panel_index": 5,
                        "scene_title": "Bình Minh Trên Đỉnh Tản Viên",
                        "characters_present": ["son_tinh"],
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
                            }
                        ],
                        "gutter_text": "",
                    },
                ],
            },
        ],
    }

    with open(os.path.join(proj_dir, "storyboard.json"), "w", encoding="utf-8") as f:
        json.dump(storyboard, f, ensure_ascii=False, indent=2)

    res = render_project(proj_id)

    # Copy toàn bộ ảnh sang ARTIFACT_DIR để hiển thị trực tiếp trong Artifact cho người dùng
    for cid in char_files:
        shutil.copyfile(
            os.path.join(proj_dir, f"char_{cid}_sheet.jpg"),
            os.path.join(ARTIFACT_DIR, f"char_{cid}_sheet.jpg"),
        )
    for ch_idx in [1, 2, 3]:
        p_count = 5 if ch_idx == 3 else 4
        for p_idx in range(1, p_count + 1):
            shutil.copyfile(
                os.path.join(proj_dir, f"ch{ch_idx}_panel_{p_idx}_typeset.jpg"),
                os.path.join(ARTIFACT_DIR, f"sttt_ch{ch_idx}_p{p_idx}_typeset.jpg"),
            )

    print("Seeded FULL SERIES son_tinh_thuy_tinh:", res)


if __name__ == "__main__":
    seed_son_tinh_thuy_tinh_full_series()
    render_project("thach_sanh")
