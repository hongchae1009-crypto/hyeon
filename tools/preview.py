"""SVG 조각들을 한 페이지로 묶어 PNG로 렌더링 (눈으로 확인용)."""
import sys, pathlib
from playwright.sync_api import sync_playwright

def shot(svgs, out, width=820):
    html = "<html><body style='margin:0;background:#eee'>" + "".join(
        f"<div style='margin:6px;background:#fff'>{s}</div>" for s in svgs) + "</body></html>"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page(viewport={"width": width, "height": 400}, device_scale_factor=1.3)
        pg.set_content(html)
        pg.screenshot(path=out, full_page=True)
        b.close()
