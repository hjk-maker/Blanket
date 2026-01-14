# ============================================================
# ROBOTS.TXT GENERATOR FOR BLANKET SYSTEM
# ============================================================

ROBOTS_TXT = """# Robots.txt for Blanket System (Research & Demo)
# Generated automatically

User-agent: *
Disallow: /Blanket_System/data/
Disallow: /Blanket_System/memory/
Disallow: /Blanket_System/logs/

Allow: /

# BlanketBot identification
User-agent: BlanketBot
Crawl-delay: 10

# Transparency:
# This project performs image ingestion ONLY for research,
# respects size limits, validation, and site policies.
"""

with open("robots.txt", "w") as f:
    f.write(ROBOTS_TXT)

print("robots.txt generated successfully.")
