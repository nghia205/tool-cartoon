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


if __name__ == "__main__":
    seed_tam_cam_full_series()
