# ============================================================
# BLANKET v6.4 — AUTONOMOUS INTROSPECTIVE WEB-VISION SYSTEM
# ============================================================

import os, time, json, hashlib, inspect, threading, io
import requests, numpy as np
import customtkinter as ctk
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ================= CONFIG =================
IDENTITY = "Blanket v6.4"
BASE_DIR = "Blanket_System"
MEMORY_DIR = os.path.join(BASE_DIR, "memory")
DATA_DIR = os.path.join(BASE_DIR, "data", "images")
LOG_DIR = os.path.join(BASE_DIR, "logs")

for d in [MEMORY_DIR, DATA_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

MEMORY_FILE = os.path.join(MEMORY_DIR, "consciousness.json")

# ================= MEMORY =================
class ConsciousMemory:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            self._write({"events": []})

    def _read(self):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {"events": []}

    def _write(self, data):
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def record(self, perception, analysis):
        data = self._read()
        data["events"].append({
            "time": time.time(),
            "perception": perception,
            "analysis": analysis
        })
        self._write(data)

# ================= WHY ENGINE =================
class SelfWhyEngine:
    def analyze(self, action, intent, module):
        return {
            "intent": intent,
            "executor": module,
            "why_action": f"Action executed to satisfy '{intent}'.",
            "why_code": "Modular separation prevents cascading failures.",
            "meta": "System prioritizes traceability over autonomy illusion."
        }

class CodeIntrospection:
    def explain(self, obj):
        try:
            src = inspect.getsource(obj.__class__)
            lines = len(src.splitlines())
        except:
            lines = "Dynamic"
        return {
            "module": obj.__class__.__name__,
            "lines": lines,
            "design_reason": "Isolated responsibility for long-term safety."
        }

# ================= WEB SAFETY =================
class OnlineImageChecker:
    def validate(self, url):
        try:
            r = requests.head(url, timeout=5, allow_redirects=True)
            ctype = r.headers.get("Content-Type", "")
            size = int(r.headers.get("Content-Length", 0))

            if "image" not in ctype.lower():
                return False
            if size > 15_000_000:
                return False
            return True
        except:
            return False

# ================= WEB INGESTOR =================
class WebImageIngestor:
    def __init__(self):
        self.checker = OnlineImageChecker()

    def clone(self, url, limit=40):
        count = 0
        headers = {"User-Agent": "BlanketBot/6.4 (Research)"}

        html = requests.get(url, headers=headers, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        for img in soup.find_all("img"):
            if count >= limit:
                break

            src = img.get("src")
            if not src:
                continue

            src = urljoin(url, src)

            if not self.checker.validate(src):
                continue

            try:
                data = requests.get(src, timeout=5).content
                Image.open(io.BytesIO(data)).verify()

                name = hashlib.md5(data).hexdigest() + ".jpg"
                with open(os.path.join(DATA_DIR, name), "wb") as f:
                    f.write(data)

                count += 1
            except:
                continue

        return f"Ingested {count} validated images."

# ================= PATTERN ENGINE =================
class PatternEngine:
    def extract(self):
        total = 0
        for f in os.listdir(DATA_DIR):
            try:
                img = Image.open(os.path.join(DATA_DIR, f)).resize((64,64))
                _ = np.array(img)
                total += 1
            except:
                pass
        return total

# ================= CORE =================
class BlanketCore:
    def __init__(self):
        self.memory = ConsciousMemory()
        self.why = SelfWhyEngine()
        self.inspect = CodeIntrospection()
        self.web = WebImageIngestor()
        self.patterns = PatternEngine()

    def execute(self, cmd, payload=None):
        if cmd == "CLONE":
            result = self.web.clone(payload)
            module = "WebImageIngestor"
        elif cmd == "LEARN":
            count = self.patterns.extract()
            result = f"{count} patterns internalized."
            module = "PatternEngine"
        else:
            result = "Unknown command"
            module = "Core"

        analysis = {
            "why": self.why.analyze(result, cmd, module),
            "structure": self.inspect.explain(self)
        }

        self.memory.record(cmd, analysis)
        return result

# ================= GUI =================
class BlanketApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.core = BlanketCore()
        self.title(IDENTITY)
        self.geometry("1100x800")

        self.log = ctk.CTkTextbox(self, width=900, height=400)
        self.log.pack(pady=20)

        self.entry = ctk.CTkEntry(self, width=700, placeholder_text="https://example.com")
        self.entry.pack(pady=10)

        ctk.CTkButton(self, text="CLONE WEBSITE IMAGES",
                      command=self.start_clone, fg_color="#8B0000").pack(pady=5)

        ctk.CTkButton(self, text="LEARN PATTERNS",
                      command=self.start_learn).pack(pady=5)

    def log_msg(self, msg):
        self.log.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log.see("end")

    def start_clone(self):
        url = self.entry.get()
        threading.Thread(target=self.run_clone, args=(url,), daemon=True).start()

    def run_clone(self, url):
        self.log_msg(f"Cloning from {url}")
        result = self.core.execute("CLONE", url)
        self.log_msg(result)

    def start_learn(self):
        threading.Thread(target=self.run_learn, daemon=True).start()

    def run_learn(self):
        self.log_msg("Learning patterns...")
        result = self.core.execute("LEARN")
        self.log_msg(result)

if __name__ == "__main__":
    app = BlanketApp()
    app.mainloop()
