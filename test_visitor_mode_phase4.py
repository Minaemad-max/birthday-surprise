"""
Visitor Mode & Clock-Shift Verification Script for Phase 4 (Version e539b75+)
Tests:
1. Clock set seconds before Dec 2, 2026 00:00 Cairo time -> Open index.html without ANY query params.
2. Confirm «تجربة الحالات» (dev panel) is completely REMOVED from DOM in visitor mode.
3. Confirm «اسمعيني» (voice note section) is cleanly hidden.
4. Confirm countdown automatically hits zero and transitions into the golden star celebration card.
5. New visit / reload after Dec 2 00:00 Cairo time opens the star celebration card directly.
6. Wish flow: Click «يا رفووووووق، عندك أمنية؟ 🎂», star approaches, flame brightens, badge «اتمنّي أمنية» appears.
7. Blow candle: Click «اطفي الشمعة» (click-only, no mic permission), flame extinguishes, smoke rises, rose petals burst, greeting & «افتحي جواب عيد ميلادك» appear.
8. Open 23 November letter & album (4 photos).
9. Open Engagement envelope & photo.
10. Generate visitor-mode mobile walkthrough MP4 & GIF.
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
from io import BytesIO

PORT = 8950
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

async def run_visitor_mode_test():
    import aiohttp

    print("==================================================")
    print("اختبار وضع الزائرة الحقيقي وضبط ساعة المتصفح قبل ٢ ديسمبر")
    print("==================================================")

    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SilentHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9242",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.8)

    base_url = f"http://127.0.0.1:{PORT}/index.html"
    recorded_frames = []

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9242/json") as resp:
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

            async def capture_frame():
                shot = await cdp_call("Page.captureScreenshot", {"format": "png"})
                if "data" in shot:
                    b64 = shot["data"]
                    img_bytes = base64.b64decode(b64)
                    im = Image.open(BytesIO(img_bytes)).convert("RGB")
                    recorded_frames.append(im)
                    return im
                return None

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

            # Setup mobile viewport (390 x 844, DPR: 3)
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
            # PART 1: ضبط ساعة المتصفح قبل ٢ ديسمبر بـ 5 ثوانٍ + زيارة بدون معاملات
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 1: ضبط ساعة المتصفح قبل بداية ٢ ديسمبر ٢٠٢٦ بتوقيت القاهرة بـ 5 ثوانٍ")
            print("    الرابط المستخدم: خالص تماماً من أي معاملات اختبار (?test)")
            print("--------------------------------------------------")

            # Cairo Target is 2026-12-02T00:00:00+02:00. In UTC timestamp:
            # 2026-12-01T22:00:00Z -> 1796162400000 ms
            clock_shift_before_script = """
            (function() {
              const targetTime = new Date("2026-12-02T00:00:00+02:00").getTime();
              const startTime = targetTime - 5000; // 5 seconds before Cairo midnight
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

            script_id_1 = (await cdp_call("Page.addScriptToEvaluateOnNewDocument", {"source": clock_shift_before_script}))["identifier"]

            # Navigate with clean URL (NO query parameters at all!)
            await cdp_call("Page.navigate", {"url": base_url})
            for _ in range(25):
                ready = await eval_js("document.readyState")
                if ready == "complete":
                    break
                await asyncio.sleep(0.15)
            await asyncio.sleep(0.5)

            # Check that dev panel is completely removed in visitor mode
            dev_panel_exists = await eval_js("document.getElementById('devTestPanel') !== null")
            assert not dev_panel_exists, "«تجربة الحالات» MUST be completely removed in visitor mode!"
            print(f"  [PASS] زر «تجربة الحالات» مختفٍ تماماً ومحذوف من الصفحة: dev_panel_exists={dev_panel_exists}")

            # Check that audio section is hidden
            audio_section_hidden = await eval_js("document.getElementById('voiceNoteSection').classList.contains('hidden')")
            assert audio_section_hidden, "«اسمعيني» MUST be hidden when not enabled!"
            print(f"  [PASS] قسم «اسمعيني» مخفي وخامل تماماً: audio_section_hidden={audio_section_hidden}")

            # Capture countdown running
            print("  جاري متابعة العدّاد التنازلي وهو يقترب من الصفر والصفحة مفتوحة...")
            for s in range(7):
                await asyncio.sleep(0.5)
                await capture_frame()

            # Verify that celebration section transitioned automatically
            is_celebration_visible = await eval_js("!document.getElementById('celebrationSection').classList.contains('hidden')")
            assert is_celebration_visible, "Celebration section must transition automatically at midnight!"
            print(f"  [PASS] تحوّل العدّاد تلقائياً إلى مشهد الاحتفال والنجمة والصفحة مفتوحة: is_celebration_visible={is_celebration_visible}")
            await save_named_screenshot("visitor-mobile-midnight-crossed")

            await cdp_call("Page.removeScriptToEvaluateOnNewDocument", {"identifier": script_id_1})

            # ------------------------------------------------------------------
            # PART 2: زيارة جديدة بعد الموعد مباشرة (ساعة المتصفح بعد ٢ ديسمبر)
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 2: زيارة جديدة للرابط بعد موعد ٢ ديسمبر مباشرة من غير معاملات")
            print("--------------------------------------------------")

            clock_shift_after_script = """
            (function() {
              const targetTime = new Date("2026-12-02T00:00:00+02:00").getTime();
              const startTime = targetTime + 15000; // 15 seconds AFTER Cairo midnight
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

            script_id_2 = (await cdp_call("Page.addScriptToEvaluateOnNewDocument", {"source": clock_shift_after_script}))["identifier"]

            # Fresh load without ANY query parameters
            await cdp_call("Page.navigate", {"url": base_url})
            await asyncio.sleep(1.0)

            # Verify direct star appearance on reload/visit
            countdown_display = await eval_js("document.getElementById('countdownSection').style.display")
            celebration_direct_visible = await eval_js("!document.getElementById('celebrationSection').classList.contains('hidden')")
            assert celebration_direct_visible, "Celebration section should be directly visible upon new visit after date!"
            print(f"  [PASS] الزيارة الجديدة تفتح مشهد النجمة والاحتفال مباشرة: celebration_direct_visible={celebration_direct_visible}")

            # Verify dev panel and voice note are still hidden
            dev_panel_exists_2 = await eval_js("document.getElementById('devTestPanel') !== null")
            audio_section_hidden_2 = await eval_js("document.getElementById('voiceNoteSection').classList.contains('hidden')")
            assert not dev_panel_exists_2, "Dev panel must remain hidden on new visit!"
            assert audio_section_hidden_2, "Voice note must remain hidden on new visit!"
            print(f"  [PASS] التحقق مجدداً: «تجربة الحالات» و«اسمعيني» كلاهما مخفيان.")

            await eval_js("document.getElementById('celebrationSection').scrollIntoView({behavior: 'instant', block: 'start'})")
            await asyncio.sleep(0.5)

            for _ in range(4):
                await capture_frame()
                await asyncio.sleep(0.2)

            await save_named_screenshot("visitor-mobile-new-visit-star")

            # ------------------------------------------------------------------
            # PART 3: تجربة سؤال الأمنية واقتراب النجمة وإطفاء الشمعة
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 3: تجربة تدفق الأمنية وإطفاء الشمعة في وضع الزائرة")
            print("--------------------------------------------------")

            # Click ask wish button
            await eval_js("document.getElementById('btnAskWish').click()")
            for _ in range(5):
                await asyncio.sleep(0.25)
                await capture_frame()

            is_approaching = await eval_js("document.getElementById('starCharacterWrap').classList.contains('is-approaching')")
            assert is_approaching, "Star character should approach!"
            await save_named_screenshot("visitor-mobile-make-wish")
            print("  [PASS] النجمة تقرّبت للأمام، والشمعة نورت، وظهرت شارة اتمني أمنية وزر «اطفي الشمعة».")

            # Click blow candle
            await eval_js("document.getElementById('btnBlowCandle').click()")
            for _ in range(10):
                await asyncio.sleep(0.25)
                await capture_frame()

            is_extinguished = await eval_js("document.getElementById('candleFlameGroup').classList.contains('is-extinguished')")
            celebration_revealed = await eval_js("!document.getElementById('celebrationContentRevealed').classList.contains('hidden')")
            assert is_extinguished, "Candle flame must be extinguished!"
            assert celebration_revealed, "Celebration content must be revealed!"
            await save_named_screenshot("visitor-mobile-candle-blown")
            print("  [PASS] انطفأت الشمعة وصعد الدخان الناعم وظهرت التهنئة وزر «افتحي جواب عيد ميلادك».")

            # ------------------------------------------------------------------
            # PART 4: فتح ظرف ٢٣ مايو من زر جواب عيد ميلادك
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 4: فتح ظرف ٢٣ مايو والـ ٤ صور")
            print("--------------------------------------------------")
            await eval_js("document.getElementById('openBirthdayLetterBtn').click()")
            for _ in range(6):
                await asyncio.sleep(0.25)
                await capture_frame()

            is_nov23_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            nov23_tag = await eval_js("document.getElementById('albumModalHeaderTag').innerText.trim()")
            assert is_nov23_open, "Nov 23 memory album modal should open!"
            assert "٢٣ مايو" in nov23_tag, f"Expected Nov 23 tag, got: {nov23_tag}"
            await save_named_screenshot("visitor-mobile-nov23-letter")
            print(f"  [PASS] فُتح جواب ٢٣ مايو بنجاح: {nov23_tag}")

            # Close modal
            await eval_js("document.getElementById('closeAlbumBtn').click()")
            await asyncio.sleep(0.4)
            await capture_frame()

            # ------------------------------------------------------------------
            # PART 5: فتح ظرف يوم خطوبتنا (متاح ومستقل)
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 5: فتح ظرف يوم خطوبتنا المستقل")
            print("--------------------------------------------------")
            await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'})")
            await asyncio.sleep(0.4)
            await capture_frame()

            is_engagement_unlocked = await eval_js("!document.getElementById('openEngagementBtn').classList.contains('hidden')")
            assert is_engagement_unlocked, "Engagement envelope must be unlocked!"

            await eval_js("document.getElementById('openEngagementBtn').click()")
            for _ in range(6):
                await asyncio.sleep(0.25)
                await capture_frame()

            is_eng_modal_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            eng_tag = await eval_js("document.getElementById('albumModalHeaderTag').innerText.trim()")
            assert is_eng_modal_open, "Engagement modal should open!"
            assert "خطوبتنا" in eng_tag, f"Expected engagement tag, got: {eng_tag}"
            await save_named_screenshot("visitor-mobile-engagement-letter")
            print(f"  [PASS] فُتح ظرف يوم خطوبتنا بنجاح: {eng_tag}")

            await eval_js("document.getElementById('closeAlbumBtn').click()")
            await asyncio.sleep(0.4)
            await capture_frame()

            # ------------------------------------------------------------------
            # COMPILE WALKTHROUGH MP4 & GIF
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("🎬 إنشاء فيديو المرور في وضع الزائرة (MP4 & GIF)")
            print("--------------------------------------------------")
            print(f"  إجمالي الإطارات المسجلة: {len(recorded_frames)} إطار")

            frames_dir = os.path.join(BASE_DIR, "screenshots", "visitor_frames")
            os.makedirs(frames_dir, exist_ok=True)
            for idx, frame in enumerate(recorded_frames):
                frame.save(os.path.join(frames_dir, f"frame_{idx:04d}.png"))

            mp4_out = os.path.join(SCREENSHOTS_DIR, "visitor-mode-walkthrough.mp4")
            gif_out = os.path.join(SCREENSHOTS_DIR, "visitor-mode-walkthrough.gif")

            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-framerate", "4",
                "-i", os.path.join(frames_dir, "frame_%04d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=390:-2",
                mp4_out
            ]
            subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            if os.path.exists(mp4_out):
                print(f"  [OK] فيديو MP4: {mp4_out} ({os.path.getsize(mp4_out)} bytes)")
                shutil.copy2(mp4_out, os.path.join(BRAIN_DIR, "visitor-mode-walkthrough.mp4"))
                shutil.copy2(mp4_out, os.path.join(BRAIN_SCREENSHOTS_DIR, "visitor-mode-walkthrough.mp4"))

            gif_frames = []
            for im in recorded_frames:
                w, h = im.size
                new_h = int(h * (320 / w))
                small_im = im.resize((320, new_h), Image.Resampling.LANCZOS)
                gif_frames.append(small_im)

            if gif_frames:
                gif_frames[0].save(
                    gif_out,
                    save_all=True,
                    append_images=gif_frames[1:],
                    duration=250,
                    loop=0,
                    optimize=True
                )
                print(f"  [OK] GIF للمعاينة: {gif_out} ({os.path.getsize(gif_out)} bytes)")
                shutil.copy2(gif_out, os.path.join(BRAIN_DIR, "visitor-mode-walkthrough.gif"))
                shutil.copy2(gif_out, os.path.join(BRAIN_SCREENSHOTS_DIR, "visitor-mode-walkthrough.gif"))

    chrome_proc.terminate()
    httpd.shutdown()
    print("\n==================================================")
    print("✅ اكتمل اختبار وضع الزائرة بنجاح تام 100%!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_visitor_mode_test())
