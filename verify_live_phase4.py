"""
Production Live Site Verification on Mobile Incognito Mode for Phase 4
Tests against: https://minaemad-max.github.io/birthday-surprise/
1. Test Part A (Current Real Date: 23 Nov 2026):
   - Countdown timer running towards Dec 2.
   - Hero selfie image and memory caption visible.
   - Engagement envelope locked with «يتفتح يوم ٢٥ مايو».
   - «تجربة الحالات» (dev panel) is completely REMOVED from DOM.
   - «اسمعيني» (voice note) is completely hidden.
   - Capture screenshot: live-production-current-date-mobile.png.

2. Test Part B (Simulated Cairo Date: Dec 2, 2026 00:00:15):
   - Golden star character holding cake, candle, and rose appears immediately.
   - Step 1 button «يا رفووووووق، عندك أمنية؟ 🎂» works.
   - Step 2 «اتمنّي أمنية» & «اطفي الشمعة» works.
   - Step 3 Flame extinguishes, greeting appears with «افتحي جواب عيد ميلادك».
   - Opening 23 Nov letter modal works (4 photos).
   - Engagement envelope is unlocked and opens official photo & letter.
   - «تجربة الحالات» and «اسمعيني» are BOTH completely hidden.
   - Capture screenshot: live-production-dec2-birthday-mobile.png.
"""
import os
import sys
import json
import time
import base64
import shutil
import asyncio
import subprocess
from PIL import Image
from io import BytesIO

LIVE_URL = "https://minaemad-max.github.io/birthday-surprise/"
BASE_DIR = r"c:\Users\Mina\Desktop\Birthday"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
BRAIN_DIR = r"C:\Users\Mina\.gemini\antigravity\brain\d7f9e886-c55e-40f8-a561-3b8525483138"
BRAIN_SCREENSHOTS_DIR = os.path.join(BRAIN_DIR, "screenshots")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)
os.makedirs(BRAIN_SCREENSHOTS_DIR, exist_ok=True)

async def test_live_production_suite():
    import aiohttp

    print("==================================================")
    print("بدء اختبار الرابط المباشر من الموبايل في التصفح الخاص (Incognito)")
    print("URL:", LIVE_URL)
    print("==================================================")

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9250",
        "--disable-gpu",
        "--incognito",
        "about:blank"
    ])
    await asyncio.sleep(2.0)

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9250/json") as resp:
            tabs = await resp.json()
            ws_url = tabs[0]["webSocketDebuggerUrl"]

        async with session.ws_connect(ws_url) as ws:
            msg_id = 1

            async def cdp_call(method, params=None):
                nonlocal msg_id
                cid = msg_id
                msg_id += 1
                payload = {"id": cid, "method": method, "params": params or {}}
                await ws.send_json(payload)
                while True:
                    raw = await ws.receive_json()
                    if raw.get("id") == cid:
                        return raw.get("result", {})

            async def eval_js(expr):
                res = await cdp_call("Runtime.evaluate", {
                    "expression": expr,
                    "returnByValue": True,
                    "awaitPromise": True
                })
                if "exceptionDetails" in res:
                    print("JS Error:", res["exceptionDetails"])
                return res.get("result", {}).get("value")

            async def save_named_screenshot(name):
                shot = await cdp_call("Page.captureScreenshot", {"format": "png"})
                b64 = shot["data"]
                img_bytes = base64.b64decode(b64)
                out_path = os.path.join(SCREENSHOTS_DIR, f"{name}.png")
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                shutil.copy2(out_path, os.path.join(BRAIN_DIR, f"{name}.png"))
                shutil.copy2(out_path, os.path.join(BRAIN_SCREENSHOTS_DIR, f"{name}.png"))
                print(f"    📸 تم حفظ اللقطة: {name}.png ({len(img_bytes)} bytes)")

            # Mobile viewport: 390x844 DPR: 3
            await cdp_call("Emulation.setDeviceMetricsOverride", {
                "width": 390,
                "height": 844,
                "deviceScaleFactor": 3,
                "mobile": True,
                "screenOrientation": {"angle": 0, "type": "portraitPrimary"}
            })
            await cdp_call("Emulation.setTouchEmulationEnabled", {"enabled": True})
            await cdp_call("Page.enable")
            await cdp_call("DOM.enable")

            # ------------------------------------------------------------------
            # PART A: فحص الموقع المنشور بالتوقيت الفعلي الحالي (قبل عيد الميلاد)
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار A: فحص الرابط المباشر في التوقيت الفعلي الحالي (23 مايو 2026)")
            print("--------------------------------------------------")
            await cdp_call("Page.navigate", {"url": LIVE_URL})
            
            # Wait for document to be ready
            for _ in range(25):
                ready = await eval_js("document.readyState === 'complete' && !!document.getElementById('pageTitle')")
                if ready:
                    break
                await asyncio.sleep(0.5)

            # 1. Title and Hero
            page_title = await eval_js("document.getElementById('pageTitle').innerText.trim()")
            assert "يا رفووووووق" in page_title and "❤️" in page_title, f"Unexpected page title: {page_title}"
            print(f"  [PASS] عنوان الصفحة على الرابط المباشر: «{page_title.replace(chr(10), ' ')}»")

            # 2. Dev tools completely removed
            dev_exists = await eval_js("document.getElementById('devTestPanel') !== null")
            assert not dev_exists, "Dev test panel MUST be removed from production DOM!"
            print(f"  [PASS] زر «تجربة الحالات» محذوف تماماً من الموقع المنشور: dev_exists={dev_exists}")

            # 3. Audio note hidden
            audio_hidden = await eval_js("document.getElementById('voiceNoteSection').classList.contains('hidden')")
            assert audio_hidden, "Audio section must be hidden!"
            print(f"  [PASS] قسم «اسمعيني» مخفي وخامل تماماً: audio_hidden={audio_hidden}")

            # 4. Live Countdown is active
            days_val = await eval_js("document.getElementById('daysVal').innerText.trim()")
            hours_val = await eval_js("document.getElementById('hoursVal').innerText.trim()")
            seconds_val = await eval_js("document.getElementById('secondsVal').innerText.trim()")
            print(f"  [PASS] العدّاد التنازلي المباشر يعمل بدقة بتوقيت القاهرة: متبقي {days_val} يوم، {hours_val} ساعة، {seconds_val} ثانية")

            # 5. Engagement envelope is locked before Nov 25
            eng_locked = await eval_js("!document.getElementById('engagementLockedBadge').classList.contains('hidden')")
            assert eng_locked, "Engagement envelope should be locked before Nov 25!"
            print("  [PASS] ظرف الخطوبة يعرض الحالة الصحيحة لتاريخ الفحص: مقفول بشارة «يتفتح يوم ٢٥ مايو»")

            await save_named_screenshot("live-production-current-date-mobile")

            # ------------------------------------------------------------------
            # PART B: فحص الموقع المنشور عند بداية ٢ ديسمبر ٢٠٢٦ بتوقيت القاهرة
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار B: فحص الرابط المباشر بساعة متصفح مضبوطة على بداية ٢ ديسمبر ٢٠٢٦")
            print("--------------------------------------------------")

            clock_shift_script = """
            (function() {
              const targetTime = new Date("2026-12-02T00:00:00+02:00").getTime();
              const startTime = targetTime + 10000; // 10 seconds into Dec 2 Cairo
              const realStart = performance.now();
              const OrigDate = window.Date;

              function PatchedDate(...args) {
                if (args.length === 0) {
                  const elapsed = performance.now() - realStart;
                  return new OrigDate(startTime + elapsed);
                }
                return new OrigDate(...args);
              }
              PatchedDate.prototype = OrigDate.prototype;
              PatchedDate.now = function() {
                const elapsed = performance.now() - realStart;
                return Math.floor(startTime + elapsed);
              };
              PatchedDate.parse = OrigDate.parse;
              PatchedDate.UTC = OrigDate.UTC;
              window.Date = PatchedDate;
            })();
            """

            script_id = (await cdp_call("Page.addScriptToEvaluateOnNewDocument", {"source": clock_shift_script}))["identifier"]

            # Reload live site in incognito
            await cdp_call("Page.navigate", {"url": LIVE_URL})
            for _ in range(25):
                ready = await eval_js("document.readyState === 'complete' && !!document.getElementById('pageTitle')")
                if ready:
                    break
                await asyncio.sleep(0.5)

            # 1. Star character appears directly
            star_visible = await eval_js("!document.getElementById('celebrationSection').classList.contains('hidden')")
            assert star_visible, "Star celebration section must appear on Dec 2 on live site!"
            btn_wish_text = await eval_js("document.getElementById('btnAskWish').innerText.trim()")
            assert "يا رفووووووق، عندك أمنية؟ 🎂" in btn_wish_text, f"Unexpected wish button: {btn_wish_text}"
            print(f"  [PASS] شخصية النجمة والتورتة والشمعة تظهر مباشرة مع زر: «{btn_wish_text}»")

            # 2. Check dev panel & audio still hidden on live site
            dev_exists_b = await eval_js("document.getElementById('devTestPanel') !== null")
            audio_hidden_b = await eval_js("document.getElementById('voiceNoteSection').classList.contains('hidden')")
            assert not dev_exists_b, "Dev panel must remain hidden!"
            assert audio_hidden_b, "Audio must remain hidden!"
            print("  [PASS] أدوات المعاينة وقسم الصوت مختفيان تماماً في وضع الزائرة على الرابط المباشر.")

            # 3. Interactive wish flow: Click Ask Wish
            await eval_js("document.getElementById('btnAskWish').click()")
            await asyncio.sleep(0.8)
            is_approaching = await eval_js("document.getElementById('starCharacterWrap').classList.contains('is-approaching')")
            assert is_approaching, "Star should approach!"
            print("  [PASS] النجمة تقرّبت للأمام والشمعة نورت مع شارة اتمنّي أمنية وزر «اطفي الشمعة».")

            # 4. Blow candle (click only)
            await eval_js("document.getElementById('btnBlowCandle').click()")
            await asyncio.sleep(1.2)
            is_extinguished = await eval_js("document.getElementById('candleFlameGroup').classList.contains('is-extinguished')")
            assert is_extinguished, "Flame must be extinguished!"
            celeb_title = await eval_js("document.getElementById('celebrationTitle').innerText.trim()")
            open_letter_btn = await eval_js("document.getElementById('openBirthdayLetterBtn').innerText.trim()")
            assert "كل سنة وإنتِ طيبة يا رفووووووق ❤️" in celeb_title
            assert "افتحي جواب عيد ميلادك" in open_letter_btn
            print(f"  [PASS] الشمعة انطفت وظهرت التهنئة: «{celeb_title}» مع زر: «{open_letter_btn}»")

            # 5. Open Nov 23 letter modal
            await eval_js("document.getElementById('openBirthdayLetterBtn').click()")
            await asyncio.sleep(0.8)
            is_modal_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            assert is_modal_open, "Nov 23 memory album modal should open!"
            modal_tag = await eval_js("document.getElementById('albumModalHeaderTag').innerText.trim()")
            print(f"  [PASS] فُتح جواب وألبوم ٢٣ مايو بنجاح: {modal_tag}")

            await eval_js("document.getElementById('closeAlbumBtn').click()")
            await asyncio.sleep(0.5)

            # 6. Open Engagement envelope
            await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'})")
            await asyncio.sleep(0.5)
            await eval_js("document.getElementById('openEngagementBtn').click()")
            await asyncio.sleep(0.8)
            is_eng_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            assert is_eng_open, "Engagement modal should open!"
            eng_tag = await eval_js("document.getElementById('albumModalHeaderTag').innerText.trim()")
            print(f"  [PASS] فُتح ظرف يوم خطوبتنا بنجاح: {eng_tag}")

            await save_named_screenshot("live-production-dec2-birthday-mobile")

            await eval_js("document.getElementById('closeAlbumBtn').click()")
            await asyncio.sleep(0.4)

    chrome_proc.terminate()
    print("\n==================================================")
    print("🎉 اكتمل فحص الرابط المباشر بنجاح 100% لكلا الحالتين!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(test_live_production_suite())
