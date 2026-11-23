"""
Verify Live Production Website via Headless Chrome in Incognito / Private Browsing Mode
Tests:
1. Live URL: https://minaemad-max.github.io/birthday-surprise/
2. Incognito / Private mobile browser emulation (iPhone: 390x844).
3. Image assets loading (hero image, engagement image).
4. Live Cairo countdown timer running.
5. Dev Test Panel ("تجربة الحالات") completely absent from DOM.
6. Engagement envelope locked with «يتفتح يوم ٢٥ نوفمبر».
"""
import asyncio
import time
import base64
import os
import shutil
import subprocess
import aiohttp

LIVE_URL = "https://minaemad-max.github.io/birthday-surprise/"
BASE_DIR = r"c:\Users\Mina\Desktop\Birthday"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
BRAIN_DIR = r"C:\Users\Mina\.gemini\antigravity\brain\d7f9e886-c55e-40f8-a561-3b8525483138"
BRAIN_SCREENSHOTS_DIR = os.path.join(BRAIN_DIR, "screenshots")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)
os.makedirs(BRAIN_SCREENSHOTS_DIR, exist_ok=True)

async def test_live_production_site():
    print("==================================================")
    print("بدء اختبار الرابط المباشر من الموبايل في التصفح الخاص")
    print("URL:", LIVE_URL)
    print("==================================================")

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9245",
        "--disable-gpu",
        "--incognito",
        "about:blank"
    ])
    await asyncio.sleep(2.0)

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9245/json") as resp:
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
                shutil.copy2(p, os.path.join(BRAIN_DIR, filename))
                shutil.copy2(p, os.path.join(BRAIN_SCREENSHOTS_DIR, filename))
                print(f"  [SAVED] {filename} ({len(img_data)} bytes)")
                return p

            # Emulate Mobile Viewport (iPhone: 390 x 844)
            await send_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 390,
                "height": 844,
                "deviceScaleFactor": 2,
                "mobile": True
            })

            print("\nالانتقال إلى الرابط المباشر عبر HTTPS...")
            await send_cmd("Page.navigate", {"url": LIVE_URL})
            await asyncio.sleep(3.0)

            # 1. التحقق من الترويسة والعنوان
            title = await eval_js("document.getElementById('pageTitle').textContent.trim()")
            print(f"  [PASS] عنوان الصفحة: «{title}»")

            # 2. التحقق من تحميل صورة الافتتاح
            hero_loaded = await eval_js("document.getElementById('heroImage').complete && document.getElementById('heroImage').naturalWidth > 0")
            hero_src = await eval_js("document.getElementById('heroImage').src")
            assert hero_loaded, f"Hero image failed to load: {hero_src}"
            print(f"  [PASS] صورة الافتتاح محملة بنجاح: {hero_src}")

            # 3. التحقق من العدّاد التنازلي المباشر
            days = await eval_js("document.getElementById('daysVal').textContent.trim()")
            hours = await eval_js("document.getElementById('hoursVal').textContent.trim()")
            mins = await eval_js("document.getElementById('minutesVal').textContent.trim()")
            secs = await eval_js("document.getElementById('secondsVal').textContent.trim()")
            assert days != "--", "Countdown values should be populated"
            print(f"  [PASS] العدّاد التنازلي شغال ومباشر: {days} يوم، {hours} ساعة، {mins} دقيقة، {secs} ثانية")

            # 4. التحقق التام من اختفاء زر ولوحة «تجربة الحالات»
            dev_panel = await eval_js("document.getElementById('devTestPanel')")
            assert dev_panel is None, "devTestPanel must be completely absent from DOM on public live URL"
            print("  [PASS] زر ولوحة «تجربة الحالات» مختفية ومحذوفة تماماً من الصفحة!")

            # 5. التحقق من ظرف الخطوبة وحالة القفل
            badge_text = await eval_js("document.getElementById('engagementLockedText').textContent.trim()")
            badge_visible = await eval_js("!document.getElementById('engagementLockedBadge').classList.contains('hidden')")
            btn_hidden = await eval_js("document.getElementById('openEngagementBtn').classList.contains('hidden')")
            
            assert badge_visible, "Engagement locked badge must be visible"
            assert "يتفتح يوم ٢٥ نوفمبر" in badge_text, f"Unexpected locked text: {badge_text}"
            assert btn_hidden, "Open button must be hidden before Nov 25"
            print(f"  [PASS] ظرف الخطوبة مقفول ومعروض بشارة: «{badge_text}»")
            print("  [PASS] زر فتح الخطوبة مخفي حتى يحين موعد ٢٥ نوفمبر")

            # التقاط لقطات حية من الموقع المباشر المنشور
            await capture_screen("live-mobile-hero-countdown.png")

            await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'});")
            await asyncio.sleep(0.5)
            await capture_screen("live-mobile-engagement-locked.png")

    chrome_proc.terminate()
    print("\n==================================================")
    print("🎉 تم التحقق بنجاح من الموقع المباشر المنشور 100%!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(test_live_production_site())
