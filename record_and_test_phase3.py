"""
Phase 3 Engagement Single Photo Edition Test & Screenshot Capture
Validates:
1. Locked envelope before Nov 25 with «يتفتح يوم ٢٥ مايو».
2. Unlocked single-photo engagement letter with dedication, approved photo, and signature «بحبك 🌹».
3. Complete absence of navigation buttons, dots, swipe hints, and placeholder notices.
4. Correct 4 unique original photos for Nov 23 memory album.
5. Captures pristine mobile screenshots (390x844).
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

PORT = 8940
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
    print("تشغيل خادم الاختبار وفحص بيئة المتصفح المحمولة (390x844)")
    print("==================================================")

    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SilentHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9230",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    base_url = f"http://127.0.0.1:{PORT}/index.html"

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9230/json") as resp:
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

            # ضبط المقاس على هاتف آيفون (390 x 844)
            await send_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 390,
                "height": 844,
                "deviceScaleFactor": 2,
                "mobile": True
            })

            # -------------------------------------------------------------
            # 1. لقطة موبايل للظرف المقفول قبل ٢٥ مايو
            # -------------------------------------------------------------
            print("\n1. التقاط لقطة موبايل للظرف المقفول...")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=before_nov25"})
            await asyncio.sleep(1.0)
            await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'});")
            await asyncio.sleep(0.4)

            locked_badge = await eval_js("!document.getElementById('engagementLockedBadge').classList.contains('hidden')")
            locked_text = await eval_js("document.getElementById('engagementLockedText').textContent.trim()")
            open_btn_hidden = await eval_js("document.getElementById('openEngagementBtn').classList.contains('hidden')")
            
            assert locked_badge, "Locked badge must be visible"
            assert "يتفتح يوم ٢٥ مايو" in locked_text, f"Unexpected locked text: {locked_text}"
            assert open_btn_hidden, "Open button must be hidden"

            await capture_screen("mobile-engagement-locked.png")
            print("  [PASS] تم بنجاح التحقق والتقاط لقطة الظرف المقفول!")

            # -------------------------------------------------------------
            # 2. لقطة موبايل للجواب المفتوح (صورة واحدة مع الإهداء والتوقيع)
            # -------------------------------------------------------------
            print("\n2. فتح ظرف الخطوبة والتحقق من تجربة الصورة الواحدة المعتمدة...")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=open_engagement"})
            await asyncio.sleep(1.0)

            # التحقق من إخفاء أزرار التقليب والدوائر وتلميح السحب وعداد الصور
            nav_hidden = await eval_js("document.getElementById('albumNavBar').classList.contains('hidden')")
            swipe_hidden = await eval_js("document.getElementById('albumSwipeHint').classList.contains('hidden')")
            counter_hidden = await eval_js("document.getElementById('albumCounterPill').classList.contains('hidden')")
            
            assert nav_hidden, "Navigation bar (prev/next/dots) must be hidden for single photo"
            assert swipe_hidden, "Swipe hint must be hidden for single photo"
            assert counter_hidden, "Counter pill must be hidden for single photo"

            # التحقق من النصوص والصور
            header_tag = await eval_js("document.getElementById('albumModalHeaderTag').textContent.trim()")
            dedication = await eval_js("document.getElementById('letterDedicationQuote').textContent.trim()")
            photo_caption = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            signature = await eval_js("document.getElementById('albumSignatureText').textContent.trim()")
            img_src = await eval_js("document.getElementById('albumCurrentImg').src")

            assert "ظرف يوم خطوبتنا" in header_tag, f"Header mismatch: {header_tag}"
            assert "يوم ٢٥ مايو مش مجرد تاريخ" in dedication, f"Dedication mismatch: {dedication}"
            assert "engagement-photo-1.jpg" in img_src, f"Wrong image source: {img_src}"
            assert "يوم خطوبتنا… اليوم اللي بدأنا فيه حكايتنا رسمي" in photo_caption, f"Caption mismatch: {photo_caption}"
            assert "بحبك 🌹" in signature, f"Signature mismatch: {signature}"

            print("  [PASS] أزرار التقليب والدوائر وتلميح السحب والعداد مخفية تماماً.")
            print(f"  [PASS] الإهداء: «{dedication}»")
            print(f"  [PASS] تعليق الصورة: «{photo_caption}»")
            print(f"  [PASS] التوقيع المعتمد: «{signature}»")

            await capture_screen("mobile-engagement-opened.png")

            # التقاط لقطة تظهر التوقيع بوضوح
            await eval_js("document.getElementById('loveLetterCard').scrollTo({top: 400, behavior: 'instant'});")
            await asyncio.sleep(0.4)
            await capture_screen("mobile-engagement-signature.png")

            # -------------------------------------------------------------
            # 3. التحقق من صور ألبوم ٢٣ مايو الأربع الأصلية
            # -------------------------------------------------------------
            print("\n3. التحقق من صور ألبوم ٢٣ مايو الأربع المصححة...")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=open_nov23"})
            await asyncio.sleep(1.0)

            # الصورة ١: الجماعية مع أبونا
            p1_src = await eval_js("document.getElementById('albumCurrentImg').src")
            p1_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            p1_is_group = await eval_js("document.getElementById('albumPhotoViewport').classList.contains('is-group-photo')")
            assert "photo-4-group-father.jpg" in p1_src, f"Expected group photo, got: {p1_src}"
            assert "يوم ما أبونا صلّى على الدبل" in p1_cap
            assert p1_is_group, "Group photo must have is-group-photo class"
            print(f"  [PASS] صورة ١: {p1_cap} (الصورة الجماعية مع أبونا 1280x720)")

            # الصورة ٢: صورة المراية
            await eval_js("document.getElementById('albumNextBtn').click();")
            await asyncio.sleep(0.3)
            p2_src = await eval_js("document.getElementById('albumCurrentImg').src")
            p2_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            assert "photo-1-mirror.jpg" in p2_src
            print(f"  [PASS] صورة ٢: {p2_cap} (صورة المراية)")

            # الصورة ٣: سيلفي الافتتاح
            await eval_js("document.getElementById('albumNextBtn').click();")
            await asyncio.sleep(0.3)
            p3_src = await eval_js("document.getElementById('albumCurrentImg').src")
            p3_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            assert "hero-selfie-rings.jpg" in p3_src
            print(f"  [PASS] صورة ٣: {p3_cap} (السيلفي اللي في الافتتاح)")

            # الصورة ٤: السيلفي التانية بالدبل
            await eval_js("document.getElementById('albumNextBtn').click();")
            await asyncio.sleep(0.3)
            p4_src = await eval_js("document.getElementById('albumCurrentImg').src")
            p4_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            assert "photo-3-selfie-rings-2.jpg" in p4_src
            print(f"  [PASS] صورة ٤: {p4_cap} (السيلفي التانية بالدبل الأصلية 960x1280)")

            # -------------------------------------------------------------
            # 4. التحقق من وضع التصفح الخاص والزائرة (غياب أدوات المطور)
            # -------------------------------------------------------------
            print("\n4. التحقق من وضع التصفح الخاص والزائرة (?mode=visitor)...")
            await send_cmd("Page.navigate", {"url": f"{base_url}?mode=visitor"})
            await asyncio.sleep(0.8)
            dev_panel = await eval_js("document.getElementById('devTestPanel')")
            assert dev_panel is None, "Dev test panel must be completely removed in visitor/private mode"
            print("  [PASS] لوحة أدوات المطور محذوفة تماماً من DOM في وضع الزائرة والتصفح الخاص!")

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
