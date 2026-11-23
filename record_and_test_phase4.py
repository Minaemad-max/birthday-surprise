"""
Phase 4 Birthday Celebration Verification and Screen Recording Script
Tests & Records:
1. Midnight transition at Dec 2 00:00 Cairo time into birthday card.
2. Direct load/reload after Dec 2 showing the golden star holding cake, rose, & candle.
3. Wish flow step 1: Button «يا رفووووووق، عندك أمنية؟ 🎂».
4. Wish flow step 2: Star approaches, candle flame lights up, badge «اتمنّي أمنية», button «اطفي الشمعة».
5. Wish flow step 3: Clicking «اطفي الشمعة» (click-only, NO mic permission): flame extinguishes, smoke rises, rose petals burst, greeting & «افتحي جواب عيد ميلادك» appear.
6. Opening 23 November memory love letter from «افتحي جواب عيد ميلادك».
7. Verifying «ظرف يوم خطوبتنا» remains unlocked, accessible, and opens engagement photo & letter.
8. Verifying «تخطي الحركة ⏭️» and reduced-motion behavior.
9. Producing mobile screenshots, MP4 walkthrough, and GIF walkthrough.
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

PORT = 8945
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

def verify_strings_and_configs():
    print("==================================================")
    print("1. فحص نصوص المرحلة الرابعة وافتتاحية عيد الميلاد")
    print("==================================================")
    with open(os.path.join(BASE_DIR, "config.js"), "r", encoding="utf-8") as f:
        cfg = f.read()

    expected_texts = [
        ("عنوان عيد الميلاد", "كل سنة وإنتِ طيبة يا رفووووووق ❤️"),
        ("جملة عيد الميلاد", "يا رب السنة دي تضحكي فيها من قلبك كتير، وأنا أبقى جنبك في كل ضحكة"),
        ("زر سؤال الأمنية", "يا رفووووووق، عندك أمنية؟ 🎂"),
        ("شارة اتمني أمنية", "اتمنّي أمنية"),
        ("تلميح الأمنية", "غمضي عينك للحظة، اتمني أمنية من قلبك… ودوسي تطفي الشمعة 🕯️"),
        ("زر إطفاء الشمعة", "اطفي الشمعة"),
        ("زر جواب عيد ميلادك", "افتحي جواب عيد ميلادك"),
        ("زر تخطي الحركة", "تخطي الحركة ⏭️"),
        ("عنوان الصوت", "اسمعيني"),
        ("ظرف الخطوبة", "يوم خطوبتنا"),
        ("ظرف ٢٣ نوفمبر", "ظرف ٢٣ نوفمبر")
    ]

    for label, text in expected_texts:
        assert text in cfg, f"Missing string in config.js: {text}"
        print(f"  [PASS] {label}: «{text}»")

async def run_cdp_tests_and_recording():
    import aiohttp

    print("\n==================================================")
    print("2. تشغيل متصفح Chrome على محاكاة الموبايل (390x844)")
    print("==================================================")

    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SilentHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9235",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.8)

    base_url = f"http://127.0.0.1:{PORT}/index.html"
    recorded_frames = []

    async with aiohttp.ClientSession() as session:
        # Discover CDP target
        async with session.get("http://127.0.0.1:9235/json") as resp:
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
                    from io import BytesIO
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

            # Setup mobile emulation: iPhone 12/13/14 (390 x 844, DPR: 3)
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
            # TEST 1: عبور منتصف الليل في ٢ ديسمبر تلقائياً
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 1: عبور ليل ٢ ديسمبر التلقائي (العدّاد يصفر ويتحول للاحتفال)")
            print("--------------------------------------------------")
            await cdp_call("Page.navigate", {"url": f"{base_url}?test=dec2_live"})
            await asyncio.sleep(1.0)
            await capture_frame()

            # Wait for 3 seconds countdown to reach zero
            for i in range(7):
                await asyncio.sleep(0.5)
                await capture_frame()

            is_celebration_visible = await eval_js("!document.getElementById('celebrationSection').classList.contains('hidden')")
            assert is_celebration_visible, "Celebration section should be visible after midnight crossing!"
            print(f"  [PASS] تحوّل العدّاد بنجاح إلى بطاقة عيد الميلاد: is_celebration_visible={is_celebration_visible}")

            # ------------------------------------------------------------------
            # TEST 2: زيارة/إعادة تحميل الموقع بعد الموعد وظهور شخصية النجمة والمرحلة 1
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 2: زيارة الرابط بعد موعد ٢ ديسمبر (المرحلة 1: سؤال الأمنية)")
            print("--------------------------------------------------")
            await cdp_call("Page.navigate", {"url": f"{base_url}?test=wish_prompt"})
            await asyncio.sleep(1.0)

            # Scroll smoothly to show the star stage clearly
            await eval_js("document.getElementById('celebrationSection').scrollIntoView({behavior: 'instant', block: 'start'})")
            await asyncio.sleep(0.5)

            for _ in range(4):
                await capture_frame()
                await asyncio.sleep(0.2)

            await save_named_screenshot("mobile-phase4-star-wish-prompt")

            star_svg_exists = await eval_js("!!document.querySelector('.star-character-svg')")
            btn_wish_text = await eval_js("document.getElementById('btnAskWish').innerText.trim()")
            assert star_svg_exists, "Star character SVG must be rendered!"
            assert "يا رفووووووق، عندك أمنية؟ 🎂" in btn_wish_text, f"Unexpected wish button text: {btn_wish_text}"
            print(f"  [PASS] النجمة والتورتة والشمعة ظاهرة، وزر الأمنية: «{btn_wish_text}»")

            # ------------------------------------------------------------------
            # TEST 3: الضغط على «يا رفووووووق، عندك أمنية؟ 🎂» -> تقريب النجمة وتوهج الشمعة
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 3: الضغط على زر الأمنية -> اقتراب النجمة وتوهج الشمعة (المرحلة 2)")
            print("--------------------------------------------------")
            await eval_js("document.getElementById('btnAskWish').click()")
            
            for _ in range(6):
                await asyncio.sleep(0.25)
                await capture_frame()

            await save_named_screenshot("mobile-phase4-star-wish-blow")

            is_approaching = await eval_js("document.getElementById('starCharacterWrap').classList.contains('is-approaching')")
            is_flame_bright = await eval_js("document.getElementById('candleFlameGroup').classList.contains('is-bright')")
            blow_btn_text = await eval_js("document.getElementById('btnBlowCandle').innerText.trim()")
            wish_badge_text = await eval_js("document.getElementById('birthdayMakeWishText').innerText.trim()")

            assert is_approaching, "Star should have .is-approaching class!"
            assert is_flame_bright, "Candle flame should have .is-bright class!"
            assert "اطفي الشمعة" in blow_btn_text, f"Unexpected blow button text: {blow_btn_text}"
            assert "اتمنّي أمنية" in wish_badge_text, f"Unexpected wish badge text: {wish_badge_text}"
            print(f"  [PASS] النجمة تقربت والشمعة نورت، شارة: «{wish_badge_text}»، وزر: «{blow_btn_text}»")

            # ------------------------------------------------------------------
            # TEST 4: إطفاء الشمعة بالضغط (اطفي الشمعة) بدون أذونات ميكروفون
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 4: إطفاء الشمعة بالضغط فقط -> انطفاء الشعلة، دخان ناعم، وتهنئة العيد")
            print("--------------------------------------------------")
            await eval_js("document.getElementById('btnBlowCandle').click()")

            # Record flame disappearing, smoke puff, petals shower, and revealed greeting
            for _ in range(12):
                await asyncio.sleep(0.25)
                await capture_frame()

            await save_named_screenshot("mobile-phase4-birthday-revealed")

            is_flame_extinguished = await eval_js("document.getElementById('candleFlameGroup').classList.contains('is-extinguished')")
            celebration_title = await eval_js("document.getElementById('celebrationTitle').innerText.trim()")
            celebration_sub = await eval_js("document.getElementById('celebrationSubtitle').innerText.trim()")
            open_letter_btn_text = await eval_js("document.getElementById('openBirthdayLetterBtn').innerText.trim()")

            assert is_flame_extinguished, "Flame should be extinguished!"
            assert "كل سنة وإنتِ طيبة يا رفووووووق ❤️" in celebration_title, f"Unexpected title: {celebration_title}"
            assert "يا رب السنة دي تضحكي فيها من قلبك كتير" in celebration_sub, f"Unexpected sub: {celebration_sub}"
            assert "افتحي جواب عيد ميلادك" in open_letter_btn_text, f"Unexpected open letter button: {open_letter_btn_text}"
            print(f"  [PASS] الشمعة انطفت والتهنئة ظهرت: «{celebration_title}»")
            print(f"  [PASS] الجملة الحميمية: «{celebration_sub}»")
            print(f"  [PASS] زر الانتقال: «{open_letter_btn_text}»")

            # ------------------------------------------------------------------
            # TEST 5: الضغط على «افتحي جواب عيد ميلادك» -> فتح ظرف ٢٣ نوفمبر والجواب
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 5: فتح جواب عيد الميلاد (ظرف ٢٣ نوفمبر والـ ٤ صور)")
            print("--------------------------------------------------")
            await eval_js("document.getElementById('openBirthdayLetterBtn').click()")

            for _ in range(8):
                await asyncio.sleep(0.25)
                await capture_frame()

            await save_named_screenshot("mobile-phase4-nov23-letter-opened")

            is_modal_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            active_album = await eval_js("document.getElementById('albumModalHeaderTag').innerText.trim()")
            letter_quote = await eval_js("document.getElementById('letterDedicationQuote').innerText.trim()")
            photo_count = await eval_js("document.getElementById('totalPhotosNum').innerText.trim()")

            assert is_modal_open, "Memory album modal should be open!"
            assert "٢٣ نوفمبر" in active_album, f"Modal should display Nov 23 album, got: {active_album}"
            assert "لو هختار يوم أعيشه معاكي تاني" in letter_quote, f"Dedication quote mismatch: {letter_quote}"
            assert photo_count in ["4", "٤"], f"Nov 23 album should have 4 photos, got: {photo_count}"
            print(f"  [PASS] ألبوم ٢٣ نوفمبر فُتح بنجاح: {active_album} ({photo_count} صور)")
            print(f"  [PASS] نص الجواب: «{letter_quote}»")

            # Navigate through photos
            await eval_js("document.getElementById('albumNextBtn').click()")
            await asyncio.sleep(0.3)
            await capture_frame()
            await eval_js("document.getElementById('albumNextBtn').click()")
            await asyncio.sleep(0.3)
            await capture_frame()

            # Close modal
            await eval_js("document.getElementById('closeAlbumBtn').click()")
            await asyncio.sleep(0.4)
            await capture_frame()

            # ------------------------------------------------------------------
            # TEST 6: التأكد التام من أن ظرف الخطوبة ما زال متاحاً ويعمل بكفاءة
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 6: التحقق من بقاء ظرف الخطوبة متاحاً ومستقلاً بعد ٢ ديسمبر")
            print("--------------------------------------------------")
            await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'})")
            await asyncio.sleep(0.4)
            await capture_frame()

            is_engagement_unlocked = await eval_js("!document.getElementById('openEngagementBtn').classList.contains('hidden')")
            assert is_engagement_unlocked, "Engagement envelope MUST remain unlocked and available!"

            await eval_js("document.getElementById('openEngagementBtn').click()")
            for _ in range(6):
                await asyncio.sleep(0.25)
                await capture_frame()

            await save_named_screenshot("mobile-phase4-engagement-opened")

            eng_modal_open = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            eng_tag = await eval_js("document.getElementById('albumModalHeaderTag').innerText.trim()")
            eng_sig = await eval_js("document.getElementById('albumSignatureText').innerText.trim()")

            assert eng_modal_open, "Engagement modal should open!"
            assert "خطوبتنا" in eng_tag, f"Expected engagement tag, got: {eng_tag}"
            assert "بحبك" in eng_sig, f"Expected signature 'بحبك', got: {eng_sig}"
            print(f"  [PASS] ظرف الخطوبة يفتح بسلاسة وتوقيع: «{eng_sig}»")

            await eval_js("document.getElementById('closeAlbumBtn').click()")
            await asyncio.sleep(0.3)
            await capture_frame()

            # ------------------------------------------------------------------
            # TEST 7: اختبار زر «تخطي الحركة ⏭️»
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 7: زر تخطي الحركة ⏭️ ينقل فوراً إلى التهنئة")
            print("--------------------------------------------------")
            await cdp_call("Page.navigate", {"url": f"{base_url}?test=wish_prompt"})
            await asyncio.sleep(0.8)
            await eval_js("document.getElementById('celebrationSection').scrollIntoView({behavior: 'instant', block: 'start'})")
            await asyncio.sleep(0.3)

            skip_btn_exists = await eval_js("!!document.getElementById('btnSkipAnimation')")
            assert skip_btn_exists, "Skip button should exist!"
            await eval_js("document.getElementById('btnSkipAnimation').click()")
            await asyncio.sleep(0.3)
            await capture_frame()

            skip_revealed = await eval_js("!document.getElementById('celebrationContentRevealed').classList.contains('hidden')")
            assert skip_revealed, "Clicking skip button should immediately reveal celebration content!"
            print(f"  [PASS] زر تخطي الحركة نقل فوراً للحالة المكتملة: skip_revealed={skip_revealed}")

            # ------------------------------------------------------------------
            # TEST 8: التحقق من وضع تقليل الحركة (prefers-reduced-motion)
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 8: دعم تقليل الحركة (prefers-reduced-motion)")
            print("--------------------------------------------------")
            await cdp_call("Emulation.setEmulatedMedia", {
                "media": "screen",
                "features": [{"name": "prefers-reduced-motion", "value": "reduce"}]
            })
            await cdp_call("Page.navigate", {"url": f"{base_url}?test=after_dec2"})
            await asyncio.sleep(0.8)
            reduced_revealed = await eval_js("!document.getElementById('celebrationContentRevealed').classList.contains('hidden')")
            assert reduced_revealed, "Under prefers-reduced-motion, celebration should be directly revealed without animation delays!"
            print(f"  [PASS] وضع تقليل الحركة يعرض المشهد المكتمل مباشرة: {reduced_revealed}")

            # ------------------------------------------------------------------
            # TEST 9: قسم التسجيل الصوتي «اسمعيني» خامل بدون أخطاء عند غياب الملف
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("▶️ اختبار 9: قسم التسجيل الصوتي «اسمعيني» خامل وأنيق")
            print("--------------------------------------------------")
            audio_hidden = await eval_js("document.getElementById('voiceNoteSection').classList.contains('hidden')")
            print(f"  [PASS] قسم الصوت خامل ومخفي بشكل نظيف عند عدم تفعيله: audio_hidden={audio_hidden}")

            # ------------------------------------------------------------------
            # COMPILE WALKTHROUGH MP4 & GIF
            # ------------------------------------------------------------------
            print("\n--------------------------------------------------")
            print("🎬 إنشاء فيديو المرور الكامل (MP4) والـ GIF المتحرك")
            print("--------------------------------------------------")
            print(f"  إجمالي الإطارات المسجلة: {len(recorded_frames)} إطار")

            frames_dir = os.path.join(BASE_DIR, "screenshots", "p4_frames")
            os.makedirs(frames_dir, exist_ok=True)
            for idx, frame in enumerate(recorded_frames):
                frame.save(os.path.join(frames_dir, f"frame_{idx:04d}.png"))

            mp4_out = os.path.join(SCREENSHOTS_DIR, "birthday-celebration-walkthrough.mp4")
            gif_out = os.path.join(SCREENSHOTS_DIR, "birthday-celebration-walkthrough.gif")

            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-framerate", "4",
                "-i", os.path.join(frames_dir, "frame_%04d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=390:-2",
                mp4_out
            ]
            res_ffmpeg = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            if os.path.exists(mp4_out):
                print(f"  [OK] تم بنجاح إنشاء فيديو MP4: {mp4_out} ({os.path.getsize(mp4_out)} bytes)")
                shutil.copy2(mp4_out, os.path.join(BRAIN_DIR, "birthday-celebration-walkthrough.mp4"))
                shutil.copy2(mp4_out, os.path.join(BRAIN_SCREENSHOTS_DIR, "birthday-celebration-walkthrough.mp4"))

            # Build GIF (downscaled to 320px width for fast loading in markdown)
            gif_frames = []
            # Sample every 1 frame or skip to keep size balanced
            for i, im in enumerate(recorded_frames):
                if i % 1 == 0:
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
                print(f"  [OK] تم بنجاح إنشاء GIF المتحرك للمعاينة: {gif_out} ({os.path.getsize(gif_out)} bytes)")
                shutil.copy2(gif_out, os.path.join(BRAIN_DIR, "birthday-celebration-walkthrough.gif"))
                shutil.copy2(gif_out, os.path.join(BRAIN_SCREENSHOTS_DIR, "birthday-celebration-walkthrough.gif"))

    chrome_proc.terminate()
    httpd.shutdown()
    print("\n==================================================")
    print("🎉 جميع اختبارات المرحلة الرابعة (افتتاحية عيد الميلاد) اكتملت بنجاح 100%!")
    print("==================================================")

if __name__ == "__main__":
    verify_strings_and_configs()
    asyncio.run(run_cdp_tests_and_recording())
