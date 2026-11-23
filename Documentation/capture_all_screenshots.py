"""
Cipher Aegis - Capture Full Dashboard Screenshots via Chrome DevTools Protocol (CDP)
"""

import sys
import os
import json
import base64
import time
import urllib.request
import asyncio
from tornado import websocket, ioloop

OUTPUT_DIR = "/Users/praisydevamahimaij/Downloads/AIORI_PS001/Documentation/Screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGES = [
    (1, "dashboard_page01_overview.png"),
    (2, "dashboard_page02_dataset_explorer.png"),
    (3, "dashboard_page03_behavioural_analysis.png"),
    (4, "dashboard_page04_detection_centre.png"),
    (5, "dashboard_page05_model_performance.png"),
    (6, "dashboard_page06_detection_delay.png"),
    (7, "dashboard_page07_benign_activity.png"),
    (8, "dashboard_page08_simulation_testing.png"),
    (9, "dashboard_page09_reports_export.png"),
    (10, "dashboard_page10_about.png"),
]

async def capture_dashboard_pages():
    for page_num, filename in PAGES:
        url = f"http://localhost:8501/?page={page_num}"
        out_path = os.path.join(OUTPUT_DIR, filename)
        print(f"[*] Navigating to Page {page_num} ({url})...")
        
        try:
            req = urllib.request.Request("http://localhost:9222/json/new", method="PUT")
            res = urllib.request.urlopen(req)
            page_info = json.loads(res.read().decode())
            ws_url = page_info["webSocketDebuggerUrl"]
            page_id = page_info["id"]

            ws = await websocket.websocket_connect(ws_url)
            
            # Set viewport to standard high-res desktop
            await ws.write_message(json.dumps({
                "id": 1,
                "method": "Emulation.setDeviceMetricsOverride",
                "params": {
                    "width": 1600,
                    "height": 1100,
                    "deviceScaleFactor": 1,
                    "mobile": False
                }
            }))
            await ws.read_message()

            await ws.write_message(json.dumps({"id": 2, "method": "Page.enable"}))
            await ws.read_message()

            await ws.write_message(json.dumps({"id": 3, "method": "Page.navigate", "params": {"url": url}}))
            await ws.read_message()

            # Wait for Streamlit WebSocket to render complete data & charts
            await asyncio.sleep(4.5)

            # Capture full page screenshot
            await ws.write_message(json.dumps({
                "id": 4,
                "method": "Page.captureScreenshot",
                "params": {"format": "png", "captureBeyondViewport": False}
            }))

            while True:
                msg = await ws.read_message()
                data = json.loads(msg)
                if data.get("id") == 4:
                    img_data = base64.b64decode(data["result"]["data"])
                    with open(out_path, "wb") as f:
                        f.write(img_data)
                    print(f"    [+] Saved: {filename} ({len(img_data):,} bytes)")
                    break

            ws.close()
            try:
                close_req = urllib.request.Request(f"http://localhost:9222/json/close/{page_id}", method="PUT")
                urllib.request.urlopen(close_req)
            except Exception:
                pass
        except Exception as e:
            print(f"    [-] Error capturing Page {page_num}: {e}")

if __name__ == "__main__":
    ioloop.IOLoop.current().run_sync(capture_dashboard_pages)
    print("\n[+] All dashboard screenshots process finished.")
