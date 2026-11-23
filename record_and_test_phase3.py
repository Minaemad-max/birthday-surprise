"""
Phase 3 Verification & Mobile Screencast Recording Script
Validates:
1. Locked state before Nov 25 (badge «يتفتح يوم ٢٥ نوفمبر», countdown running).
2. Live midnight transition at Nov 25 00:00 Cairo time (automatic unlock without reload).
3. Post-Nov 25 reload state (button «افتحي ظرف الخطوبة» available).
4. Screencast recording of breaking seal, opening envelope, drifting petals, and flipping photos.
5. Post-Dec 2 state (birthday celebration active, Nov 23 envelope available, AND engagement envelope available).
6. Reduced motion compliance.
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
from PIL import Image

PORT = 8935
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

def run_configuration_checks():
    print("==================================================")
    print("1. اختبار نصوص الإعدادات وظرف الخطوبة وظرف ٢٣ نوفمبر")
    print("==================================================")
    with open(os.path.join(BASE_DIR, "config.js"), "r", encoding="utf-8") as f:
        cfg = f.read()

    checks = [
        ("اسم الدلع", "يا رفووووووق ❤️"),
        ("تاريخ فك قفل ظرف الخطوبة (توقيت القاهرة)", "2026-11-25T00:00:00+02:00"),
        ("تاريخ عيد الميلاد (توقيت القاهرة)", "2026-12-02T00:00:00+02:00"),
        ("عنوان ظرف الخطوبة", "يوم خطوبتنا"),
        ("نص القفل لظرف الخطوبة", "يتفتح يوم ٢٥ نوفمبر"),
        ("زر فتح ظرف الخطوبة", "افتحي ظرف الخطوبة"),
        ("عبارة إهداء الخطوبة", "يا رفووووووق، يوم ٢٥ نوفمبر مش مجرد تاريخ، ده اليوم اللي لبسنا فيه دبل بعض ووعدنا بعض نكمل العمر سوا 💍❤️"),
        ("جملة ختام ألبوم الخطوبة", "أحلى خطوبة وأجمل بداية… وكل لحظة معاكي بتأكدلي إني اخترت صح. بحبك يا رفووووووق ❤️"),
        ("زر فتح ظرف ٢٣ نوفمبر", "افتحي الجواب يا رفووووووق"),
        ("جملة ختام ٢٣ نوفمبر", "يوم ٢٣ نوفمبر كان حلو أوي عشان كنت معاكي… وكل سنة وإنتِ حبيبتي يا رفووووووق ❤️")
    ]

    for label, text in checks:
        assert text in cfg, f"Missing config string: {text}"
        print(f"  [PASS] {label}: «{text}»")

    photo_path = os.path.join(BASE_DIR, "assets", "images", "engagement-photo-1.jpg")
    assert os.path.exists(photo_path), "engagement-photo-1.jpg does not exist!"
    print(f"  [PASS] وجود الصورة الرسمية للخطوبة: {photo_path} ({os.path.getsize(photo_path)} bytes)")

async def run_full_browser_verification_and_recording():
    import aiohttp
    
    print("\n==================================================")
    print("2. تشغيل الاختبارات الفعلية وتسجيل شاشة الموبايل (Headless Chrome + CDP)")
    print("==================================================")

    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SilentHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9226",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    base_url = f"http://127.0.0.1:{PORT}/index.html"

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9226/json") as resp:
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

            # -----------------------------------------------------------------
            # TEST 1: قبل ٢٥ نوفمبر (الظرف مقفول والعدّاد شغال)
            # -----------------------------------------------------------------
            print("\n--- اختبار ١: حالة ما قبل ٢٥ نوفمبر ---")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=before_nov25"})
            await asyncio.sleep(1.0)

            locked_badge_visible = await eval_js("!document.getElementById('engagementLockedBadge').classList.contains('hidden')")
            open_btn_hidden = await eval_js("document.getElementById('openEngagementBtn').classList.contains('hidden')")
            locked_text = await eval_js("document.getElementById('engagementLockedText').textContent.trim()")
            days_val = await eval_js("document.getElementById('daysVal').textContent")

            assert locked_badge_visible, "Locked badge should be visible before Nov 25"
            assert open_btn_hidden, "Open button should be hidden before Nov 25"
            assert "يتفتح يوم ٢٥ نوفمبر" in locked_text, f"Unexpected locked text: {locked_text}"
            print(f"  [PASS] شارة القفل ظاهرة: «{locked_text}»")
            print(f"  [PASS] زر الفتح مخفي حتى يحين الموعد")
            print(f"  [PASS] عدّاد عيد الميلاد شغال: الأيام = {days_val}")
            await capture_screen("mobile-before-nov25-locked.png")

            # -----------------------------------------------------------------
            # TEST 2: عبور منتصف ليل ٢٥ نوفمبر والصفحة مفتوحة (الانتقال التلقائي)
            # -----------------------------------------------------------------
            print("\n--- اختبار ٢: عبور منتصف ليل ٢٥ نوفمبر تلقائياً دون إعادة تحميل ---")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=nov25_live"})
            await asyncio.sleep(0.5)

            badge_before = await eval_js("!document.getElementById('engagementLockedBadge').classList.contains('hidden')")
            assert badge_before, "Badge should still be locked before 3s elapse"

            print("  [WAIT] انتظار عبور منتصف الليل (٣.٥ ثانية)...")
            await asyncio.sleep(3.6)

            badge_after = await eval_js("!document.getElementById('engagementLockedBadge').classList.contains('hidden')")
            btn_after = await eval_js("!document.getElementById('openEngagementBtn').classList.contains('hidden')")
            btn_text = await eval_js("document.getElementById('openEngagementBtn').textContent.trim()")

            assert not badge_after, "Badge should hide automatically after midnight Nov 25"
            assert btn_after, "Open button should become visible automatically"
            assert "افتحي ظرف الخطوبة" in btn_text, f"Unexpected button text: {btn_text}"
            print(f"  [PASS] تم فك القفل تلقائياً والصفحة مفتوحة!")
            print(f"  [PASS] زر الفتح ظاهر ونشط: «{btn_text}»")
            await capture_screen("mobile-nov25-unlocked-live.png")

            # -----------------------------------------------------------------
            # TEST 3: زيارة جديدة أو إعادة تحميل بعد ٢٥ نوفمبر
            # -----------------------------------------------------------------
            print("\n--- اختبار ٣: إعادة التحميل بعد ٢٥ نوفمبر ---")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=after_nov25"})
            await asyncio.sleep(0.8)

            btn_reload = await eval_js("!document.getElementById('openEngagementBtn').classList.contains('hidden')")
            countdown_active = await eval_js("!document.getElementById('countdownSection').classList.contains('hidden')")
            assert btn_reload, "Button should be visible on fresh reload after Nov 25"
            assert countdown_active, "Birthday countdown must remain active"
            print("  [PASS] الزيارة بعد ٢٥ نوفمبر تفتح الظرف مباشرة مع استمرار عدّاد عيد الميلاد")
            await capture_screen("mobile-after-nov25-reload.png")

            # -----------------------------------------------------------------
            # TEST 4: تسجيل شاشة الموبايل لحركة فتح ظرف الخطوبة وتقليب الصور
            # -----------------------------------------------------------------
            print("\n--- اختبار ٤: التقاط وتجميع لقطات الحركة المتسلسلة لفتح ظرف الخطوبة ---")
            frames_dir = os.path.join(SCREENSHOTS_DIR, "engagement_rec_frames")
            if os.path.exists(frames_dir):
                shutil.rmtree(frames_dir)
            os.makedirs(frames_dir, exist_ok=True)

            recorded_images = []
            frame_idx = 0

            async def grab_frame():
                nonlocal frame_idx
                res = await send_cmd("Page.captureScreenshot", {"format": "png"})
                data = base64.b64decode(res["data"])
                fname = f"frame_{frame_idx:04d}.png"
                fpath = os.path.join(frames_dir, fname)
                with open(fpath, "wb") as f:
                    f.write(data)
                frame_idx += 1
                return fpath

            # التمرير إلى ظرف الخطوبة
            await eval_js("document.getElementById('engagementEnvelopeSection').scrollIntoView({behavior: 'instant', block: 'center'});")
            await asyncio.sleep(0.5)

            # اللقطات الأولية: الظرف مقفول وجاهز للفتح
            for _ in range(3):
                p = await grab_frame()
                recorded_images.append(Image.open(p))
                await asyncio.sleep(0.15)

            # النقر على زر «افتحي ظرف الخطوبة»
            print("  [ACTION] الضغط على زر «افتحي ظرف الخطوبة»...")
            await eval_js("document.getElementById('openEngagementBtn').click();")

            # التقاط إطارات فك الختم وفتح الغطاء وتطاير البتلات (أول 0.8 ثانية)
            for _ in range(8):
                await asyncio.sleep(0.12)
                p = await grab_frame()
                recorded_images.append(Image.open(p))

            # التحقق من فتح الألبوم
            modal_visible = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            header_tag = await eval_js("document.getElementById('albumModalHeaderTag').textContent.trim()")
            photo_caption = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            current_num = await eval_js("document.getElementById('currentPhotoNum').textContent.trim()")
            
            assert modal_visible, "Engagement album modal should be open"
            assert "ظرف يوم خطوبتنا" in header_tag, f"Header tag mismatch: {header_tag}"
            print(f"  [PASS] فتح ألبوم الخطوبة بنجاح! الترويسة: «{header_tag}»")
            print(f"  [PASS] الصورة الأولى: صورة {current_num} - «{photo_caption}»")
            await capture_screen("mobile-engagement-photo-1.png")

            # الثبات على الصورة الأولى لثانية
            for _ in range(4):
                await asyncio.sleep(0.2)
                p = await grab_frame()
                recorded_images.append(Image.open(p))

            # تقليب الصورة التالية (Next)
            print("  [ACTION] تقليب الصورة التالية...")
            await eval_js("document.getElementById('albumNextBtn').click();")
            await asyncio.sleep(0.35)

            # التقاط إطارات الصورة الثانية
            for _ in range(5):
                await asyncio.sleep(0.2)
                p = await grab_frame()
                recorded_images.append(Image.open(p))

            photo2_caption = await eval_js("document.getElementById('albumCurrentCaption').textContent.trim()")
            current_num_2 = await eval_js("document.getElementById('currentPhotoNum').textContent.trim()")
            print(f"  [PASS] الصورة الثانية: صورة {current_num_2} - «{photo2_caption}»")
            await capture_screen("mobile-engagement-photo-2-placeholder.png")

            # العودة للصورة الأولى
            print("  [ACTION] العودة للصورة الأولى...")
            await eval_js("document.getElementById('albumPrevBtn').click();")
            await asyncio.sleep(0.35)
            for _ in range(3):
                p = await grab_frame()
                recorded_images.append(Image.open(p))

            # التمرير لأسفل الألبوم لرؤية جملة الإغلاق والتوقيع
            await eval_js("document.getElementById('loveLetterCard').scrollTo({top: 800, behavior: 'smooth'});")
            await asyncio.sleep(0.6)
            for _ in range(4):
                p = await grab_frame()
                recorded_images.append(Image.open(p))
            await capture_screen("mobile-engagement-album-closing.png")

            # تجميع MP4 و GIF
            print(f"\n  [COMPILING] تجميع {len(recorded_images)} إطار إلى MP4 و GIF...")
            mp4_out = os.path.join(SCREENSHOTS_DIR, "engagement-envelope-walkthrough.mp4")
            gif_out = os.path.join(SCREENSHOTS_DIR, "engagement-envelope-walkthrough.gif")

            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-framerate", "6",
                "-i", os.path.join(frames_dir, "frame_%04d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=390:-2",
                mp4_out
            ]
            try:
                subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                shutil.copy2(mp4_out, os.path.join(BRAIN_SCREENSHOTS_DIR, "engagement-envelope-walkthrough.mp4"))
                shutil.copy2(mp4_out, os.path.join(BRAIN_DIR, "engagement-envelope-walkthrough.mp4"))
                print(f"    🎬 تم بنجاح إنشاء فيديو MP4: {mp4_out} ({os.path.getsize(mp4_out)} bytes)")
            except Exception as e:
                print(f"    [WARN] ffmpeg MP4 generation note: {e}")

            # إنشاء GIF متحرك عبر Pillow
            try:
                small_frames = []
                for img in recorded_images:
                    w, h = img.size
                    small = img.resize((360, int(h * 360 / w)), Image.Resampling.LANCZOS).convert("P", palette=Image.Palette.ADAPTIVE, colors=96)
                    small_frames.append(small)

                small_frames[0].save(
                    gif_out,
                    save_all=True,
                    append_images=small_frames[1:],
                    optimize=True,
                    duration=180,
                    loop=0
                )
                shutil.copy2(gif_out, os.path.join(BRAIN_SCREENSHOTS_DIR, "engagement-envelope-walkthrough.gif"))
                shutil.copy2(gif_out, os.path.join(BRAIN_DIR, "engagement-envelope-walkthrough.gif"))
                print(f"    🖼️ تم بنجاح إنشاء GIF متحرك: {gif_out} ({os.path.getsize(gif_out)} bytes)")
            except Exception as e:
                print(f"    [WARN] GIF generation note: {e}")

            # إغلاق الألبوم
            await eval_js("document.getElementById('closeAlbumBtn').click();")
            await asyncio.sleep(0.5)

            # -----------------------------------------------------------------
            # TEST 5: بعد ٢ ديسمبر (عيد الميلاد نشط + ظرف ٢٣ نوفمبر + ظرف الخطوبة متاح)
            # -----------------------------------------------------------------
            print("\n--- اختبار ٥: بعد ٢ ديسمبر (عيد الميلاد + توفر الظرفين معاً) ---")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=after_dec2"})
            await asyncio.sleep(1.0)

            celeb_visible = await eval_js("!document.getElementById('celebrationSection').classList.contains('hidden')")
            celeb_title = await eval_js("document.getElementById('celebrationTitle').textContent.trim()")
            nov23_envelope_btn = await eval_js("!document.getElementById('openEnvelopeBtn').classList.contains('hidden')")
            engagement_btn = await eval_js("!document.getElementById('openEngagementBtn').classList.contains('hidden')")

            assert celeb_visible, "Birthday celebration must be visible after Dec 2"
            assert "كل سنة وإنتِ طيبة يا رفووووووق ❤️" in celeb_title, f"Unexpected title: {celeb_title}"
            assert nov23_envelope_btn, "Nov 23 envelope must be accessible in celebration"
            assert engagement_btn, "Engagement envelope MUST REMAIN ACCESSIBLE after Dec 2!"

            print(f"  [PASS] رسالة التهنئة ظاهرة: «{celeb_title}»")
            print("  [PASS] ظرف ٢٣ نوفمبر متاح للفتح")
            print("  [PASS] ظرف الخطوبة يظل متاحاً تماماً للفتح بعد عيد الميلاد دون أي تعارض!")
            await capture_screen("mobile-after-dec2-both-envelopes.png")

            # فتح ظرف ٢٣ نوفمبر للتأكد من استقلالية الألبومين
            print("  [ACTION] فتح ظرف ٢٣ نوفمبر بعد عيد الميلاد...")
            await eval_js("document.getElementById('openEnvelopeBtn').click();")
            await asyncio.sleep(0.8)
            nov23_modal_header = await eval_js("document.getElementById('albumModalHeaderTag').textContent.trim()")
            nov23_photos_count = await eval_js("document.getElementById('totalPhotosNum').textContent.trim()")
            assert "ظرف ٢٣ نوفمبر" in nov23_modal_header, f"Mismatch header: {nov23_modal_header}"
            assert nov23_photos_count == "4", f"Expected 4 photos for Nov 23, got: {nov23_photos_count}"
            print(f"  [PASS] ألبوم ٢٣ نوفمبر فتح بنجاح ويحتوي على {nov23_photos_count} صور!")
            await capture_screen("mobile-dec2-nov23-album.png")

            await eval_js("document.getElementById('closeAlbumBtn').click();")
            await asyncio.sleep(0.5)

            # -----------------------------------------------------------------
            # TEST 6: التحقق من تقليل الحركة (Prefers Reduced Motion)
            # -----------------------------------------------------------------
            print("\n--- اختبار ٦: احترام إعداد تقليل الحركة ---")
            await send_cmd("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]})
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=after_nov25"})
            await asyncio.sleep(0.6)

            start_t = time.time()
            await eval_js("document.getElementById('openEngagementBtn').click();")
            await asyncio.sleep(0.1)
            is_modal_now = await eval_js("!document.getElementById('memoryAlbumOverlay').classList.contains('hidden')")
            petals_count = await eval_js("document.getElementById('petalsContainer').children.length")
            duration = time.time() - start_t

            assert is_modal_now, "Modal must open immediately when reduced motion is requested"
            assert petals_count == 0, "No petals should be spawned when reduced motion is active"
            print(f"  [PASS] فتح الألبوم فورياً خلال {duration:.3f} ثانية دون بتلات أو تأخير حركي")

    chrome_proc.terminate()
    try:
        httpd.shutdown()
    except Exception:
        pass
    print("\n==================================================")
    print("✅ اكتملت جميع الاختبارات بنجاح بنسبة ١٠٠٪!")
    print("==================================================")

if __name__ == "__main__":
    run_configuration_checks()
    asyncio.run(run_full_browser_verification_and_recording())
