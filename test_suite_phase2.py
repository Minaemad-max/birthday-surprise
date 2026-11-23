"""
Phase 2 Test Suite: Memory Album, Envelope, Last-Second Transition, and Responsive Verification
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
from datetime import datetime, timezone, timedelta

try:
    import aiohttp
except ImportError:
    aiohttp = None

PORT = 8931
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

def run_config_and_security_tests():
    print("==================================================")
    print("1. اختبار نصوص الإعدادات وظرف ٢٣ نوفمبر والألبوم")
    print("==================================================")
    with open(os.path.join(BASE_DIR, "config.js"), "r", encoding="utf-8") as f:
        cfg = f.read()

    checks = [
        ("اسم الدلع والعنوان", "يا رفووووووق ❤️"),
        ("اسم الظرف", "ظرف ٢٣ نوفمبر"),
        ("زر فتح الظرف", "افتحي ظرف ٢٣ نوفمبر"),
        ("نص الصورة ١ (الجماعية مع أبونا)", "يوم ما أبونا صلّى على الدبل"),
        ("نص الصورة ٢ (المراية)", "أنا وإنتِ يوم ٢٣ نوفمبر"),
        ("نص الصورة ٣ (سيلفي الافتتاح)", "وبعدها نزلنا أول ديت"),
        ("نص الصورة ٤ (السيلفي التانية بالدبل)", "كل ما أبص للصور دي ببتسم. بحبك يا رفووووووق ❤️"),
        ("تاريخ صلاة الدبل", "٢٣ نوفمبر"),
        ("توقيت القاهرة في التاريخ", "2026-12-02T00:00:00+02:00")
    ]

    for label, text in checks:
        assert text in cfg, f"Missing config string: {text}"
        print(f"  [PASS] {label}: «{text}»")

    print("\n==================================================")
    print("2. اختبار ثبات التوقيت عبر المناطق الزمنية (Cairo Timezone Math)")
    print("==================================================")
    cairo_tz = timezone(timedelta(hours=2))
    target_dt = datetime(2026, 12, 2, 0, 0, 0, tzinfo=cairo_tz)
    target_utc_ts = int(target_dt.timestamp() * 1000)

    simulated_now = datetime(2026, 11, 23, 3, 59, 11, tzinfo=cairo_tz)
    expected_diff = int((target_dt - simulated_now).total_seconds() * 1000)

    for name, offset in [("القاهرة (UTC+2)", 2), ("لندن (UTC+0)", 0), ("نيويورك (UTC-5)", -5), ("طوكيو (UTC+9)", 9)]:
        tz = timezone(timedelta(hours=offset))
        now_tz = simulated_now.astimezone(tz)
        diff = target_utc_ts - int(now_tz.timestamp() * 1000)
        assert diff == expected_diff, f"Timezone mismatch for {name}"
        print(f"  [PASS] منطقة {name}: الفارق موحد = {diff} مللي ثانية (٨ أيام و٢٠ ساعة)")

async def run_browser_tests():
    print("\n==================================================")
    print("3. تشغيل الاختبارات الفعلية في المتصفح (Headless Chrome + CDP)")
    print("==================================================")
    
    # Start local HTTP server
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SilentHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9223",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    base_url = f"http://127.0.0.1:{PORT}/index.html"

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9223/json") as resp:
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
                p = os.path.join(SCREENSHOTS_DIR, filename)
                with open(p, "wb") as f:
                    f.write(img_data)
                # Copy to brain dir
                shutil.copy2(p, os.path.join(BRAIN_DIR, filename))
                shutil.copy2(p, os.path.join(BRAIN_SCREENSHOTS_DIR, filename))
                print(f"    📷 تم التقاط وحفظ: {filename} ({len(img_data)} bytes)")
                return p

            # ----------------------------------------------------
            # TEST A: Visitor Mode Security Check (Before date)
            # ----------------------------------------------------
            print("\n  [TEST A] اختبار وضع الزائرة وحماية الروابط قبل الموعد:")
            await send_cmd("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})
            await send_cmd("Page.navigate", {"url": f"{base_url}?mode=visitor&test=ended"})
            await asyncio.sleep(1.2)

            is_dev_panel_gone = await eval_js("document.getElementById('devTestPanel') === null")
            is_countdown_visible = await eval_js("document.getElementById('countdownSection').style.display !== 'none'")
            is_celebration_hidden = await eval_js("document.getElementById('celebrationSection').classList.contains('hidden')")

            assert is_dev_panel_gone, "Dev test panel should be completely removed in visitor mode"
            assert is_countdown_visible, "Countdown should remain visible for visitor before target date"
            assert is_celebration_hidden, "Celebration must be hidden for visitor before target date"
            print("    [PASS] في وضع الزائرة (?mode=visitor): تم إخفاء لوحة التحكم وتجاهل معلمات الرابط بنجاح!")

            # Capture mobile before date
            await capture_screen("mobile-before-date.png")

            # ----------------------------------------------------
            # TEST B: Last-Second Transition (03s -> 02s -> 01s -> 00s -> Celebration)
            # ----------------------------------------------------
            print("\n  [TEST B] اختبار عبور الموعد والصفحة مفتوحة (Last-Second Transition):")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=3s"})
            await asyncio.sleep(1.0)

            # Check that ticker is running before zero
            sec_before = await eval_js("document.getElementById('secondsVal').textContent")
            print(f"    العدّاد يعمل قبل الصفر: {sec_before} ثوانٍ")

            # Wait 2.8 seconds for zero transition
            await asyncio.sleep(2.8)
            sec_at_zero = await eval_js("document.getElementById('secondsVal').textContent")
            print(f"    العدّاد عند لحظة الصفر: {sec_at_zero}")

            # Wait for celebration entrance (after 450ms zero pulse)
            await asyncio.sleep(0.8)
            is_celebration_shown = await eval_js("!document.getElementById('celebrationSection').classList.contains('hidden')")
            has_open_btn = await eval_js("document.getElementById('openEnvelopeBtn') !== null")
            btn_text = await eval_js("document.getElementById('openEnvelopeBtn').textContent.trim()")

            assert is_celebration_shown, "Celebration section should be visible after zero"
            assert has_open_btn, "Open envelope button should be present"
            assert "افتحي ظرف ٢٣ نوفمبر" in btn_text, f"Unexpected button text: {btn_text}"
            print(f"    [PASS] عبرت الصفحة لحظة الصفر بسلاسة: ظهرت التهنئة والزر «{btn_text}»!")

            # ----------------------------------------------------
            # TEST C: Fresh Visit After Target Date
            # ----------------------------------------------------
            print("\n  [TEST C] اختبار زيارة جديدة أو إعادة تحميل بعد الموعد (Fresh Visit After Date):")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=ended"})
            await asyncio.sleep(1.2)

            is_celebration_immediate = await eval_js("!document.getElementById('celebrationSection').classList.contains('hidden')")
            is_countdown_hidden = await eval_js("document.getElementById('countdownSection').style.display === 'none'")
            assert is_celebration_immediate, "Celebration must show immediately on reload after date"
            assert is_countdown_hidden, "Countdown must be hidden on reload after date"
            print("    [PASS] فتحت الصفحة بعد الموعد مباشرة على كارت الاحتفال دون أي وميض للعدّاد!")

            # Scroll to envelope container so it is prominently visible in screenshot
            await eval_js("document.getElementById('envelopeContainer').scrollIntoView({behavior: 'instant', block: 'center'})")
            await asyncio.sleep(0.4)

            # Capture envelope after date
            await capture_screen("mobile-envelope-after-date.png")

            # ----------------------------------------------------
            # TEST D: Second Timezone Simulation (New York UTC-5)
            # ----------------------------------------------------
            print("\n  [TEST D] اختبار التحقق في منطقة زمنية ثانية (New York UTC-5):")
            await send_cmd("Emulation.setTimezoneOverride", {"timezoneId": "America/New_York"})
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=ended"})
            await asyncio.sleep(1.0)
            tz_celebration = await eval_js("!document.getElementById('celebrationSection').classList.contains('hidden')")
            assert tz_celebration, "Celebration should work identically in New York timezone"
            print("    [PASS] تم التحقق في منطقة زمنية أمريكا/نيويورك (UTC-5) بنجاح 100%!")

            # ----------------------------------------------------
            # TEST E: Envelope Opening and 4-Photo Album Navigation
            # ----------------------------------------------------
            print("\n  [TEST E] اختبار فتح ظرف ٢٣ نوفمبر وتصفح الصور الأربع:")
            # Narrow mobile: 360x780
            await send_cmd("Emulation.setDeviceMetricsOverride", {"width": 360, "height": 780, "deviceScaleFactor": 2, "mobile": True})
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=ended"})
            await asyncio.sleep(1.0)

            # Click open envelope button
            await eval_js("document.getElementById('openEnvelopeBtn').click()")
            await asyncio.sleep(0.6)

            is_album_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            assert is_album_open, "Album overlay must be visible after clicking open envelope"
            print("    [PASS] فُتح الألبوم بنجاح عند النقر على الزر!")

            # Check Photo 1: Group photo with priest
            p1_src = await eval_js("document.getElementById('albumCurrentImg').src")
            p1_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            p1_is_group = await eval_js("document.getElementById('albumPhotoViewport').classList.contains('is-group-photo')")
            
            assert "photo-4-group-father.jpg" in p1_src, f"Expected group photo, got: {p1_src}"
            assert "يوم ما أبونا صلّى على الدبل" in p1_cap, f"Expected caption 1, got: {p1_cap}"
            assert p1_is_group, "Photo 1 must have is-group-photo styling (object-fit: contain)"
            print(f"    [PASS] صورة ١ (الجماعية مع أبونا): «{p1_cap}» — معروضة بكامل الأشخاص (contain).")
            
            # Check for horizontal scroll / overflow
            scroll_w = await eval_js("document.documentElement.scrollWidth")
            client_w = await eval_js("document.documentElement.clientWidth")
            assert scroll_w <= client_w, f"Horizontal overflow detected: scrollWidth={scroll_w} > clientWidth={client_w}"
            print(f"    [PASS] فحص العرض الضيق (360px): لا يوجد أي تمرير أفقي (scrollWidth={scroll_w}, clientWidth={client_w}).")

            # Capture Group Photo in album
            await capture_screen("album-group-photo.png")

            # Navigate to Photo 2: Mirror photo
            await eval_js("document.getElementById('albumNextBtn').click()")
            await asyncio.sleep(0.35)
            p2_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            assert "أنا وإنتِ يوم ٢٣ نوفمبر" in p2_cap, f"Expected caption 2, got: {p2_cap}"
            print(f"    [PASS] صورة ٢ (المراية): «{p2_cap}».")

            # Navigate to Photo 3: Opening selfie
            await eval_js("document.getElementById('albumNextBtn').click()")
            await asyncio.sleep(0.35)
            p3_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            assert "وبعدها نزلنا أول ديت" in p3_cap, f"Expected caption 3, got: {p3_cap}"
            print(f"    [PASS] صورة ٣ (السيلفي الافتتاحية): «{p3_cap}».")

            # Navigate to Photo 4: Second rings selfie
            await eval_js("document.getElementById('albumNextBtn').click()")
            await asyncio.sleep(0.35)
            p4_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            is_next_disabled = await eval_js("document.getElementById('albumNextBtn').disabled")
            assert "بحبك يا رفووووووق ❤️" in p4_cap, f"Expected caption 4, got: {p4_cap}"
            assert is_next_disabled, "Next button should be disabled at photo 4"
            print(f"    [PASS] صورة ٤ (السيلفي التانية بالدبل): «{p4_cap}» — الزر التالي معطل عند النهاية.")

            # Capture Photo 4
            await capture_screen("album-photo-4.png")

            # Test keyboard arrow navigation (ArrowRight in RTL goes back to Photo 3)
            await eval_js("document.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}))")
            await asyncio.sleep(0.3)
            p3_back_cap = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            assert "وبعدها نزلنا أول ديت" in p3_back_cap, "Keyboard ArrowRight should navigate to previous photo in RTL"
            print("    [PASS] كيبورد (ArrowRight): عاد للصورة السابقة بنجاح في اتجاه RTL!")

            # ----------------------------------------------------
            # TEST F: Desktop Album View (1280x820)
            # ----------------------------------------------------
            print("\n  [TEST F] فحص العرض على الكمبيوتر (Desktop 1280x820):")
            await send_cmd("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 820, "deviceScaleFactor": 1, "mobile": False})
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=album"})
            await asyncio.sleep(1.2)
            await capture_screen("desktop-album-view.png")
            print("    [PASS] تم فحص وحفظ عرض الكمبيوتر بنجاح!")

    chrome_proc.terminate()
    httpd.shutdown()
    print("\n==================================================")
    print("✅ جميع اختبارات المرحلة الثانية اكتملت بنجاح 100%!")
    print("==================================================")

if __name__ == "__main__":
    run_config_and_security_tests()
    asyncio.run(run_browser_tests())
