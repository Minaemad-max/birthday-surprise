# -*- coding: utf-8 -*-
"""
Verification and Mobile Screenshot Capture for May Update:
- '٢٣ مايو'
- '٢٥ مايو'
- 'بتوقيت رفووووووووووق'
- Locked & Unlocked states verification
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
from PIL import Image

PORT = 8960
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
    print("بدء الفحص والتقاط لقطات الموبايل لتعديلات مايو وتوقيت رفووووووووووق")
    print("==================================================")

    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SilentHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9255",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    base_url = f"http://127.0.0.1:{PORT}/index.html"

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9255/json") as resp:
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

            # ضبط المقاس على هاتف آيفون حديث (390 x 844)
            await send_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 390,
                "height": 844,
                "deviceScaleFactor": 2,
                "mobile": True
            })

            # -------------------------------------------------------------
            # فحص 1: الحالة الفعلية قبل الموعد (Locked State)
            # -------------------------------------------------------------
            print("\n1. فحص الحالة المقفولة (التوقيت الحالي في وضع الزائرة)...")
            await send_cmd("Page.navigate", {"url": f"{base_url}"})
            for _ in range(20):
                ready = await eval_js("document.readyState")
                if ready == "complete":
                    break
                await asyncio.sleep(0.2)
            await asyncio.sleep(0.8)

            # التحقق من شارة التاريخ على الهيرو
            hero_badge = await eval_js("document.getElementById('photoDateBadge').querySelector('.badge-text').textContent.trim()")
            assert "٢٣ مايو" in hero_badge, f"Hero badge mismatch: {hero_badge}"
            print(f"  [PASS] شارة صورة الاستقبال: «{hero_badge}»")

            # التحقق من سطر التوقيت تحت العدّاد
            tz_badge_text = await eval_js("document.querySelector('.cairo-tz-badge').textContent.trim()")
            tz_badge_title = await eval_js("document.querySelector('.cairo-tz-badge').getAttribute('title')")
            assert "بتوقيت رفووووووووووق" in tz_badge_text, f"Timezone text mismatch: {tz_badge_text}"
            assert "بتوقيت رفووووووووووق" in tz_badge_title, f"Timezone title mismatch: {tz_badge_title}"
            print(f"  [PASS] سطر التوقيت تحت العدّاد: «{tz_badge_text}»")

            # التقاط لقطة الهيرو والعدّاد
            await capture_screen("mobile-hero-countdown-may.png")

            # التمرير إلى ظرف الخطوبة المقفول
            await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'});")
            await asyncio.sleep(0.5)

            locked_badge_visible = await eval_js("!document.getElementById('engagementLockedBadge').classList.contains('hidden')")
            locked_text = await eval_js("document.getElementById('engagementLockedText').textContent.trim()")
            desc_text = await eval_js("document.getElementById('engagementStatusDesc').textContent.trim()")
            open_btn_hidden = await eval_js("document.getElementById('openEngagementBtn').classList.contains('hidden')")
            dev_panel = await eval_js("document.getElementById('devTestPanel')")

            assert locked_badge_visible, "Locked badge must be visible before unlock date"
            assert "يتفتح يوم ٢٥ مايو" in locked_text, f"Locked text mismatch: {locked_text}"
            assert "٢٥ مايو" in desc_text, f"Description text mismatch: {desc_text}"
            assert open_btn_hidden, "Open button must be hidden when locked"
            assert dev_panel is None, "Dev panel must not exist in visitor mode"

            print(f"  [PASS] شارة قفل ظرف الخطوبة: «{locked_text}»")
            print(f"  [PASS] وصف ظرف الخطوبة: «{desc_text}»")
            print("  [PASS] زر الفتح مخفي، ولوحة المطور محذوفة تماماً.")

            # التقاط لقطة ظرف الخطوبة المقفول
            await capture_screen("mobile-engagement-locked-may25.png")

            # -------------------------------------------------------------
            # فحص 2: الحالة المفتوحة لظرف الخطوبة (Unlocked State)
            # -------------------------------------------------------------
            print("\n2. فحص حالة فتح ظرف الخطوبة (بعد موعد الفتح)...")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=open_engagement"})
            await asyncio.sleep(1.2)

            modal_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            header_tag = await eval_js("document.getElementById('albumModalHeaderTag').textContent.trim()")
            dedication = await eval_js("document.getElementById('letterDedicationQuote').textContent.trim()")
            date_badge = await eval_js("document.getElementById('albumDateBadgeText').textContent.trim()")
            caption = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            signature = await eval_js("document.getElementById('albumSignatureText').textContent.trim()")

            assert modal_open, "Modal must be open in open_engagement test"
            assert "ظرف يوم خطوبتنا" in header_tag, f"Header tag mismatch: {header_tag}"
            assert "يوم ٢٥ مايو مش مجرد تاريخ" in dedication, f"Dedication mismatch: {dedication}"
            assert "٢٥ مايو" in date_badge, f"Photo badge mismatch: {date_badge}"
            assert "يوم خطوبتنا… اليوم اللي بدأنا فيه حكايتنا رسمي" in caption, f"Caption mismatch: {caption}"
            assert "بحبك 🌹" in signature, f"Signature mismatch: {signature}"

            print(f"  [PASS] عنوان الظرف في المودال: «{header_tag}»")
            print(f"  [PASS] إهداء الجواب: «{dedication}»")
            print(f"  [PASS] شارة صورة الخطوبة: «{date_badge}»")
            print(f"  [PASS] تعليق الصورة: «{caption}»")
            print(f"  [PASS] التوقيع: «{signature}»")

            # التقاط لقطة الجواب المفتوح مع صورة الخطوبة
            await capture_screen("mobile-engagement-unlocked-may25.png")

            # التمرير لأسفل لالتقاط التوقيع
            await eval_js("document.getElementById('loveLetterCard').scrollTo({top: 450, behavior: 'instant'});")
            await asyncio.sleep(0.4)
            await capture_screen("mobile-engagement-unlocked-signature-may25.png")

            # فحص زر الفتح عندما يكون الظرف متاحاً
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=after_nov25"})
            await asyncio.sleep(1.0)
            await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'});")
            await asyncio.sleep(0.4)
            open_btn_visible = await eval_js("!document.getElementById('openEngagementBtn').classList.contains('hidden')")
            open_btn_text = await eval_js("document.getElementById('openEngagementBtn').textContent.trim()")
            assert open_btn_visible, "Open button must be visible after unlock date"
            assert "افتحي ظرف الخطوبة" in open_btn_text, f"Unexpected button text: {open_btn_text}"
            print(f"  [PASS] زر الفتح المتاح: «{open_btn_text}»")
            await capture_screen("mobile-engagement-button-available-may25.png")

            # -------------------------------------------------------------
            # فحص 3: فحص ظرف ٢٣ مايو وألبوم الصور
            # -------------------------------------------------------------
            print("\n3. فحص ظرف ٢٣ مايو وألبوم الصور...")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=open_nov23"})
            await asyncio.sleep(1.0)

            nov23_header = await eval_js("document.getElementById('albumModalHeaderTag').textContent.trim()")
            nov23_dedication = await eval_js("document.getElementById('letterDedicationQuote').textContent.trim()")
            nov23_closing = await eval_js("document.getElementById('albumClosingMsg').textContent.trim()")
            nov23_badge = await eval_js("document.getElementById('albumDateBadgeText').textContent.trim()")

            assert "ظرف ٢٣ مايو" in nov23_header, f"Nov23 header mismatch: {nov23_header}"
            assert "يوم ٢٣ مايو هييجي في بالي" in nov23_dedication, f"Nov23 dedication mismatch: {nov23_dedication}"
            assert "يوم ٢٣ مايو كان حلو أوي" in nov23_closing, f"Nov23 closing mismatch: {nov23_closing}"
            assert "٢٣ مايو" in nov23_badge, f"Nov23 photo badge mismatch: {nov23_badge}"

            print(f"  [PASS] رأس مودال ظرف ٢٣ مايو: «{nov23_header}»")
            print(f"  [PASS] إهداء ظرف ٢٣ مايو: «{nov23_dedication}»")
            print(f"  [PASS] خاتمة ظرف ٢٣ مايو: «{nov23_closing}»")
            print(f"  [PASS] شارة صورة ألبوم ٢٣ مايو: «{nov23_badge}»")
            await capture_screen("mobile-may23-album-modal.png")

            # فحص المواعيد البرمجية
            print("\n4. فحص المواعيد البرمجية الداخلية...")
            eng_date = await eval_js("BIRTHDAY_CONFIG.engagementDateCairo")
            bday_date = await eval_js("BIRTHDAY_CONFIG.targetDateCairo")
            print(f"  [INFO] موعد فك القفل البرمجي لظرف الخطوبة: {eng_date}")
            print(f"  [INFO] موعد احتفال عيد الميلاد البرمجي: {bday_date}")
            assert eng_date == "2026-11-25T00:00:00+02:00", f"Unexpected engagementDateCairo: {eng_date}"
            assert bday_date == "2026-12-02T00:00:00+02:00", f"Unexpected targetDateCairo: {bday_date}"
            print("  [PASS] المواعيد البرمجية مطابقة تماماً للمطلوب.")

    chrome_proc.terminate()
    try:
        httpd.shutdown()
    except Exception:
        pass

    print("\n==================================================")
    print("✅ جميع الفحوصات واللقطات اكتملت بنجاح 100%!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_verification())
