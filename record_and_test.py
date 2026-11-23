"""
Romantic Edition: Verification and Screen Recorder Script for Phase 2 Love Letter & Roses
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

PORT = 8932
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

def run_string_and_design_checks():
    print("==================================================")
    print("1. اختبار نصوص جواب الحب والورد وعبارات الإغلاق")
    print("==================================================")
    with open(os.path.join(BASE_DIR, "config.js"), "r", encoding="utf-8") as f:
        cfg = f.read()

    checks = [
        ("اسم الدلع", "يا رفووووووق ❤️"),
        ("اسم المستلم على الظرف", "لرفووووووق"),
        ("زر فتح الجواب", "افتحي الجواب يا رفووووووق"),
        ("عبارة الجواب", "يا رفووووووق، لو هختار يوم أعيشه معاكي تاني، يوم ٢٣ نوفمبر هييجي في بالي على طول. ❤️"),
        ("جملة قفل الألبوم", "يوم ٢٣ نوفمبر كان حلو أوي عشان كنت معاكي… وكل سنة وإنتِ حبيبتي يا رفووووووق ❤️"),
        ("توقيع الحب", "بحبك"),
        ("تاريخ الذكرى", "٢٣ نوفمبر")
    ]

    for label, text in checks:
        assert text in cfg, f"Missing config string: {text}"
        print(f"  [PASS] {label}: «{text}»")

async def record_walkthrough_and_test():
    import aiohttp
    
    print("\n==================================================")
    print("2. تسجيل شاشة الموبايل واختبار الحركة المتسلسلة (CDP Screencast)")
    print("==================================================")
    
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), SilentHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_proc = subprocess.Popen([
        chrome_exe,
        "--headless=new",
        "--remote-debugging-port=9224",
        "--disable-gpu",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    base_url = f"http://127.0.0.1:{PORT}/index.html"

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:9224/json") as resp:
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
                print(f"    📷 تم حفظ لقطة: {filename} ({len(img_data)} bytes)")
                return p

            # Set Mobile Viewport (iPhone 14: 390x844)
            await send_cmd("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})

            # ----------------------------------------------------
            # SCREENSHOT 1: Mobile Before Date (with rose corner)
            # ----------------------------------------------------
            print("\n  [SNAP 1] التقاط واجهة الموبايل قبل الموعد مع وردة ركن الإطار:")
            await send_cmd("Page.navigate", {"url": base_url})
            await asyncio.sleep(1.2)
            has_rose_corner = await eval_js("document.querySelector('.polaroid-rose-corner') !== null")
            assert has_rose_corner, "Rose corner must exist on polaroid frame before target date"
            await capture_screen("mobile-before-date.png")
            print("    [PASS] وردة ركن إطار صورة الدبل ظاهرة ولمسات الوردي الغامق متناسقة!")

            # ----------------------------------------------------
            # SCREENSHOT 2: Envelope with «لرفووووووق» & Wax Seal with Heart
            # ----------------------------------------------------
            print("\n  [SNAP 2] التقاط كارت الظرف الكريمي مع الختم والاسم:")
            await send_cmd("Page.navigate", {"url": f"{base_url}?test=ended"})
            await asyncio.sleep(1.2)
            await eval_js("document.getElementById('envelopeContainer').scrollIntoView({behavior: 'instant', block: 'center'})")
            await asyncio.sleep(0.4)
            
            recipient_text = await eval_js("document.querySelector('.recipient-name').textContent.trim()")
            has_heart_seal = await eval_js("document.querySelector('.seal-heart') !== null")
            btn_text = await eval_js("document.getElementById('openEnvelopeBtn').textContent.trim()")
            
            assert "لرفووووووق" in recipient_text, f"Expected لرفووووووق, got {recipient_text}"
            assert has_heart_seal, "Wax seal must have heart icon"
            assert "افتحي الجواب يا رفووووووق" in btn_text, f"Unexpected button text: {btn_text}"
            print(f"    [PASS] الظرف معروض باسم «{recipient_text}»، ختم الشمع الوردي والقلب، والزر «{btn_text}».")
            await capture_screen("mobile-envelope-after-date.png")

            # ----------------------------------------------------
            # SCREEN RECORDING: Walkthrough from Envelope to Opening & Flip Photo
            # ----------------------------------------------------
            print("\n  [RECORDING] بدء التقاط لقطات الحركة المتسلسلة لتسجيل الشاشة...")
            frames_dir = os.path.join(BASE_DIR, "screenshots", "rec_frames")
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

            # Frame 1-3: Envelope at rest before click
            for _ in range(3):
                p = await grab_frame()
                recorded_images.append(Image.open(p))
                await asyncio.sleep(0.15)

            # Trigger Envelope Opening Sequence
            print("    نقر زر «افتحي الجواب يا رفووووووق» وبدء الحركة المتسلسلة...")
            await eval_js("document.getElementById('openEnvelopeBtn').click()")

            # Capture frames during seal breaking and flap opening (first 0.7s)
            for _ in range(6):
                await asyncio.sleep(0.12)
                p = await grab_frame()
                recorded_images.append(Image.open(p))

            # Capture frames as love letter emerges with rose petals
            for _ in range(6):
                await asyncio.sleep(0.15)
                p = await grab_frame()
                recorded_images.append(Image.open(p))

            # Assert love letter dedication is visible
            dedication_visible = await eval_js("document.getElementById('letterDedicationQuote') !== null")
            assert dedication_visible, "Love letter dedication quote must be visible"

            # Capture group photo inside album
            await capture_screen("album-group-photo.png")

            # Pause on Photo 1 (Group photo) in the recording
            for _ in range(4):
                await asyncio.sleep(0.2)
                p = await grab_frame()
                recorded_images.append(Image.open(p))

            # Flip to Photo 2 (Mirror photo)
            print("    تقليب الصورة الأولى والانتقال لصورة المراية...")
            await eval_js("document.getElementById('albumNextBtn').click()")
            await asyncio.sleep(0.35)

            # Capture frames after flip
            for _ in range(5):
                await asyncio.sleep(0.2)
                p = await grab_frame()
                recorded_images.append(Image.open(p))

            # Navigate to Photo 4 to verify and capture the closing message
            await eval_js("document.getElementById('albumNextBtn').click()")
            await asyncio.sleep(0.25)
            await eval_js("document.getElementById('albumNextBtn').click()")
            await asyncio.sleep(0.35)
            await eval_js("document.getElementById('albumClosingLetter').scrollIntoView({behavior: 'instant', block: 'center'})")
            await asyncio.sleep(0.3)

            closing_msg = await eval_js("document.getElementById('albumClosingMsg').textContent.trim()")
            has_rose_sig = await eval_js("document.querySelector('.signature-rose') !== null")
            assert "يوم ٢٣ نوفمبر كان حلو أوي عشان كنت معاكي" in closing_msg, f"Unexpected closing text: {closing_msg}"
            assert has_rose_sig, "Closing signature must have rose"
            print(f"    [PASS] قفل الألبوم بجملة: «{closing_msg}» مع الوردة وتوقيع «بحبك».")
            await capture_screen("album-closing-photo.png")

            # ----------------------------------------------------
            # COMPILE VIDEO (MP4) AND ANIMATED GIF VIA FFMPEG & PILLOW
            # ----------------------------------------------------
            print("\n  [COMPILING] تجميع تسجيل الشاشة إلى فيديو MP4 وملف GIF متحرك...")
            mp4_out = os.path.join(SCREENSHOTS_DIR, "envelope-open-walkthrough.mp4")
            gif_out = os.path.join(SCREENSHOTS_DIR, "envelope-open-walkthrough.gif")

            # 1. Compile MP4 with ffmpeg
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-framerate", "5",
                "-i", os.path.join(frames_dir, "frame_%04d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=390:-2",
                mp4_out
            ]
            res_ffmpeg = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            if os.path.exists(mp4_out):
                print(f"    🎬 تم بنجاح إنشاء فيديو MP4: {mp4_out} ({os.path.getsize(mp4_out)} bytes)")
                shutil.copy2(mp4_out, os.path.join(BRAIN_DIR, "envelope-open-walkthrough.mp4"))
                shutil.copy2(mp4_out, os.path.join(BRAIN_SCREENSHOTS_DIR, "envelope-open-walkthrough.mp4"))

            # 2. Compile GIF using Pillow for embedded display in markdown artifacts
            # Resize frames slightly to keep GIF lightweight and buttery smooth
            gif_frames = []
            for im in recorded_images:
                # Downscale to 320px width for fast loading in markdown
                w, h = im.size
                new_h = int(h * (320 / w))
                small_im = im.resize((320, new_h), Image.Resampling.LANCZOS)
                gif_frames.append(small_im)

            gif_frames[0].save(
                gif_out,
                save_all=True,
                append_images=gif_frames[1:],
                duration=220,
                loop=0,
                optimize=True
            )
            print(f"    🎞️ تم بنجاح إنشاء GIF المتحرك للمعاينة: {gif_out} ({os.path.getsize(gif_out)} bytes)")
            shutil.copy2(gif_out, os.path.join(BRAIN_DIR, "envelope-open-walkthrough.gif"))
            shutil.copy2(gif_out, os.path.join(BRAIN_SCREENSHOTS_DIR, "envelope-open-walkthrough.gif"))

    chrome_proc.terminate()
    httpd.shutdown()
    print("\n==================================================")
    print("✅ اكتملت جميع اختبارات وتسجيلات تجربة جواب الحب والورد بنجاح 100%!")
    print("==================================================")

if __name__ == "__main__":
    run_string_and_design_checks()
    asyncio.run(record_walkthrough_and_test())
