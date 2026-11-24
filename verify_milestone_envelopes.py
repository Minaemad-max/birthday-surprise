# -*- coding: utf-8 -*-
"""
Verification script for both milestone envelopes:
1. May 25 Outing Envelope (فرح مارتين وأول خروجة)
2. May 27 Engagement Envelope (يوم خطوبتنا)
"""
import os
import sys
import json
import time
import base64
import shutil
import asyncio
import http.server
import socketserver
import threading
import subprocess

PORT = 8970
BASE_DIR = r"c:\Users\Mina\Desktop\Birthday"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
BRAIN_DIR = r"C:\Users\Mina\.gemini\antigravity\brain\d7f9e886-c55e-40f8-a561-3b8525483138"
BRAIN_SCREENSHOTS_DIR = os.path.join(BRAIN_DIR, "screenshots")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)
os.makedirs(BRAIN_SCREENSHOTS_DIR, exist_ok=True)

class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

async def run_verification():
    import aiohttp

    print("==================================================")
    print("بدء التحقق من ظرفي ٢٥ مايو (أول خروجة) و٢٧ مايو (الخطوبة)")
    print("==================================================")

    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SilentHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9277",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    base_url = f"http://127.0.0.1:{PORT}/index.html"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:9277/json") as resp:
                tabs = await resp.json()
                ws_url = tabs[0]["webSocketDebuggerUrl"]

            async with session.ws_connect(ws_url) as ws:
                async def send_cmd(method, params=None):
                    cmd_id = int(time.time() * 1000) % 1000000
                    payload = {"id": cmd_id, "method": method}
                    if params:
                        payload["params"] = params
                    await ws.send_json(payload)
                    while True:
                        msg = await ws.receive_json()
                        if msg.get("id") == cmd_id:
                            return msg.get("result", {})

                async def eval_js(expr):
                    res = await send_cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
                    return res.get("result", {}).get("value")

                async def capture_screen(filename):
                    res = await send_cmd("Page.captureScreenshot", {"format": "png"})
                    img_data = base64.b64decode(res["data"])
                    out_path = os.path.join(SCREENSHOTS_DIR, filename)
                    with open(out_path, "wb") as f:
                        f.write(img_data)
                    shutil.copy2(out_path, os.path.join(BRAIN_SCREENSHOTS_DIR, filename))
                    shutil.copy2(out_path, os.path.join(BRAIN_DIR, filename))
                    print(f"  [SAVED] {filename}")
                    return out_path

                # Mobile viewport (iPhone 390x844)
                await send_cmd("Emulation.setDeviceMetricsOverride", {
                    "width": 390,
                    "height": 844,
                    "deviceScaleFactor": 2,
                    "mobile": True
                })

                # -------------------------------------------------------------
                # 1. التوقيت الفعلي الحالي (قبل منتصف ليل ٢٥ نوفمبر): كلاهما مقفول
                # -------------------------------------------------------------
                print("\n1. فحص التوقيت الحالي في وضع الزاهرة (كلا الظرفين مقفولان)...")
                await send_cmd("Page.navigate", {"url": base_url})
                for _ in range(25):
                    ready = await eval_js("document.readyState")
                    if ready == "complete":
                        break
                    await asyncio.sleep(0.15)
                await asyncio.sleep(0.8)

                # فحص ظرف أول خروجة
                await eval_js("document.getElementById('outingEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'});")
                await asyncio.sleep(0.3)
                outing_locked_text = await eval_js("document.getElementById('outingLockedText').textContent.trim()")
                outing_btn_hidden = await eval_js("document.getElementById('openOutingBtn').classList.contains('hidden')")
                assert "يتفتح يوم ٢٥ مايو" in outing_locked_text, f"Outing locked text mismatch: {outing_locked_text}"
                assert outing_btn_hidden, "Outing button should be hidden when locked"
                print(f"  [PASS] ظرف أول خروجة مقفول: «{outing_locked_text}»")

                await capture_screen("mobile-outing-locked-may25.png")

                # فحص ظرف الخطوبة
                await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'});")
                await asyncio.sleep(0.3)
                eng_locked_text = await eval_js("document.getElementById('engagementLockedText').textContent.trim()")
                eng_btn_hidden = await eval_js("document.getElementById('openEngagementBtn').classList.contains('hidden')")
                assert "يتفتح يوم ٢٧ مايو" in eng_locked_text, f"Engagement locked text mismatch: {eng_locked_text}"
                assert eng_btn_hidden, "Engagement button should be hidden when locked"
                print(f"  [PASS] ظرف الخطوبة مقفول: «{eng_locked_text}»")

                await capture_screen("mobile-engagement-locked-may27.png")

                # -------------------------------------------------------------
                # 2. فتح ظرف أول خروجة (فرح مارتين)
                # -------------------------------------------------------------
                print("\n2. فحص فتح ظرف أول خروجة (فرح مارتين)...")
                await send_cmd("Page.navigate", {"url": f"{base_url}?test=open_outing"})
                await asyncio.sleep(1.0)

                modal_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
                outing_header = await eval_js("document.getElementById('albumModalHeaderTag').textContent.trim()")
                outing_dedication = await eval_js("document.getElementById('letterDedicationQuote').textContent.trim()")
                outing_badge = await eval_js("document.getElementById('albumDateBadgeText').textContent.trim()")
                outing_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
                outing_img = await eval_js("document.getElementById('albumCurrentImg').src")

                assert modal_open, "Modal must be open"
                assert "أول خروجة" in outing_header or "٢٥ مايو" in outing_header, f"Outing header mismatch: {outing_header}"
                assert "فرح مارتين" in outing_dedication, f"Outing dedication mismatch: {outing_dedication}"
                assert "أمسك إيدك" in outing_dedication, "Dedication must mention holding hands"
                assert "٢٥ مايو" in outing_badge, f"Badge mismatch: {outing_badge}"
                assert "may25-outing.jpg" in outing_img or "outing-photo-1.jpg" in outing_img, f"Wrong image: {outing_img}"

                print(f"  [PASS] ترويسة الجواب: «{outing_header}»")
                print(f"  [PASS] إهداء الجواب: «{outing_dedication}»")
                print(f"  [PASS] شارة وتاريخ الصورة: «{outing_badge}»")
                print(f"  [PASS] تعليق الصورة: «{outing_cap}»")

                await capture_screen("mobile-outing-opened-may25.png")

                # -------------------------------------------------------------
                # 3. محاكاة بعد ٢٥ مايو وقبل ٢٧ مايو: ظرف ٢٥ متاح، وظرف ٢٧ مقفول
                # -------------------------------------------------------------
                print("\n3. فحص بعد ٢٥ مايو (ظرف ٢٥ متاح، وظرف ٢٧ مقفول)...")
                await send_cmd("Page.navigate", {"url": f"{base_url}?test=after_may25"})
                await asyncio.sleep(1.0)

                outing_btn_visible = await eval_js("!document.getElementById('openOutingBtn').classList.contains('hidden')")
                eng_locked = await eval_js("!document.getElementById('engagementLockedBadge').classList.contains('hidden')")
                assert outing_btn_visible, "Outing open button must be visible after May 25"
                assert eng_locked, "Engagement envelope must remain locked until May 27"
                print("  [PASS] زر ظرف ٢٥ متاح للفتح، وظرف ٢٧ لا يزال مقفولاً بنجاح.")

                # -------------------------------------------------------------
                # 4. فتح ظرف الخطوبة (٢٧ مايو)
                # -------------------------------------------------------------
                print("\n4. فحص فتح ظرف الخطوبة (٢٧ مايو)...")
                await send_cmd("Page.navigate", {"url": f"{base_url}?test=open_engagement"})
                await asyncio.sleep(1.0)

                eng_header = await eval_js("document.getElementById('albumModalHeaderTag').textContent.trim()")
                eng_dedication = await eval_js("document.getElementById('letterDedicationQuote').textContent.trim()")
                eng_badge = await eval_js("document.getElementById('albumDateBadgeText').textContent.trim()")
                eng_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
                eng_img = await eval_js("document.getElementById('albumCurrentImg').src")

                assert "ظرف يوم خطوبتنا" in eng_header, f"Engagement header mismatch: {eng_header}"
                assert "٢٧ مايو" in eng_dedication, f"Engagement dedication mismatch: {eng_dedication}"
                assert "٢٧ مايو" in eng_badge, f"Badge mismatch: {eng_badge}"
                assert "engagement-photo-1.jpg" in eng_img, f"Wrong engagement image: {eng_img}"

                print(f"  [PASS] ترويسة جواب الخطوبة: «{eng_header}»")
                print(f"  [PASS] إهداء الخطوبة: «{eng_dedication}»")
                print(f"  [PASS] شارة صورة الخطوبة: «{eng_badge}»")
                print(f"  [PASS] تعليق صورة الخطوبة: «{eng_cap}»")

                await capture_screen("mobile-engagement-opened-may27.png")

                print("\n==================================================")
                print("✅ جميع الفحوصات واللقطات اكتملت بنجاح 100%!")
                print("==================================================")
    finally:
        chrome_proc.terminate()
        try:
            httpd.shutdown()
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(run_verification())
