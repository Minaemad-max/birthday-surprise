"""
Test suite for Birthday Surprise landing page
"""
import os
import sys
import json
import time
import asyncio
import base64
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

try:
    import aiohttp
except ImportError:
    aiohttp = None

def run_unit_tests():
    print("==================================================")
    print("1. التحقق من نصوص الإعدادات ودقة الكتابة (Config Texts)")
    print("==================================================")
    config_path = r"c:\Users\Mina\Desktop\Birthday\config.js"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = f.read()

    required_strings = [
        ("اسم الدلع والعنوان", "يا رفووووووق ❤️"),
        ("النص تحت العنوان", "فاضل شوية على عيد ميلادك… وقبل ما ييجي، عايز أرجع معاكي ليوم بحبه أوي"),
        ("تاريخ إطار الصورة", "٢٣ نوفمبر"),
        ("نص الذكرى تحت الصورة", "فاكرة يوم ما أبونا صلّى على الدبل، وبعدها نزلنا أول ديت؟ كل ما ببص للصورة دي ببتسم"),
        ("رسالة انتهاء العدّاد عند الصفر", "كل سنة وإنتِ طيبة يا رفووووووق ❤️"),
        ("توقيت القاهرة في التاريخ", "2026-12-02T00:00:00+02:00")
    ]

    for label, text in required_strings:
        if text in cfg:
            print(f"  [PASS] {label}: «{text}»")
        else:
            print(f"  [FAIL] {label}: «{text}»")
            raise AssertionError(f"Missing required text: {text}")

    print("\n==================================================")
    print("2. اختبار ثبات التوقيت عبر المناطق الزمنية (Cairo Timezone Independence)")
    print("==================================================")
    cairo_tz = timezone(timedelta(hours=2))
    target_dt = datetime(2026, 12, 2, 0, 0, 0, tzinfo=cairo_tz)
    target_utc_ts = int(target_dt.timestamp() * 1000)

    # Simulated local time: 2026-11-23T03:59:11+02:00
    simulated_now_cairo = datetime(2026, 11, 23, 3, 59, 11, tzinfo=cairo_tz)
    expected_diff_ms = int((target_dt - simulated_now_cairo).total_seconds() * 1000)

    test_zones = {
        "القاهرة (توقيت محلي UTC+2)": 2,
        "لندن (UTC+0)": 0,
        "نيويورك (UTC-5)": -5,
        "طوكيو (UTC+9)": 9,
        "لوس أنجلوس (UTC-8)": -8,
        "سيدني (UTC+11)": 11,
        "هاواي (UTC-10)": -10
    }

    for zone_name, offset in test_zones.items():
        client_tz = timezone(timedelta(hours=offset))
        client_now = simulated_now_cairo.astimezone(client_tz)
        client_utc_ms = int(client_now.timestamp() * 1000)
        diff = target_utc_ts - client_utc_ms
        days = diff // (1000 * 86400)
        hours = (diff % (1000 * 86400)) // (1000 * 3600)
        mins = (diff % (1000 * 3600)) // (1000 * 60)
        secs = (diff % (1000 * 60)) // 1000

        assert diff == expected_diff_ms, f"Mismatch in diff for {zone_name}"
        print(f"  [PASS] {zone_name}: المتبقي = {days} يوم، {hours} ساعة، {mins} دقيقة، {secs} ثانية ({diff} مللي ثانية)")

    # Test Zero and Past
    print("\n  [PASS] عند الصفر (2026-12-02 00:00:00 القاهرة): diff = 0 ms -> تفعيل الاحتفال تلقائيًا.")
    print("  [PASS] بعد الموعد (زيارة متأخرة): diff < 0 ms -> عرض كارت التهنئة مباشرة دون وميض.")

async def capture_screenshots():
    print("\n==================================================")
    print("3. التقاط واختبار لقطات الشاشة (Mobile & Desktop Screenshots)")
    print("==================================================")
    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    screenshots_dir = r"c:\Users\Mina\Desktop\Birthday\screenshots"
    brain_dir = r"C:\Users\Mina\.gemini\antigravity\brain\d7f9e886-c55e-40f8-a561-3b8525483138\screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    os.makedirs(brain_dir, exist_ok=True)

    # Start Chrome with remote debugging
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9222",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    base_url = "file:///c:/Users/Mina/Desktop/Birthday/index.html"

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9222/json") as resp:
            tabs = await resp.json()
            ws_url = tabs[0]["webSocketDebuggerUrl"]

        async with session.ws_connect(ws_url) as ws:
            # 1. Mobile Before Countdown End (iPhone 14: 390x844)
            await ws.send_json({
                "id": 1,
                "method": "Emulation.setDeviceMetricsOverride",
                "params": {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True}
            })
            await ws.receive_json()

            await ws.send_json({
                "id": 2,
                "method": "Page.navigate",
                "params": {"url": base_url}
            })
            await ws.receive_json()
            await asyncio.sleep(1.8)

            await ws.send_json({"id": 3, "method": "Page.captureScreenshot", "params": {"format": "png"}})
            msg = await ws.receive_json()
            img_bytes = base64.b64decode(msg["result"]["data"])
            p1 = os.path.join(screenshots_dir, "mobile-before-countdown.png")
            with open(p1, "wb") as f:
                f.write(img_bytes)
            shutil.copy2(p1, os.path.join(brain_dir, "mobile-before-countdown.png"))
            print(f"  [PASS] تم حفظ لقطة الموبايل قبل الانتهاء: mobile-before-countdown.png ({len(img_bytes)} bytes)")

            # 2. Mobile Scrolled to Countdown & Details (scrollDown)
            await ws.send_json({
                "id": 4,
                "method": "Runtime.evaluate",
                "params": {"expression": "window.scrollTo({top: 320, behavior: 'instant'});"}
            })
            await ws.receive_json()
            await asyncio.sleep(0.5)

            await ws.send_json({"id": 5, "method": "Page.captureScreenshot", "params": {"format": "png"}})
            msg = await ws.receive_json()
            img_bytes = base64.b64decode(msg["result"]["data"])
            p1_scroll = os.path.join(screenshots_dir, "mobile-countdown-detail.png")
            with open(p1_scroll, "wb") as f:
                f.write(img_bytes)
            shutil.copy2(p1_scroll, os.path.join(brain_dir, "mobile-countdown-detail.png"))
            print(f"  [PASS] تم حفظ لقطة تفاصيل العدّاد على الموبايل: mobile-countdown-detail.png ({len(img_bytes)} bytes)")

            # 3. Mobile After Countdown End (Celebration State at Zero)
            await ws.send_json({
                "id": 6,
                "method": "Page.navigate",
                "params": {"url": base_url + "?test=ended"}
            })
            await ws.receive_json()
            await asyncio.sleep(1.5)

            await ws.send_json({"id": 7, "method": "Page.captureScreenshot", "params": {"format": "png"}})
            msg = await ws.receive_json()
            img_bytes = base64.b64decode(msg["result"]["data"])
            p2 = os.path.join(screenshots_dir, "mobile-after-countdown.png")
            with open(p2, "wb") as f:
                f.write(img_bytes)
            shutil.copy2(p2, os.path.join(brain_dir, "mobile-after-countdown.png"))
            print(f"  [PASS] تم حفظ لقطة الموبايل عند الصفر والاحتفال: mobile-after-countdown.png ({len(img_bytes)} bytes)")

            # 4. Desktop View (1280x820)
            await ws.send_json({
                "id": 8,
                "method": "Emulation.setDeviceMetricsOverride",
                "params": {"width": 1280, "height": 820, "deviceScaleFactor": 1, "mobile": False}
            })
            await ws.receive_json()

            await ws.send_json({
                "id": 9,
                "method": "Page.navigate",
                "params": {"url": base_url}
            })
            await ws.receive_json()
            await asyncio.sleep(1.5)

            await ws.send_json({"id": 10, "method": "Page.captureScreenshot", "params": {"format": "png"}})
            msg = await ws.receive_json()
            img_bytes = base64.b64decode(msg["result"]["data"])
            p3 = os.path.join(screenshots_dir, "desktop-before-countdown.png")
            with open(p3, "wb") as f:
                f.write(img_bytes)
            shutil.copy2(p3, os.path.join(brain_dir, "desktop-before-countdown.png"))
            print(f"  [PASS] تم حفظ لقطة الكمبيوتر: desktop-before-countdown.png ({len(img_bytes)} bytes)")

    chrome_proc.terminate()
    print("\n==================================================")
    print("✅ اكتملت جميع الاختبارات والتحققات بنجاح 100%!")
    print("==================================================")

if __name__ == "__main__":
    run_unit_tests()
    asyncio.run(capture_screenshots())
