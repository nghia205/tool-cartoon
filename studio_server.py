#!/usr/bin/env python3
"""
AI Webtoon Studio Server (Web UI + REST API)
--------------------------------------------
Chạy lệnh: python3 studio_server.py
Mở trình duyệt: http://localhost:8080
"""
import os
import json
import mimetypes
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from studio_engine import (
    BASE_DIR,
    PROJECTS_DIR,
    render_project,
    create_full_webtoon_from_prompt,
)

ENV_FILE = os.path.join(BASE_DIR, ".env")


def load_env_keys() -> dict:
    keys = {"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    keys[k.strip()] = v.strip().strip('"').strip("'")
    for k in keys:
        if os.environ.get(k):
            keys[k] = os.environ[k]
    return keys


def save_env_key(provider: str, api_key: str):
    if not api_key:
        return
    keys = load_env_keys()
    if provider == "gemini":
        keys["GEMINI_API_KEY"] = api_key
    elif provider == "openai":
        keys["OPENAI_API_KEY"] = api_key
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        for k, v in keys.items():
            f.write(f'{k}="{v}"\n')


def get_project_details(project_id: str) -> dict:
    proj_dir = os.path.join(PROJECTS_DIR, project_id)
    sb_path = os.path.join(proj_dir, "storyboard.json")
    if not os.path.exists(sb_path):
        return None
    with open(sb_path, "r", encoding="utf-8") as f:
        sb = json.load(f)
    panel_count = len(sb.get("panels", []))
    ts = int(os.path.getmtime(sb_path))
    panels_info = []
    for i in range(1, panel_count + 1):
        panels_info.append(
            {
                "index": i,
                "raw_url": f"/projects/{project_id}/panel_{i}_raw.jpg?t={ts}",
                "typeset_url": f"/projects/{project_id}/panel_{i}_typeset.jpg?t={ts}",
            }
        )
    return {
        "project_id": project_id,
        "title": sb.get("title", project_id),
        "subtitle": sb.get("subtitle", ""),
        "panel_count": panel_count,
        "storyboard": sb,
        "panels": panels_info,
        "strip_url": f"/projects/{project_id}/webtoon_full_strip.jpg?t={ts}",
        "zip_url": f"/projects/{project_id}/{project_id}_webtoon.zip",
    }


class StudioHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def _send_json(self, data: dict, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/studio":
            self.path = "/studio.html"
            return super().do_GET()

        if path == "/api/config":
            keys = load_env_keys()
            return self._send_json(
                {
                    "has_gemini_key": bool(keys.get("GEMINI_API_KEY")),
                    "has_openai_key": bool(keys.get("OPENAI_API_KEY")),
                }
            )

        if path == "/api/projects":
            items = []
            if os.path.exists(PROJECTS_DIR):
                for name in sorted(os.listdir(PROJECTS_DIR)):
                    info = get_project_details(name)
                    if info:
                        items.append(
                            {
                                "project_id": info["project_id"],
                                "title": info["title"],
                                "subtitle": info["subtitle"],
                                "panel_count": info["panel_count"],
                                "strip_url": info["strip_url"],
                                "zip_url": info["zip_url"],
                            }
                        )
            return self._send_json({"projects": items})

        if path.startswith("/api/projects/"):
            proj_id = path.split("/api/projects/", 1)[1].strip("/")
            info = get_project_details(proj_id)
            if not info:
                return self._send_json({"error": "Không tìm thấy bộ truyện"}, 404)
            return self._send_json(info)

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if path == "/api/generate":
            try:
                prompt = body.get("prompt", "").strip()
                if not prompt:
                    return self._send_json({"error": "Vui lòng nhập yêu cầu tạo truyện!"}, 400)
                num_panels = int(body.get("num_panels", 5))
                provider = body.get("provider", "gemini")
                api_key = body.get("api_key", "").strip()

                if api_key and body.get("save_key", True):
                    save_env_key(provider, api_key)
                elif not api_key:
                    env_keys = load_env_keys()
                    api_key = (
                        env_keys.get("GEMINI_API_KEY")
                        if provider == "gemini"
                        else env_keys.get("OPENAI_API_KEY")
                    )

                res = create_full_webtoon_from_prompt(
                    prompt=prompt,
                    num_panels=num_panels,
                    provider=provider,
                    api_key=api_key,
                )
                details = get_project_details(res["project_id"])
                return self._send_json({"status": "ok", "project": details})
            except Exception as e:
                return self._send_json({"error": f"Lỗi khi tạo Webtoon: {str(e)}"}, 500)

        if path == "/api/render":
            try:
                proj_id = body.get("project_id", "").strip()
                storyboard = body.get("storyboard")
                if not proj_id or not storyboard:
                    return self._send_json({"error": "Thiếu project_id hoặc storyboard"}, 400)
                proj_dir = os.path.join(PROJECTS_DIR, proj_id)
                sb_path = os.path.join(proj_dir, "storyboard.json")
                with open(sb_path, "w", encoding="utf-8") as f:
                    json.dump(storyboard, f, ensure_ascii=False, indent=2)
                render_project(proj_id)
                details = get_project_details(proj_id)
                return self._send_json({"status": "ok", "project": details})
            except Exception as e:
                return self._send_json({"error": f"Lỗi khi render lại Typeset: {str(e)}"}, 500)

        return self._send_json({"error": "Endpoint không hợp lệ"}, 404)


def run_server(port=8080):
    server = ThreadingHTTPServer(("0.0.0.0", port), StudioHandler)
    print(f"============================================================")
    print(f"🚀 AI WEBTOON STUDIO ĐANG CHẠY TẠI: http://localhost:{port}")
    print(f"📂 Thư mục dự án: {PROJECTS_DIR}")
    print(f"============================================================")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
