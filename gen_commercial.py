import os

BASE = "C:/Users/Mo_Tsai/Desktop/Google Drive/自動化測試資料夾/ONwebsite"

CSS = """<style>
  :root {
    --bg: #0e0e0c; --bg2: #141412; --bg3: #1a1a17;
    --line: #252520; --white: #f0efe8;
    --muted: #4a4a44; --dim: #2a2a26; --accent: #666660;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background: var(--bg); color: var(--white); }
  .nav { display: flex; align-items: center; justify-content: space-between; padding: 20px 40px; border-bottom: 0.5px solid var(--line); position: sticky; top: 0; background: var(--bg); z-index: 100; }
  .nav-logo { font-size: 10px; font-weight: 300; letter-spacing: 0.26em; text-transform: uppercase; color: var(--white); text-decoration: none; }
  .nav-links { display: flex; gap: 28px; }
  .nav-link { font-size: 9px; font-weight: 300; letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted); text-decoration: none; padding-bottom: 2px; border-bottom: 0.5px solid transparent; transition: all 0.2s; }
  .nav-link:hover { color: var(--white); border-color: var(--white); }
  .nav-link.active { color: var(--white); border-color: var(--white); }
  .back { display: inline-block; padding: 20px 40px 0; font-size: 9px; font-weight: 300; letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color 0.2s; }
  .back:hover { color: var(--white); }
  .hero-img { height: 420px; background: var(--bg3); display: flex; align-items: center; justify-content: center; position: relative; margin-top: 18px; overflow: hidden; }
  .hero-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .hero-ph { font-size: 9px; color: var(--dim); letter-spacing: 0.12em; text-transform: uppercase; }
  .hero-overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 32px 40px; background: linear-gradient(transparent, rgba(14,14,12,0.88)); }
  .hero-title { font-size: 32px; font-weight: 300; color: var(--white); letter-spacing: 0.04em; margin-bottom: 8px; }
  .hero-meta { display: flex; gap: 12px; align-items: center; }
  .hero-type { font-size: 8px; color: var(--muted); letter-spacing: 0.2em; text-transform: uppercase; }
  .hero-dot { width: 2px; height: 2px; background: var(--muted); border-radius: 50%; }
  .body { padding: 40px 40px 0; max-width: 720px; }
  .desc-zh { font-size: 12px; font-weight: 300; color: var(--accent); line-height: 2; border-left: 0.5px solid var(--line); padding-left: 20px; margin-bottom: 20px; }
  .desc-en { font-size: 11px; font-weight: 300; color: var(--dim); line-height: 1.85; border-left: 0.5px solid var(--dim); padding-left: 20px; font-style: italic; margin-bottom: 52px; }
  .section-label { font-size: 8px; font-weight: 300; letter-spacing: 0.28em; text-transform: uppercase; color: var(--muted); padding: 0 40px; margin-bottom: 12px; }
  .g1 { display: grid; grid-template-columns: 1fr; gap: 1px; background: var(--line); margin-bottom: 1px; }
  .g2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: var(--line); margin-bottom: 1px; }
  .g-tall { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: var(--line); margin-bottom: 1px; }
  .g-tall-r { display: flex; flex-direction: column; gap: 1px; }
  .ph { background: var(--bg2); display: flex; align-items: center; justify-content: center; overflow: hidden; }
  .ph img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .ph-label { font-size: 8px; color: var(--dim); letter-spacing: 0.1em; text-transform: uppercase; }
  .ph-full { height: 360px; } .ph-half { height: 220px; }
  .ph-wide { height: 280px; } .ph-tall { height: 460px; }
  .ph-tall-half { flex: 1; min-height: 0; }
  .floorplan { padding: 36px 40px; border-top: 0.5px solid var(--line); }
  .floorplan-label { font-size: 8px; font-weight: 300; letter-spacing: 0.28em; text-transform: uppercase; color: var(--muted); margin-bottom: 14px; }
  .floorplan-box { background: var(--bg2); height: 200px; display: flex; align-items: center; justify-content: center; }
  .floorplan-box span { font-size: 8px; color: var(--dim); letter-spacing: 0.1em; text-transform: uppercase; }
  .bottom { padding: 28px 40px; border-top: 0.5px solid var(--line); display: flex; justify-content: space-between; align-items: center; }
  .bottom-nav { font-size: 9px; font-weight: 300; letter-spacing: 0.18em; text-transform: uppercase; color: var(--muted); text-decoration: none; transition: color 0.2s; }
  .bottom-nav:hover { color: var(--white); }
  .bowerbird { font-size: 9px; font-weight: 300; letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted); text-decoration: none; border: 0.5px solid var(--line); padding: 10px 20px; transition: all 0.2s; }
  .bowerbird:hover { color: var(--white); border-color: var(--accent); }
</style>"""

# Grid display order from commercial.html
PROJECTS = [
  ("de-nuit",    "de nuit",                "F&amp;B", "餐飲空間", "Taipei"),
  ("r-sanderson","R. Sanderson",           "Retail",  "零售空間", "Taipei"),
  ("monte",      "Monte",                  "F&amp;B", "餐飲空間", "Taipei"),
  ("lezun",      "樂樽爐端燒",             "F&amp;B", "餐飲空間", "Taipei"),
  ("iron-chef",  "IRON CHEF",              "F&amp;B", "餐飲空間", "Taipei"),
  ("mu-clinic",  "慕診所",                 "Other",   "其他",     "Taipei"),
  ("elle-cafe",  "ELLE Café",              "F&amp;B", "餐飲空間", "Taipei"),
  ("fire-play",  "Fire Play",              "F&amp;B", "餐飲空間", "Taipei"),
  ("cava-baja",  "Cava Baja",              "F&amp;B", "餐飲空間", "Taipei"),
  ("retrodandy", "Retrodandy",             "Retail",  "零售空間", "Taipei"),
  ("wave-flower","浪花花藝 Wave Flower",   "Retail",  "零售空間", "Taipei"),
  ("yun-jiao",   "耘角",                   "F&amp;B", "餐飲空間", "Taipei"),
  ("dunhua-32f", "敦化摩天辦公室 32F",     "Office",  "辦公空間", "Taipei"),
  ("dunnan-9f",  "敦南摩天辦公室 9F",      "Office",  "辦公空間", "Taipei"),
  ("new-vision", "新創視眼鏡",             "Retail",  "零售空間", "Taipei"),
]

n = len(PROJECTS)

for i, (slug, name, type_en, type_zh, loc) in enumerate(PROJECTS):
  if slug == "de-nuit":
    continue  # already done from reference template

  prev_slug, prev_name = PROJECTS[(i - 1) % n][0], PROJECTS[(i - 1) % n][1]
  next_slug, next_name = PROJECTS[(i + 1) % n][0], PROJECTS[(i + 1) % n][1]

  os.makedirs(f"{BASE}/commercial/{slug}", exist_ok=True)
  path = f"{BASE}/commercial/{slug}/index.html"

  html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — ON Design Lab</title>
{CSS}
</head>
<body>

<nav class="nav">
  <a class="nav-logo" href="../../index.html">ON Design Lab</a>
  <div class="nav-links">
    <a class="nav-link active" href="../index.html">Commercial</a>
    <a class="nav-link" href="../../residential/index.html">Residential</a>
    <a class="nav-link" href="../../info/index.html">Info</a>
  </div>
</nav>

<a class="back" href="../index.html">← Commercial</a>

<div class="hero-img">
  <!-- 換圖時：<img src="../../images/{slug}/01.jpg" alt="{name}"> -->
  <span class="hero-ph">01 — Cover photo</span>
  <div class="hero-overlay">
    <div class="hero-title">{name}</div>
    <div class="hero-meta">
      <span class="hero-type">{type_en}</span>
      <div class="hero-dot"></div>
      <span class="hero-type">{type_zh}</span>
      <div class="hero-dot"></div>
      <span class="hero-type">{loc}</span>
    </div>
  </div>
</div>

<div class="body">
  <p class="desc-zh">[待補文案]</p>
  <p class="desc-en">[Design statement — to be provided]</p>
</div>

<p class="section-label">Photos</p>

<div class="g1">
  <div class="ph ph-full">
    <!-- <img src="../../images/{slug}/02.jpg" alt="02"> -->
    <span class="ph-label">02</span>
  </div>
</div>
<div class="g2">
  <div class="ph ph-half"><span class="ph-label">03</span></div>
  <div class="ph ph-half"><span class="ph-label">04</span></div>
</div>
<div class="g1">
  <div class="ph ph-wide"><span class="ph-label">05</span></div>
</div>
<div class="g-tall">
  <div class="ph ph-tall"><span class="ph-label">06</span></div>
  <div class="g-tall-r">
    <div class="ph ph-tall-half"><span class="ph-label">07</span></div>
    <div class="ph ph-tall-half"><span class="ph-label">08</span></div>
  </div>
</div>
<div class="g2">
  <div class="ph ph-half"><span class="ph-label">09</span></div>
  <div class="ph ph-half"><span class="ph-label">10</span></div>
</div>

<div class="floorplan">
  <div class="floorplan-label">Floor Plan</div>
  <div class="floorplan-box">
    <!-- <img src="../../images/{slug}/plan.jpg" alt="Floor Plan" style="width:100%;height:100%;object-fit:contain;"> -->
    <span>平面圖</span>
  </div>
</div>

<div class="bottom">
  <a class="bottom-nav" href="../{prev_slug}/index.html">← {prev_name}</a>
  <a class="bowerbird" href="#">View on BowerBird →</a>
  <a class="bottom-nav" href="../{next_slug}/index.html">{next_name} →</a>
</div>

</body>
</html>"""

  with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
  print(f"Generated: commercial/{slug}/")

print(f"Done. {n-1} pages generated.")
