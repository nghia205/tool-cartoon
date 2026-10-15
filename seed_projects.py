#!/usr/bin/env python3
"""
Khởi tạo sẵn TRỌN BỘ các bộ truyện tranh Webtoon hoàn chỉnh trong thư mục projects/:
1. tam_cam (Tấm Cám: Phượng Hoàng Niết Bàn - 4 Nhân vật + 3 Chương / 12 Khung hình)
2. son_tinh_thuy_tinh (Sơn Tinh - Thủy Tinh: Đại Chiến Thần Linh - 4 Nhân vật + 3 Chương / 13 Khung hình)
3. thach_sanh (Dã Sử Dị Giới: Thạch Sanh - 1 Chương / 4 Khung hình)
"""
import os
import json
import shutil
from studio_engine import PROJECTS_DIR, render_project

ARTIFACT_DIR = "/home/nghia/.gemini/antigravity-cli/brain/736e78f7-050d-4df0-a16c-7165f93d1f37"


def seed_tam_cam_full_series():
    proj_id = "tam_cam"
    proj_dir = os.path.join(PROJECTS_DIR, proj_id)
    os.makedirs(proj_dir, exist_ok=True)

    # 1. Copy 4 Character Reference Sheets
    char_files = {
        "tam": "tam_empress_reference_sheet_1792037847349.jpg",
        "hoang_tu": "young_dragon_king_fullbody_sheet_1792037875053.jpg",
        "cam": "cam_character_reference_sheet_1792037850950.jpg",
        "di_ghe": "di_ghe_character_sheet_1792037851611.jpg",
    }
    for cid, fname in char_files.items():
        shutil.copyfile(
            os.path.join(ARTIFACT_DIR, fname),
            os.path.join(proj_dir, f"char_{cid}_raw.jpg"),
        )

    # 2. Copy Raw Panels cho cả 3 Chương (Tổng cộng 12 khung hình từ đầu đến kết cục)
    chapter_raw_sources = {
        1: [
            "tam_cam_ch1_panel1_png_1792037851789.jpg",
            "tam_cam_ch1_panel2_sparrows_golden_slippers_1792037852664.jpg",
            "prince_finds_golden_slipper_1792037919809.jpg",
            "tam_cam_ch1_p4_royal_betrothal_1792037922723.jpg",
        ],
        2: [
            "tam_cam_ch2_betrayal_areca_palm_1792037919303.jpg",
            "ch2_panel2_golden_oriole_returns_1792037983338.jpg",
            "ch2_panel3_golden_persimmon_notext_1792037947394.jpg",
            "tam_cam_ch2_p4_reunion_1792037989996.jpg",
        ],
        3: [
            "chapter3_panel1_empress_tam_return_1792037987506.jpg",
            "cam_kneels_before_empress_tam_1792038025967.jpg",
            "ch3_panel3_karmic_retribution_1792037989407.jpg",
            "webtoon_ch3_panel4_finale_1792037987199.jpg",
        ],
    }

    for ch_idx, files in chapter_raw_sources.items():
        for p_idx, fname in enumerate(files, start=1):
            shutil.copyfile(
                os.path.join(ARTIFACT_DIR, fname),
                os.path.join(proj_dir, f"ch{ch_idx}_panel_{p_idx}_raw.jpg"),
            )

    storyboard = {
        "title": "TẤM CÁM: PHƯỢNG HOÀNG NIẾT BÀN",
        "subtitle": "TRỌN BỘ CỔ TÍCH VIỆT NAM (3 CHƯƠNG HOÀN CHỈNH)",
        "credits": "Nguyên tác: Cổ tích Việt Nam (Public Domain) • AI Webtoon Studio",
        "characters": [
            {
                "id": "tam",
                "name": "Tấm (Hoàng Hậu Phượng Hoàng)",
                "role": "Nữ chính • Từ Thôn Nữ Dịu Dàng Đến Mẫu Nghi Thiên Hạ",
                "visual_dna": (
                    "Breathtakingly beautiful 18-year-old ancient Vietnamese maiden who becomes Empress, "
                    "silky waist-length raven-black hair adorned with a glowing golden phoenix-and-lotus hairpin, "
                    "luminous warm amber-gold eyes, wearing ornate crimson, peach-pink, and gold Vietnamese royal silk robes."
                ),
            },
            {
                "id": "hoang_tu",
                "name": "Quốc Vương (Minh Quân Nước Nam)",
                "role": "Nam chính • Vị Vua Trẻ Si Tình & Uy Nghiêm",
                "visual_dna": (
                    "Strikingly handsome 21-year-old Vietnamese monarch, sharp noble jawline, raven-black hair "
                    "crowned with a golden dragon coronet, warm deep golden eyes, wearing grand black-and-gold "
                    "royal dragon-embroidered robes with a crimson silk inner collar."
                ),
            },
            {
                "id": "cam",
                "name": "Cám (Ác Nữ Đố Kỵ)",
                "role": "Phản diện • Người Em Cùng Cha Khác Mẹ Tham Lam",
                "visual_dna": (
                    "17-year-old scheming villainess stepsister, sharp upturned fox-like dark eyes, arrogant "
                    "jealous smirk, black hair pinned with silver hairpins, wearing flashy violet-and-magenta silk robes."
                ),
            },
            {
                "id": "di_ghe",
                "name": "Bà Dì Ghẻ (Mẹ Cám)",
                "role": "Phản diện • Người Mẹ Kế Độc Ác & Thâm Hiểm",
                "visual_dna": (
                    "45-year-old cold, calculating matriarch villainess, sharp high cheekbones, narrow scheming eyes, "
                    "hair coiled tightly in a dark bun, wearing dark plum-and-gold brocade traditional robes."
                ),
            },
        ],
        "chapters": [
            # ==================================================================
            # CHƯƠNG 1: GIỎ TÉP, CÁ BỐNG & ĐÔI HÀI THÊU CHỈ VÀNG
            # ==================================================================
            {
                "chapter_index": 1,
                "chapter_title": "CHƯƠNG 1: ĐÔI HÀI THÊU CHỈ VÀNG & LỄ LẬP HẬU",
                "footer_title": "— HẾT CHƯƠNG 1: ĐÓN ĐỌC CHƯƠNG 2 - KIẾP NẠN & HÓA THÂN —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Giọt Nước Mắt Bên Đầm Sen & Ông Bụt",
                        "characters_present": ["tam"],
                        "image_prompt": "Young Tấm weeping beside an empty basket by a sunset lotus pond as Ông Bụt materializes in golden light.",
                        "narrations": [
                            {
                                "text": "Mồ côi cha mẹ từ sớm, Tấm phải sống cảnh cơ cực dưới đòn roi\nvà sự lừa lọc của mẹ con Dì Ghẻ...",
                                "x": 400,
                                "y": 95,
                                "w": 680,
                                "h": 95,
                                "border_color": [250, 204, 21, 235],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Làm sao con khóc?\nHãy nhìn vào trong giỏ xem còn gì không...",
                                "x": 270,
                                "y": 320,
                                "rx": 245,
                                "ry": 70,
                                "tail": [430, 250],
                                "dark_mode": False,
                                "font_size": 21,
                            },
                            {
                                "text": "Chị Cám lừa trút hết tép của con rồi...\nChỉ còn duy nhất một con cá Bống nhỏ!",
                                "x": 400,
                                "y": -95,
                                "rx": 275,
                                "ry": 72,
                                "tail": [320, -280],
                                "dark_mode": False,
                                "font_size": 21,
                            },
                        ],
                        "gutter_text": "Mẹ con Cám nhẫn tâm giết cả cá Bống rồi trộn thóc với gạo bắt Tấm nhặt\nđể ngăn nàng đi trẩy hội kinh thành... Nhưng phép màu một lần nữa giáng lâm!",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Đàn Chim Sẻ Thần & Đôi Hài Kim Phượng",
                        "characters_present": ["tam"],
                        "image_prompt": "Flock of glowing golden sparrows sorting rice as golden phoenix silk slippers materialize before Tấm.",
                        "narrations": [
                            {
                                "text": "Ông Bụt gọi vạn cánh chim sẻ xuống nhặt thóc giúp Tấm,\nrồi từ tro cốt cá Bống hóa ra y phục lụa tiên và Đôi Hài Kim Phượng!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [250, 204, 21, 240],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "LẤP LÁNH!!",
                                "x": 540,
                                "y": 650,
                                "font_size": 44,
                                "color": [253, 224, 71, 255],
                                "glow_color": [234, 179, 8, 255],
                                "angle": -8,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Đôi hài thêu chỉ vàng đẹp quá...\nCon có thể đến kinh thành dự hội rồi!",
                                "x": 275,
                                "y": -95,
                                "rx": 255,
                                "ry": 70,
                                "tail": [330, -350],
                                "dark_mode": False,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "Trên đường trẩy hội qua cầu, Tấm vô tình đánh rơi một chiếc hài xuống suối...\nCũng chính là lúc đoàn ngự giá của Quốc Vương trẻ tuổi đi ngang qua!",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Quốc Vương Nhặt Chiếc Hài Vàng",
                        "characters_present": ["hoang_tu"],
                        "image_prompt": "Handsome young Vietnamese King holding up a glowing golden phoenix silk slipper beside his white warhorse.",
                        "narrations": [
                            {
                                "text": "Voi ngựa ngự giá bỗng dừng bước trước hào quang tỏa ra từ dòng suối...",
                                "x": 400,
                                "y": 85,
                                "w": 690,
                                "h": 80,
                                "border_color": [250, 204, 21, 235],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Chiếc hài thêu chỉ vàng tinh xảo nhường này,\nchủ nhân của nó ắt hẳn là bậc giai nhân tuyệt sắc!",
                                "x": 290,
                                "y": 210,
                                "rx": 275,
                                "ry": 72,
                                "tail": [410, 320],
                                "dark_mode": False,
                                "font_size": 20,
                            },
                            {
                                "text": "Truyền lệnh khắp kinh thành: Hễ cô gái nào\nướm vừa chiếc hài này, trẫm sẽ lập làm Hoàng Hậu!",
                                "x": 400,
                                "y": -95,
                                "rx": 295,
                                "ry": 74,
                                "tail": [450, -320],
                                "dark_mode": False,
                                "font_size": 20,
                            },
                        ],
                        "gutter_text": "Hàng ngàn tiểu thư quyền quý và cả Cám đều cố ướm thử nhưng vô vọng.\nCho đến khi Tấm bước ra...",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Chân Tình Ướm Vừa Hài Phượng",
                        "characters_present": ["tam", "hoang_tu", "cam", "di_ghe"],
                        "image_prompt": "Handsome King kneeling to fit the glowing golden slipper onto Tấm's foot while Cám and Stepmother watch in shocked envy.",
                        "narrations": [
                            {
                                "text": "Khoảnh khắc bàn chân Tấm chạm vào chiếc hài, kim quang bừng sáng!\nĐôi hài vừa như in, định sẵn duyên phận Đế - Hậu!",
                                "x": 400,
                                "y": 95,
                                "w": 690,
                                "h": 95,
                                "border_color": [250, 204, 21, 245],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Cuối cùng trẫm cũng tìm thấy nàng!\nHãy theo trẫm về cung làm Hoàng Hậu!",
                                "x": 270,
                                "y": -95,
                                "rx": 255,
                                "ry": 70,
                                "tail": [320, -360],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "",
                    },
                ],
            },
            # ==================================================================
            # CHƯƠNG 2: ÂM MƯU NGÀY GIỖ CHA & SỰ HÓA THÂN BẤT DIỆT
            # ==================================================================
            {
                "chapter_index": 2,
                "chapter_title": "CHƯƠNG 2: ÂM MƯU NGÀY GIỖ CHA & SỰ HÓA THÂN BẤT DIỆT",
                "footer_title": "— HẾT CHƯƠNG 2: ĐÓN ĐỌC CHƯƠNG 3 - PHƯỢNG HOÀNG NIẾT BÀN —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Tội Ác Dưới Gốc Cây Cau",
                        "characters_present": ["tam", "cam", "di_ghe"],
                        "image_prompt": "Stepmother and Cám chopping the base of a tall swaying areca palm tree in a storm while Tấm clings to the top.",
                        "narrations": [
                            {
                                "text": "[NGÀY GIỖ CHA]\nTấm hiếu thảo xin phép về quê làm giỗ cha, nào ngờ rơi vào bẫy tử thần!",
                                "x": 400,
                                "y": 90,
                                "w": 690,
                                "h": 92,
                                "border_color": [239, 68, 68, 240],
                                "text_color": [254, 226, 226, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "PHẬP! RẮC!!",
                                "x": 480,
                                "y": 640,
                                "font_size": 52,
                                "color": [254, 202, 202, 255],
                                "glow_color": [220, 38, 38, 255],
                                "angle": -10,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Dì ơi! Chị Cám ơi! Sao lại chặt gốc cau?!",
                                "x": 240,
                                "y": 230,
                                "rx": 225,
                                "ry": 64,
                                "tail": [390, 180],
                                "dark_mode": False,
                                "font_size": 20,
                            },
                            {
                                "text": "Chị Tấm cứ chết đi!\nNgôi Hoàng Hậu từ nay sẽ thuộc về Cám!!",
                                "x": 400,
                                "y": -95,
                                "rx": 265,
                                "ry": 72,
                                "tail": [520, -320],
                                "dark_mode": True,
                                "font_size": 21,
                            },
                        ],
                        "gutter_text": "Dì Ghẻ đưa Cám vào cung thế chỗ... Nhưng chân hồn của Tấm bất diệt,\nhóa thành chim Vàng Anh bay thẳng về hoàng cung!",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Linh Hồn Chim Vàng Anh",
                        "characters_present": ["hoang_tu", "tam", "cam"],
                        "image_prompt": "Young King holding out his hand as a glowing golden Oriole bird lands with Tấm's spiritual silhouette behind it.",
                        "narrations": [],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Vàng ảnh vàng anh, có phải vợ anh\nchui vào tay áo...",
                                "x": 270,
                                "y": 100,
                                "rx": 245,
                                "ry": 70,
                                "tail": [360, 290],
                                "dark_mode": False,
                                "font_size": 21,
                            },
                            {
                                "text": "Không thể nào... Con chim đó\nmang linh hồn của chị Tấm sao?!",
                                "x": 520,
                                "y": -95,
                                "rx": 240,
                                "ry": 70,
                                "tail": [650, -340],
                                "dark_mode": True,
                                "font_size": 20,
                            },
                        ],
                        "gutter_text": "Mẹ con Cám điên cuồng sát hại Vàng Anh, chặt cây Xoan Đào, đốt cả khung cửi...\nNhưng từ đống tro tàn, một cây Thị thần kỳ vươn lên giữa trời đất!",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Quả Thị Vàng & Bà Lão Hàng Nước",
                        "characters_present": ["tam"],
                        "image_prompt": "Glowing golden persimmon fruit dropping into the woven bag of a kind elderly village woman.",
                        "narrations": [
                            {
                                "text": "Từ giọt máu và tro tàn của khung cửi,\nkết thành một quả Thị vàng rực tỏa hương thơm ngát khắp vùng!",
                                "x": 400,
                                "y": 95,
                                "w": 680,
                                "h": 95,
                                "border_color": [250, 204, 21, 240],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Thị ơi thị rụng bị bà,\nBà để bà ngửi chứ bà không ăn...",
                                "x": 380,
                                "y": -95,
                                "rx": 265,
                                "ry": 72,
                                "tail": [430, -330],
                                "dark_mode": False,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "Hàng ngày Tấm từ quả Thị bước ra giúp bà lão dọn nhà và têm trầu cánh phượng.\nCho đến một ngày, Quốc Vương dừng chân ghé quán nước...",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Miếng Trầu Cánh Phượng & Ngày Trùng Phùng",
                        "characters_present": ["tam", "hoang_tu"],
                        "image_prompt": "Tấm stepping out of golden aura with phoenix-wing betel leaves as the young King embraces her with tears of joy.",
                        "narrations": [
                            {
                                "text": "Nhìn miếng trầu têm cánh phượng quen thuộc, trái tim nhà Vua run lên!\nKhi Tấm bước ra trong ánh hào quang, đôi uyên ương vỡ òa trùng phùng!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [250, 204, 21, 245],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Tấm! Đúng là nàng rồi!\nTrẫm thề không bao giờ để ai hãm hại nàng nữa!",
                                "x": 400,
                                "y": -95,
                                "rx": 280,
                                "ry": 72,
                                "tail": [420, -380],
                                "dark_mode": False,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "",
                    },
                ],
            },
            # ==================================================================
            # CHƯƠNG 3: PHƯỢNG HOÀNG TRỞ LẠI & SỰ PHÁN XỬ CUỐI CÙNG
            # ==================================================================
            {
                "chapter_index": 3,
                "chapter_title": "CHƯƠNG 3: PHƯỢNG HOÀNG TRỞ LẠI & PHÁN XỬ CUỐI CÙNG",
                "footer_title": "— ĐẠI KẾT CỤC: TRỌN BỘ TẤM CÁM - PHƯỢNG HOÀNG NIẾT BÀN —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Hoàng Hậu Tấm Uy Nghi Hồi Cung",
                        "characters_present": ["tam", "hoang_tu"],
                        "image_prompt": "Empress Tấm in crimson-and-gold phoenix robes walking hand-in-hand with the young King up the grand palace staircase.",
                        "narrations": [
                            {
                                "text": "[ĐẠI ĐIỆN HOÀNG CUNG]\nTrải qua muôn trùng sinh tử, Phượng Hoàng tái sinh càng thêm rực rỡ uy quyền!",
                                "x": 400,
                                "y": 95,
                                "w": 700,
                                "h": 95,
                                "border_color": [250, 204, 21, 245],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Cung nghinh Hoàng Hậu nương nương hồi cung!\nVạn tuế! Vạn vạn tuế!",
                                "x": 400,
                                "y": -95,
                                "rx": 275,
                                "ry": 72,
                                "tail": [260, -280],
                                "dark_mode": False,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "Trước dung nhan tuyệt mỹ như tiên giáng trần của Tấm,\nCám vừa khiếp sợ vừa bị lòng đố kỵ làm cho mờ mắt...",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Lời Phán Từ Ngai Vàng Phượng Hoàng",
                        "characters_present": ["tam", "cam"],
                        "image_prompt": "Empress Tấm looking down serenely from her golden phoenix throne while Cám kneels trembling below.",
                        "narrations": [],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Chị Tấm ơi... Chị làm thế nào\nmà trắng trẻo đẹp đẽ hơn xưa thế?!",
                                "x": 270,
                                "y": -100,
                                "rx": 250,
                                "ry": 72,
                                "tail": [360, -290],
                                "dark_mode": True,
                                "font_size": 21,
                            },
                            {
                                "text": "Em có muốn đẹp không,\nđể chị bảo quân hầu giúp em?",
                                "x": 480,
                                "y": 110,
                                "rx": 235,
                                "ry": 68,
                                "tail": [420, 290],
                                "dark_mode": False,
                                "font_size": 21,
                            },
                        ],
                        "gutter_text": "Lòng tham và sự đố kỵ mù quáng đã tự dẫn lối cho kẻ ác\nbước vào cái hố nhân quả do chính mình đào nên!",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Nhân Quả Nhãn Tiền",
                        "characters_present": ["cam", "di_ghe"],
                        "image_prompt": "Cám inside a deep stone pit shrouded in steam and karma flames while the Stepmother collapses in horror above.",
                        "narrations": [
                            {
                                "text": "[THIÊN ĐẠO LUÂN HỒI - ÁC GIẢ ÁC BÁO]\nKẻ năm xưa năm lần bảy lượt đoạt mạng người hiền,\nnay tự mình nhận lấy kết cục bi thảm!",
                                "x": 400,
                                "y": 95,
                                "w": 680,
                                "h": 98,
                                "border_color": [168, 85, 247, 240],
                                "text_color": [243, 232, 255, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "ẦMMM!!",
                                "x": 540,
                                "y": 640,
                                "font_size": 52,
                                "color": [216, 180, 254, 255],
                                "glow_color": [126, 34, 206, 255],
                                "angle": -10,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Không... Cám con tôi!!\nBáo ứng... tất cả là báo ứng rồi!!",
                                "x": 400,
                                "y": -95,
                                "rx": 260,
                                "ry": 72,
                                "tail": [410, -450],
                                "dark_mode": True,
                                "font_size": 21,
                            }
                        ],
                        "gutter_text": "Khép lại những tháng ngày bão giông và oán hận...\nÁnh mặt trời bình yên một lần nữa tỏa rạng khắp kinh kỳ!",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Đại Kết Cục: Long Phượng Hòa Minh",
                        "characters_present": ["tam", "hoang_tu"],
                        "image_prompt": "The young Dragon King and Empress Tấm standing together on high imperial balcony at golden sunrise with soaring Golden Dragon and Phoenix.",
                        "narrations": [
                            {
                                "text": "Từ đó, Hoàng Hậu Tấm cùng Quốc Vương trị vì đất nước muôn dân ấm no.\nỞ hiền gặp lành — chân lý ngàn đời vẫn mãi tỏa sáng!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [250, 204, 21, 245],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Bình minh lên rồi...\nGiang sơn này và trái tim trẫm mãi mãi thuộc về nàng!",
                                "x": 400,
                                "y": -95,
                                "rx": 285,
                                "ry": 72,
                                "tail": [410, -360],
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

    # Copy sang ARTIFACT_DIR để hiển thị trực tiếp trong Artifact cho người dùng
    for cid in char_files:
        shutil.copyfile(
            os.path.join(proj_dir, f"char_{cid}_sheet.jpg"),
            os.path.join(ARTIFACT_DIR, f"tc_char_{cid}_sheet.jpg"),
        )
    for ch_idx in [1, 2, 3]:
        for p_idx in range(1, 5):
            shutil.copyfile(
                os.path.join(proj_dir, f"ch{ch_idx}_panel_{p_idx}_typeset.jpg"),
                os.path.join(ARTIFACT_DIR, f"tc_ch{ch_idx}_p{p_idx}_typeset.jpg"),
            )

    print("Seeded FULL SERIES tam_cam:", res)


def seed_thanh_giong_full_series():
    proj_id = "thanh_giong"
    proj_dir = os.path.join(PROJECTS_DIR, proj_id)
    os.makedirs(proj_dir, exist_ok=True)

    # 1. Copy 4 ảnh gốc Hồ Sơ Nhân Vật (Character Reference Sheets)
    char_files = {
        "thanh_giong": "thanh_giong_manhwa_sheet_1792049335856.jpg",
        "giong_be": "giong_child_reference_sheet_1792049498098.jpg",
        "me_giong": "me_giong_character_sheet_1792049307824.jpg",
        "thach_linh": "thach_linh_tuong_quan_ref_sheet_png_1792049300131.jpg",
    }
    for cid, fname in char_files.items():
        src = os.path.join(ARTIFACT_DIR, fname)
        dst = os.path.join(proj_dir, f"char_{cid}_raw.jpg")
        if os.path.exists(src):
            shutil.copyfile(src, dst)

    # 2. Copy 12 ảnh gốc của 3 Chương (4 khung / chương)
    ch_panel_files = {
        1: [
            "chapter1_panel1_an_invasion_messenger_1792049299769.jpg",
            "giong_chapter1_panel2_1792049493682.jpg",
            "giong_chapter1_panel3_transformation_1792049301054.jpg",
            "chapter1_panel4_iron_horse_forge_1792049300037.jpg",
        ],
        2: [
            "thanh_giong_iron_horse_panel_1792049326389.jpg",
            "thanh_giong_ch2_panel2_1792049493243.jpg",
            "thanh_giong_ch2_panel3_clash_1792049328340.jpg",
            "thanh_giong_ch2_panel4_png_1792049328657.jpg",
        ],
        3: [
            "thanh_giong_ch3_panel1_victory_1792049332803.jpg",
            "thanh_giong_soc_son_armor_1792049330613.jpg",
            "thanh_giong_ascension_soc_son_1792049357782.jpg",
            "ch3_panel4_phu_dong_thien_vuong_shrine_1792049326838.jpg",
        ],
    }
    for ch_idx, p_list in ch_panel_files.items():
        for p_idx, fname in enumerate(p_list, start=1):
            src = os.path.join(ARTIFACT_DIR, fname)
            dst = os.path.join(proj_dir, f"ch{ch_idx}_panel_{p_idx}_raw.jpg")
            if os.path.exists(src):
                shutil.copyfile(src, dst)

    storyboard = {
        "title": "THÁNH GIÓNG: PHÙ ĐỔNG THIÊN VƯƠNG",
        "subtitle": "TRỌN BỘ HUYỀN SỬ ĐẠI VIỆT (3 CHƯƠNG HOÀN CHỈNH)",
        "credits": "Nguyên tác: Truyền thuyết Dân gian Việt Nam (Public Domain) • Sản xuất: Antigravity Agent (agy CLI)",
        "ai_pacing_note": "Đạo diễn AI (agy CLI) chia bộ truyện thành 3 Chương × 4 Khung hình: Chương 1 (Tiếng nói đầu đời & Thức tỉnh thần lực), Chương 2 (Ngựa sắt phun lửa & Đại chiến Tre Đằng Ngà), Chương 3 (Hóa Thánh về trời trên đỉnh Sóc Sơn).",
        "characters": [
            {
                "id": "thanh_giong",
                "name": "Thánh Gióng (Phù Đổng Thiên Vương)",
                "role": "Nam chính • Thiên Tướng Hộ Quốc Lạc Việt (Tứ Bất Tử)",
                "visual_dna": "20-year-old colossal godlike ancient Vietnamese heavenly warrior, sharp heroic jawline, piercing glowing golden eyes, flowing raven-black hair beneath a golden-bronze Lac Viet war crown, wearing ornate black-and-gold Dong Son dragon-scale battle armor with glowing molten-gold seams, holding a glowing golden-iron war rod (Roi Sắt).",
            },
            {
                "id": "giong_be",
                "name": "Cậu Bé Gióng (Làng Phù Đổng)",
                "role": "Hình thái Ấu Thơ • Thần Đồng Làng Gióng",
                "visual_dna": "Cute yet mysterious 3-year-old ancient Vietnamese divine child, big luminous golden-amber eyes filled with ancient celestial wisdom, black hair tuft, wearing simple rustic brown-and-cream Vietnamese village linen clothes, surrounded by a subtle golden lotus halo.",
            },
            {
                "id": "me_giong",
                "name": "Mẹ Gióng",
                "role": "Người Mẹ Hiền Làng Phù Đổng",
                "visual_dna": "Kind, gentle 40-year-old ancient Vietnamese village mother, warm loving eyes, black hair wrapped in a traditional Vietnamese headscarf (khăn mỏ quạ), wearing humble brown-and-beige traditional Áo Tứ Thân.",
            },
            {
                "id": "thach_linh",
                "name": "Thạch Linh Tướng Quân",
                "role": "Đại Phản Diện • Chúa Tể Đại Quân Giặc Ân",
                "visual_dna": "Towering, brutal warlord of the Ân Invaders with a scarred menacing face, glowing blood-red eyes, black horned iron-skull armor with a dark crimson fur cloak, wielding a massive serrated black iron halberd.",
            },
        ],
        "chapters": [
            {
                "chapter_index": 1,
                "chapter_title": "CHƯƠNG 1: TIẾNG NÓI ĐẦU ĐỜI & SỰ THỨC TỈNH CỦA THIÊN TƯỚNG",
                "footer_title": "— HẾT CHƯƠNG 1: ĐÓN ĐỌC CHƯƠNG 2 - CHIẾN MÃ PHUN LỬA —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Vó Ngựa Giặc Ân & Trống Lệnh Cầu Hiền",
                        "characters_present": ["thach_linh"],
                        "image_prompt": "Terrifying Ân invader army burning border villages above while a royal Vietnamese messenger rides a white horse beating a bronze drum below.",
                        "narrations": [
                            {
                                "text": "[ĐỜI HÙNG VƯƠNG THỨ SÁU]\nGiặc Ân hung bạo tràn qua biên ải như bão lửa.\nVua Hùng sai sứ giả đi khắp thiên hạ cầu người tài cứu nước!",
                                "x": 400,
                                "y": 95,
                                "w": 700,
                                "h": 98,
                                "border_color": [239, 68, 68, 240],
                                "text_color": [254, 226, 226, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "TÙNG! TÙNG!!",
                                "x": 540,
                                "y": 640,
                                "font_size": 48,
                                "color": [253, 224, 71, 255],
                                "glow_color": [220, 38, 38, 255],
                                "angle": -9,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Quân giặc Ân thế mạnh như chẻ tre!\nAi là bậc kỳ tài xin ra giúp nước cứu dân!!",
                                "x": 400,
                                "y": -95,
                                "rx": 285,
                                "ry": 72,
                                "tail": [410, -340],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Tại làng Phù Đổng, có cậu bé lên ba vẫn chưa biết nói cười, đặt đâu nằm đấy... Nhưng khi vừa nghe tiếng trống sứ giả, kim quang trên trời bỗng giáng xuống!",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Tiếng Nói Đầu Đời Của Thần Đồng",
                        "characters_present": ["giong_be", "me_giong"],
                        "image_prompt": "3-year-old Gióng standing radiantly in a pillar of golden celestial light pointing toward the kneeling Royal Messenger.",
                        "narrations": [
                            {
                                "text": "Đứa trẻ ba năm chưa từng cất tiếng, lời đầu tiên nói ra\nlại là lời thề gánh vác vận mệnh cả giang sơn!",
                                "x": 400,
                                "y": 90,
                                "w": 690,
                                "h": 92,
                                "border_color": [250, 204, 21, 240],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Ông về tâu với Đức Vua đúc cho ta một con ngựa sắt,\nmột cái roi sắt và một tấm áo giáp sắt để ta phá giặc này!",
                                "x": 400,
                                "y": -95,
                                "rx": 310,
                                "ry": 76,
                                "tail": [400, -450],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Từ sau hôm gặp sứ giả, Gióng lớn nhanh như thổi! Cơm ăn mấy cũng không no, áo vừa mặc xong đã căng đứt chỉ, cả làng Phù Đổng nô nức góp gạo nuôi trang dũng sĩ...",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Làng Phù Đổng Góp Gạo & Gióng Vươn Vai Hóa Khổng Lồ",
                        "characters_present": ["thanh_giong", "me_giong"],
                        "image_prompt": "Villagers bringing baskets of rice as Gióng transforms in a golden-crimson vortex into a colossal heavenly warrior.",
                        "narrations": [
                            {
                                "text": "Tình dân đất Việt hội tụ thành thần lực vô biên!\nCậu bé vươn vai một cái, hóa thành Thiên Tướng uy dũng cao hơn trượng!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [250, 204, 21, 240],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "BÙNG NỔ!!",
                                "x": 520,
                                "y": 540,
                                "font_size": 52,
                                "color": [253, 224, 71, 255],
                                "glow_color": [234, 88, 12, 255],
                                "angle": -8,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Ơn nghĩa mẹ cha và bà con làng Phù Đổng,\nta nguyện lấy máu giặc Ân để báo đền!",
                                "x": 400,
                                "y": -95,
                                "rx": 280,
                                "ry": 72,
                                "tail": [400, -450],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Cùng lúc đó tại kinh thành Phong Châu, hàng ngàn thợ rèn giỏi nhất ngày đêm đỏ lửa đúc nên thần binh truyền thuyết...",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Đại Lò Rèn Đúc Chiến Mã Sắt & Giáp Kim Long",
                        "characters_present": ["thanh_giong"],
                        "image_prompt": "Colossal Iron Warhorse with fiery eyes, black-and-gold Dong Son dragon battle armor, and glowing iron war rod in royal forge.",
                        "narrations": [
                            {
                                "text": "Ngựa Sắt ngậm hỏa châu, Giáp Sắt khắc giao long, Roi Sắt nặng ngàn cân —\nThần binh xuất thế chờ đón chủ nhân!",
                                "x": 400,
                                "y": 95,
                                "w": 700,
                                "h": 95,
                                "border_color": [249, 115, 22, 240],
                                "text_color": [255, 237, 213, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "RỰC LỬA!!",
                                "x": 530,
                                "y": 620,
                                "font_size": 48,
                                "color": [253, 186, 116, 255],
                                "glow_color": [220, 38, 38, 255],
                                "angle": -9,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Chiến mã sắt đã rèn xong!\nMau rước tráng sĩ làng Phù Đổng xuất chinh!",
                                "x": 400,
                                "y": -95,
                                "rx": 275,
                                "ry": 72,
                                "tail": [350, -320],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "",
                    },
                ],
            },
            {
                "chapter_index": 2,
                "chapter_title": "CHƯƠNG 2: CHIẾN MÃ PHUN LỬA & ĐẠI CHIẾN TRE ĐẰNG NGÀ",
                "footer_title": "— HẾT CHƯƠNG 2: ĐÓN ĐỌC CHƯƠNG 3 - HÓA THÁNH VỀ TRỜI —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Ngựa Sắt Hí Vang Phun Đại Hỏa Diễm",
                        "characters_present": ["thanh_giong"],
                        "image_prompt": "Thánh Gióng in black-and-gold Dong Son armor mounting the rearing Iron Warhorse as it breathes golden-crimson dragon fire.",
                        "narrations": [
                            {
                                "text": "Khoảnh khắc Thánh Gióng vỗ nhẹ lên lưng Ngựa Sắt,\nchiến mã bỗng hóa sinh linh, hí vang một tiếng phun lửa rực trời!",
                                "x": 400,
                                "y": 95,
                                "w": 700,
                                "h": 95,
                                "border_color": [250, 204, 21, 240],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "HÍÍÍ—ẦMMM!!",
                                "x": 520,
                                "y": 540,
                                "font_size": 52,
                                "color": [253, 224, 71, 255],
                                "glow_color": [220, 38, 38, 255],
                                "angle": -10,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Tiến lên, Chiến Mã Sắt!\nHôm nay ta và ngươi quét sạch bóng quân thù khỏi bờ cõi!",
                                "x": 400,
                                "y": -95,
                                "rx": 295,
                                "ry": 72,
                                "tail": [400, -450],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Ngựa sắt lao đi nhanh như lốc cuốn! Đón đầu đại quân giặc Ân dưới chân núi Trâu, Gióng vung Roi Sắt giáng đòn sấm sét...",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Một Roi Quét Sạch Vạn Quân Thù",
                        "characters_present": ["thanh_giong", "thach_linh"],
                        "image_prompt": "Thánh Gióng riding his fire-breathing Iron Warhorse sweeping his glowing molten-iron rod through the Ân invader army.",
                        "narrations": [
                            {
                                "text": "Ngựa phun lửa thiêu rụi chiến xa, Roi Sắt quét tới đâu\nđội hình tiên phong của giặc Ân tan tác tới đó!",
                                "x": 400,
                                "y": 90,
                                "w": 680,
                                "h": 92,
                                "border_color": [249, 115, 22, 240],
                                "text_color": [255, 237, 213, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "ĐOÀNG!!",
                                "x": 540,
                                "y": 600,
                                "font_size": 54,
                                "color": [253, 224, 71, 255],
                                "glow_color": [220, 38, 38, 255],
                                "angle": -8,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Kẻ nào dám phạm bờ cõi Văn Lang,\nhãy nhận lấy cơn thịnh nộ này!!",
                                "x": 400,
                                "y": -95,
                                "rx": 275,
                                "ry": 72,
                                "tail": [410, -420],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Giữa biển lửa loạn quân, Thạch Linh Tướng Quân — chúa tể giặc Ân vung đại đao hắc thiết lao ra tử chiến trực diện với Thánh Gióng!",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Tử Chiến Chủ Tướng Giặc Ân & Roi Sắt Gãy Đôi",
                        "characters_present": ["thanh_giong", "thach_linh"],
                        "image_prompt": "Extreme close-up clash between Thánh Gióng and the horned Ân General shattering both the iron rod and black halberd.",
                        "narrations": [
                            {
                                "text": "Đòn va chạm kinh thiên động địa giữa hai luồng thần lực\nkhiến cả đại đao giặc Ân lẫn cây Roi Sắt đều nổ tung thành vạn mảnh!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [239, 68, 68, 240],
                                "text_color": [254, 226, 226, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "CHOANG! RẮC!!",
                                "x": 480,
                                "y": 540,
                                "font_size": 50,
                                "color": [254, 202, 202, 255],
                                "glow_color": [220, 38, 38, 255],
                                "angle": -9,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Roi sắt của ngươi gãy rồi!\nXem ngươi lấy gì cản đại quân của ta?!",
                                "x": 400,
                                "y": -95,
                                "rx": 270,
                                "ry": 72,
                                "tail": [520, -450],
                                "dark_mode": True,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Không chút nao núng, Thánh Gióng xoay người vươn đôi tay thần lực nhổ phăng cả rặng tre ngà ngàn năm bên sườn núi!",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Nhổ Cụm Tre Đằng Ngà Quật Tan Tướng Giặc",
                        "characters_present": ["thanh_giong", "thach_linh"],
                        "image_prompt": "Colossal Thánh Gióng uprooting entire clusters of glowing golden bamboo trees to crush the terrified Ân General and his army.",
                        "narrations": [
                            {
                                "text": "Cỏ cây non nước Đại Việt đều hóa thành thần binh!\nCụm tre ngà thấm hỏa khí của Ngựa Sắt bừng sáng sắc vàng kim bất diệt!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [250, 204, 21, 245],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "ẦM ĐOÀNG!!",
                                "x": 520,
                                "y": 580,
                                "font_size": 52,
                                "color": [253, 224, 71, 255],
                                "glow_color": [234, 179, 8, 255],
                                "angle": -10,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Từng tấc đất, từng nhành tre nơi đây\nđều là vũ khí chôn vùi lũ xâm lăng!!",
                                "x": 400,
                                "y": -95,
                                "rx": 280,
                                "ry": 72,
                                "tail": [400, -450],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "",
                    },
                ],
            },
            {
                "chapter_index": 3,
                "chapter_title": "CHƯƠNG 3: TRE ĐẰNG NGÀ HÓA VÀNG & PHÙ ĐỔNG THIÊN VƯƠNG VỀ TRỜI",
                "footer_title": "— ĐẠI KẾT CỤC: HẾT TRỌN BỘ THÁNH GIÓNG —",
                "panels": [
                    {
                        "panel_index": 1,
                        "scene_title": "Bình Minh Khải Hoàn & Rặng Tre Đằng Ngà Vàng Óng",
                        "characters_present": ["thanh_giong"],
                        "image_prompt": "Thánh Gióng standing victorious on his Iron Warhorse at golden sunrise surrounded by glowing golden bamboo while invaders flee.",
                        "narrations": [
                            {
                                "text": "Chủ tướng giặc Ân tử trận, tàn quân khiếp đảm vứt giáp xin hàng.\nBờ cõi Văn Lang sạch bóng quân thù dưới ánh bình minh rực rỡ!",
                                "x": 400,
                                "y": 95,
                                "w": 700,
                                "h": 95,
                                "border_color": [250, 204, 21, 240],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Sứ mệnh hộ quốc đã hoàn tất...\nNon sông này từ nay trở lại thái bình!",
                                "x": 400,
                                "y": -95,
                                "rx": 270,
                                "ry": 70,
                                "tail": [400, -450],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Không màng danh lợi hay tước lộc triều đình, người anh hùng một mình một ngựa phi thẳng lên đỉnh núi Sóc Sơn mây phủ...",
                    },
                    {
                        "panel_index": 2,
                        "scene_title": "Cởi Giáp Sắt Lưu Lại Đỉnh Sóc Sơn",
                        "characters_present": ["thanh_giong"],
                        "image_prompt": "Thánh Gióng on misty summit of Mount Sóc Sơn placing his black-and-gold iron battle armor on a stone altar and smiling back at his homeland.",
                        "narrations": [
                            {
                                "text": "Trên đỉnh Sóc Sơn lộng gió, Thánh Gióng cởi bỏ bộ giáp sắt Kim Long\nđể lại nhân gian, ngoái nhìn quê hương và mẹ già lần cuối...",
                                "x": 400,
                                "y": 95,
                                "w": 700,
                                "h": 95,
                                "border_color": [103, 232, 249, 235],
                                "text_color": [224, 242, 254, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Xin tạ từ mẹ hiền và bách tính Văn Lang...\nKhi nào non nước cần, ta sẽ còn hiển linh!",
                                "x": 400,
                                "y": -95,
                                "rx": 285,
                                "ry": 72,
                                "tail": [400, -480],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Dứt lời, Ngựa Sắt hí vang một tiếng chấn động tầng mây, tung vó lửa bay thẳng vào vòm trời rực sáng!",
                    },
                    {
                        "panel_index": 3,
                        "scene_title": "Ngựa Sắt Đạp Mây Bay Về Cõi Trời",
                        "characters_present": ["thanh_giong", "me_giong"],
                        "image_prompt": "Thánh Gióng riding his glowing Iron Warhorse straight up into parted golden heavenly clouds while King Hùng and villagers bow below.",
                        "narrations": [
                            {
                                "text": "Giữa muôn đạo hào quang sen vàng, cả người lẫn ngựa hóa kim quang\nbay thẳng về trời trước sự thành kính bái vọng của muôn dân!",
                                "x": 400,
                                "y": 95,
                                "w": 710,
                                "h": 95,
                                "border_color": [250, 204, 21, 245],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [
                            {
                                "text": "VÚTTT!!",
                                "x": 540,
                                "y": 480,
                                "font_size": 50,
                                "color": [253, 224, 71, 255],
                                "glow_color": [245, 158, 11, 255],
                                "angle": -10,
                            }
                        ],
                        "bubbles": [
                            {
                                "text": "Bái tạ Đức Phù Đổng Thiên Vương!!\nThần uy của Ngài mãi mãi trường tồn cùng dân tộc!",
                                "x": 400,
                                "y": -95,
                                "rx": 290,
                                "ry": 72,
                                "tail": [400, -280],
                                "dark_mode": False,
                                "font_size": 20,
                            }
                        ],
                        "gutter_text": "Từ đó về sau, những rặng tre bị lửa ngựa sắt hun đốt hóa thành Tre Đằng Ngà vàng óng, còn vết chân ngựa hóa thành những hồ nước trong xanh nối tiếp nhau...",
                    },
                    {
                        "panel_index": 4,
                        "scene_title": "Đại Kết Cục: Huyền Thoại Phù Đổng Thiên Vương Bất Diệt",
                        "characters_present": ["thanh_giong"],
                        "image_prompt": "Grand ancient Vietnamese temple Đền Gióng nestled among golden bamboo groves and circular footprint lakes under eternal golden sunlight.",
                        "narrations": [
                            {
                                "text": "Vua Hùng nhớ công ơn, phong Ngài là Phù Đổng Thiên Vương,\nlập đền thờ tại quê hương — một trong Tứ Bất Tử hộ trì non sông Việt Nam!",
                                "x": 400,
                                "y": 95,
                                "w": 720,
                                "h": 98,
                                "border_color": [250, 204, 21, 245],
                                "text_color": [254, 249, 195, 255],
                                "font_size": 20,
                            }
                        ],
                        "sfx": [],
                        "bubbles": [
                            {
                                "text": "Hào khí Phù Đổng ngàn năm bất diệt,\nđời đời kiếp kiếp che chở con Lạc cháu Hồng!",
                                "x": 400,
                                "y": -95,
                                "rx": 285,
                                "ry": 72,
                                "tail": [400, -520],
                                "dark_mode": False,
                                "font_size": 20,
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
    print("Seeded FULL SERIES thanh_giong:", res)


if __name__ == "__main__":
    seed_tam_cam_full_series()
    seed_thanh_giong_full_series()

