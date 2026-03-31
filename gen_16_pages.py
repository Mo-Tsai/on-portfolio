import os

BASE = "C:/Users/Mo_Tsai/Desktop/Google Drive/自動化測試資料夾/ONwebsite"

# Project definitions: slug, title, type_en, type_zh, location, prev_href, prev_label, next_href, next_label
projects = [
    ("monte",      "Monte",                    "F&amp;B",  "餐飲空間", "Taipei", "de-nuit",    "de nuit",              "r-sanderson",  "R. Sanderson"),
    ("r-sanderson","R. Sanderson",             "Retail",   "零售空間", "Taipei", "monte",       "Monte",                "lezun",        "樂樽爐端燒"),
    ("lezun",      "樂樽爐端燒",               "F&amp;B",  "餐飲空間", "Taipei", "r-sanderson", "R. Sanderson",         "mu-clinic",    "慕診所"),
    ("mu-clinic",  "慕診所",                   "Other",    "其他空間", "Taipei", "lezun",       "樂樽爐端燒",           "dunhua-32f",   "敦化摩天辦公室 32F"),
    ("dunhua-32f", "敦化摩天辦公室 32F",       "Office",   "辦公空間", "Taipei", "mu-clinic",   "慕診所",               "elle-cafe",    "ELLE Café"),
    ("elle-cafe",  "ELLE Café",                "F&amp;B",  "餐飲空間", "Taipei", "dunhua-32f",  "敦化摩天辦公室 32F",   "fire-play",    "Fire Play"),
    ("fire-play",  "Fire Play",                "F&amp;B",  "餐飲空間", "Taipei", "elle-cafe",   "ELLE Café",            "iron-chef",    "IRON CHEF"),
    ("iron-chef",  "IRON CHEF",                "F&amp;B",  "餐飲空間", "Taipei", "fire-play",   "Fire Play",            "cava-baja",    "Cava Baja"),
    ("cava-baja",  "Cava Baja",                "F&amp;B",  "餐飲空間", "Taipei", "iron-chef",   "IRON CHEF",            "retrodandy",   "Retrodandy"),
    ("retrodandy", "Retrodandy",               "Retail",   "零售空間", "Taipei", "cava-baja",   "Cava Baja",            "wave-flower",  "浪花花藝 Wave Flower"),
    ("wave-flower","浪花花藝 Wave Flower",      "Retail",   "零售空間", "Taipei", "retrodandy",  "Retrodandy",           "yun-jiao",     "耘角"),
    ("yun-jiao",   "耘角",                     "F&amp;B",  "餐飲空間", "Taipei", "wave-flower", "浪花花藝 Wave Flower",  "dunnan-9f",    "敦南摩天辦公室 9F"),
    ("dunnan-9f",  "敦南摩天辦公室 9F",        "Office",   "辦公空間", "Taipei", "yun-jiao",    "耘角",                  "new-vision",   "新創視眼鏡"),
    ("new-vision", "新創視眼鏡",               "Retail",   "零售空間", "Taipei", "dunnan-9f",   "敦南摩天辦公室 9F",    "lalaport",     "恆隆行_南港LaLaport"),
    ("lalaport",   "恆隆行_南港LaLaport",      "Retail",   "零售空間", "Taipei", "new-vision",  "新創視眼鏡",           "la-vie-wine",  "La Vie Wine 樂活酒窖"),
    ("la-vie-wine","La Vie Wine 樂活酒窖",     "Retail",   "零售空間", "Taipei", "lalaport",    "恆隆行_南港LaLaport",  "de-nuit",      "de nuit"),
]

# Image data: slug -> list of (filename_noext, orientation)
# L = landscape (w>h), P = portrait (h>w), S = square
img_data = {
    "monte": [
        ("01","P"),("02","P"),("03","L"),("04","P"),("05","L"),
        ("06","P"),("07","P"),("08","P"),("10","P"),("11","P"),
        ("12","P"),("13","P"),("14","P"),("15","P"),("16","P"),
        ("18","L"),("21","L"),("26","P"),("27","P"),("28","P"),
        ("31","L"),("32","L"),
    ],
    "r-sanderson": [
        ("01","P"),("02","P"),("03","L"),("06","L"),("08","P"),
        ("11","L"),("13","L"),("14","L"),("15","L"),("16","L"),
        ("19","P"),("20","P"),("22","L"),("23","S"),
    ],
    "lezun": [
        ("01","P"),("02","P"),("03","P"),("05","L"),("06","P"),
        ("08","L"),("10","L"),("15","L"),("20","L"),
    ],
    "mu-clinic": [
        ("01","L"),("02","L"),("03","P"),("04","P"),("05","P"),
        ("21","L"),("25","L"),("26","P"),("28","P"),("29","P"),
        ("37","L"),("39","P"),("41","L"),("43","P"),("47","L"),
        ("56","P"),("58","P"),
    ],
    "dunhua-32f": [
        ("01","P"),("02","P"),("04","L"),("05","P"),("07","L"),
        ("08","L"),("09","L"),("11","L"),("12","P"),("14","L"),("15","L"),
    ],
    "elle-cafe": [
        ("01","L"),("02","L"),("04","L"),("05","L"),("07","P"),
        ("08","P"),("09","L"),("18","L"),("20","L"),("27","L"),("31","L"),
    ],
    "fire-play": [
        ("01","P"),("02","P"),("03","L"),("04","P"),("05","L"),
        ("06","L"),("07","L"),("08","P"),("09","L"),("11","L"),("12","P"),
    ],
    "iron-chef": [
        ("01","L"),("03","L"),("04","L"),("05","P"),("06","L"),
        ("09","L"),("14","L"),("23","P"),("27","P"),("29","L"),("31","P"),("34","L"),
    ],
    "cava-baja": [
        ("01","L"),("02","L"),("03","L"),("06","L"),("12","P"),
        ("13","P"),("17","P"),("18","L"),("19","L"),("20","L"),("22","L"),
    ],
    "retrodandy": [
        ("02","L"),("03","L"),("04","L"),("05","L"),("06","L"),
    ],
    "wave-flower": [
        ("02","L"),("03","P"),("04","P"),("05","P"),("09","L"),
        ("10","L"),("14","P"),("15","P"),("16","P"),("17","P"),("20","P"),
    ],
    "yun-jiao": [
        ("01","P"),("03","P"),("04","P"),("05","P"),("07","P"),
        ("08","L"),("11","L"),("12","P"),("13","L"),("14","L"),("16","L"),
        ("17","L"),("18","L"),("20","L"),("21","L"),("22","P"),("23","L"),
        ("24","L"),("25","P"),("26","L"),("27","P"),("28","L"),
    ],
    "dunnan-9f": [
        ("01","L"),("02","L"),("03","L"),("04","P"),("05","P"),
        ("06","L"),("07","L"),("08","L"),("09","P"),("14","L"),("15","L"),
    ],
    "new-vision": [
        ("01","L"),("02","L"),("05","L"),("06","P"),("07","P"),
        ("08","P"),("09","L"),("10","L"),("12","L"),("13","L"),
    ],
    "lalaport": [
        ("01","L"),("03","L"),("04","L"),("05","L"),("07","L"),
        ("08","L"),("10","L"),("12","L"),
    ],
    "la-vie-wine": [
        ("01","L"),("02","L"),("03","P"),("04","L"),("05","L"),
        ("06","L"),("07","L"),("09","L"),("10","L"),("11","L"),
        ("12","L"),("13","L"),("14","P"),
    ],
}


def plan_layout(photos_in):
    """Plan photo layout blocks. Returns list of block dicts."""
    blocks = []
    photos = list(photos_in)
    count_since_editorial = 0

    while photos:
        # Insert editorial after every 3 photos
        if count_since_editorial >= 3:
            blocks.append({"type": "editorial"})
            count_since_editorial = 0

        fn, ori = photos[0]

        if ori == "P":
            # Try to make p-asymm: P on left + 2 L on right
            L_indices = [j for j in range(1, len(photos)) if photos[j][1] in ("L", "S")]
            if len(L_indices) >= 2:
                fn1 = photos[L_indices[0]][0]
                fn2 = photos[L_indices[1]][0]
                blocks.append({"type": "asymm", "left": fn, "right1": fn1, "right2": fn2})
                for idx in sorted([0, L_indices[0], L_indices[1]], reverse=True):
                    photos.pop(idx)
                count_since_editorial += 3
                continue

            # Try p-2col with another P
            P_indices = [j for j in range(1, len(photos)) if photos[j][1] == "P"]
            if P_indices:
                fn2 = photos[P_indices[0]][0]
                blocks.append({"type": "2col", "left": fn, "right": fn2})
                for idx in sorted([0, P_indices[0]], reverse=True):
                    photos.pop(idx)
                count_since_editorial += 2
                continue

            # Fallback: full
            blocks.append({"type": "full", "fn": fn})
            photos.pop(0)
            count_since_editorial += 1

        elif ori in ("L", "S"):
            # Try p-2col with another L or S (only when not about to insert editorial)
            LS_indices = [j for j in range(1, len(photos)) if photos[j][1] in ("L", "S")]
            if LS_indices and count_since_editorial < 3:
                fn2 = photos[LS_indices[0]][0]
                blocks.append({"type": "2col", "left": fn, "right": fn2})
                for idx in sorted([0, LS_indices[0]], reverse=True):
                    photos.pop(idx)
                count_since_editorial += 2
                continue

            blocks.append({"type": "full", "fn": fn})
            photos.pop(0)
            count_since_editorial += 1

        else:
            blocks.append({"type": "full", "fn": fn})
            photos.pop(0)
            count_since_editorial += 1

    return blocks


def render_blocks(slug, blocks):
    parts = []
    for b in blocks:
        if b["type"] == "full":
            parts.append(
                '  <div class="p-full"><img src="../../images/' + slug + '/' + b["fn"] + '.jpg" alt="' + b["fn"] + '"></div>\n'
                '  <div class="gap-row"></div>\n'
            )
        elif b["type"] == "2col":
            parts.append(
                '  <div class="p-2col">\n'
                '    <div class="p-cell"><img src="../../images/' + slug + '/' + b["left"] + '.jpg" alt="' + b["left"] + '"></div>\n'
                '    <div class="p-cell"><img src="../../images/' + slug + '/' + b["right"] + '.jpg" alt="' + b["right"] + '"></div>\n'
                '  </div>\n'
                '  <div class="gap-row"></div>\n'
            )
        elif b["type"] == "asymm":
            parts.append(
                '  <div class="p-asymm">\n'
                '    <div class="p-asymm-left p-cell"><img src="../../images/' + slug + '/' + b["left"] + '.jpg" alt="' + b["left"] + '"></div>\n'
                '    <div class="p-asymm-right">\n'
                '      <div class="p-cell"><img src="../../images/' + slug + '/' + b["right1"] + '.jpg" alt="' + b["right1"] + '"></div>\n'
                '      <div class="p-cell"><img src="../../images/' + slug + '/' + b["right2"] + '.jpg" alt="' + b["right2"] + '"></div>\n'
                '    </div>\n'
                '  </div>\n'
                '  <div class="gap-row"></div>\n'
            )
        elif b["type"] == "editorial":
            parts.append('  <div class="editorial"><p>[待補說明文字]</p></div>\n')
    return "".join(parts)


def collect_all_photos(blocks):
    photos = []
    seen = set()
    for b in blocks:
        if b["type"] == "full":
            if b["fn"] not in seen:
                photos.append(b["fn"])
                seen.add(b["fn"])
        elif b["type"] == "2col":
            for key in ("left", "right"):
                if b[key] not in seen:
                    photos.append(b[key])
                    seen.add(b[key])
        elif b["type"] == "asymm":
            for key in ("left", "right1", "right2"):
                if b[key] not in seen:
                    photos.append(b[key])
                    seen.add(b[key])
    return photos


def build_html(slug, title, type_en, type_zh, location,
               prev_href, prev_label, next_href, next_label,
               photo_blocks_html, thumb_items, lb_array):

    onerror_attr = "onerror=\"this.parentElement.style.display='none'\""

    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"zh-TW\">\n"
        "<head>\n"
        "<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "<title>" + title + " \u2014 ON Design Lab</title>\n"
        "<style>\n"
        "  :root {\n"
        "    --bg:    #0e0e0c;\n"
        "    --bg2:   #141412;\n"
        "    --line:  #252520;\n"
        "    --white: #f0efe8;\n"
        "    --muted: #4a4a44;\n"
        "    --dim:   #2a2a26;\n"
        "    --accent:#666660;\n"
        "  }\n"
        "  * { margin:0; padding:0; box-sizing:border-box; }\n"
        "  body { font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; background:var(--bg); color:var(--white); }\n"
        "  .nav { display:flex; align-items:center; justify-content:space-between; padding:20px 40px; border-bottom:0.5px solid var(--line); position:sticky; top:0; background:var(--bg); z-index:200; }\n"
        "  .nav-logo { font-size:10px; font-weight:300; letter-spacing:0.26em; text-transform:uppercase; color:var(--white); text-decoration:none; }\n"
        "  .nav-links { display:flex; gap:28px; }\n"
        "  .nav-link { font-size:9px; font-weight:300; letter-spacing:0.22em; text-transform:uppercase; color:var(--muted); text-decoration:none; padding-bottom:2px; border-bottom:0.5px solid transparent; transition:all 0.2s; }\n"
        "  .nav-link:hover, .nav-link.active { color:var(--white); border-color:var(--white); }\n"
        "  .back { display:inline-block; padding:20px 40px 0; font-size:9px; font-weight:300; letter-spacing:0.2em; text-transform:uppercase; color:var(--muted); text-decoration:none; transition:color 0.2s; }\n"
        "  .back:hover { color:var(--white); }\n"
        "  .hero-img { width:100%; height:85vh; overflow:hidden; position:relative; margin-top:18px; }\n"
        "  .hero-img img { width:100%; height:100%; object-fit:cover; object-position:center 50%; display:block; }\n"
        "  .hero-overlay { position:absolute; bottom:0; left:0; right:0; padding:40px 48px; background:linear-gradient(transparent, rgba(14,14,12,0.9)); pointer-events:none; }\n"
        "  .hero-title { font-size:36px; font-weight:300; color:var(--white); letter-spacing:0.04em; margin-bottom:10px; }\n"
        "  .hero-meta { display:flex; gap:12px; align-items:center; }\n"
        "  .hero-type { font-size:9px; color:var(--muted); letter-spacing:0.22em; text-transform:uppercase; }\n"
        "  .hero-dot { width:2px; height:2px; background:var(--muted); border-radius:50%; }\n"
        "  .intro { max-width:560px; padding:80px 40px; margin:0 auto; text-align:center; }\n"
        "  .desc-zh { font-size:15px; line-height:2.1; color:var(--accent); margin-bottom:28px; }\n"
        "  .desc-en { font-size:13px; line-height:1.9; color:var(--dim); font-style:italic; }\n"
        "  .plan { max-width:560px; margin:0 auto; padding:0 40px 60px; }\n"
        "  .plan-label { font-size:8px; letter-spacing:0.28em; text-transform:uppercase; color:var(--muted); margin-bottom:14px; }\n"
        "  .plan img { width:100%; height:auto; display:block; }\n"
        "  .photos { width:100%; }\n"
        "  .p-full, .p-2col, .p-asymm { padding:0 20%; }\n"
        "  .p-full img { width:100%; height:auto; display:block; }\n"
        "  .p-2col { display:grid; grid-template-columns:1fr 1fr; gap:3px; }\n"
        "  .p-cell { position:relative; }\n"
        "  .p-cell img { width:100%; height:auto; display:block; }\n"
        "  .p-asymm { display:grid; grid-template-columns:1fr 1fr; gap:3px; align-items:stretch; }\n"
        "  .p-asymm-left img { width:100%; height:100%; object-fit:cover; display:block; }\n"
        "  .p-asymm-right { display:flex; flex-direction:column; gap:3px; }\n"
        "  .p-asymm-right .p-cell { flex:1; }\n"
        "  .p-asymm-right .p-cell img { width:100%; height:100%; object-fit:cover; display:block; }\n"
        "  .editorial { max-width:560px; padding:64px 40px; margin:0 auto; text-align:center; }\n"
        "  .editorial p { font-size:13px; font-weight:300; color:var(--muted); line-height:2.1; }\n"
        "  .editorial p + p { margin-top:20px; }\n"
        "  .gap-row { height:3px; background:var(--bg); }\n"
        "  .thumb-label { font-size:8px; font-weight:300; letter-spacing:0.28em; text-transform:uppercase; color:var(--muted); padding:32px 40px 12px; }\n"
        "  .thumb-strip { display:flex; overflow-x:auto; gap:4px; padding:0 40px 32px; scrollbar-width:none; }\n"
        "  .thumb-strip::-webkit-scrollbar { display:none; }\n"
        "  .thumb { flex-shrink:0; width:120px; height:80px; overflow:hidden; cursor:pointer; opacity:0.6; transition:opacity 0.2s; }\n"
        "  .thumb:hover { opacity:1; }\n"
        "  .thumb img { width:100%; height:100%; object-fit:cover; display:block; }\n"
        "  .lightbox { position:fixed; inset:0; background:rgba(0,0,0,0.95); z-index:1000; display:flex; align-items:center; justify-content:center; }\n"
        "  #lb-img { max-width:90vw; max-height:90vh; object-fit:contain; }\n"
        "  .lb-close { position:absolute; top:24px; right:32px; font-size:32px; color:var(--white); cursor:pointer; font-weight:300; line-height:1; user-select:none; }\n"
        "  .lb-prev, .lb-next { position:absolute; top:50%; transform:translateY(-50%); font-size:48px; color:var(--white); cursor:pointer; font-weight:300; padding:0 24px; opacity:0.5; transition:opacity 0.2s; user-select:none; line-height:1; }\n"
        "  .lb-prev { left:0; } .lb-next { right:0; }\n"
        "  .lb-prev:hover, .lb-next:hover { opacity:1; }\n"
        "  .bottom { padding:28px 40px; border-top:0.5px solid var(--line); display:flex; justify-content:space-between; align-items:center; margin-top:16px; }\n"
        "  .bottom-nav { font-size:9px; font-weight:300; letter-spacing:0.18em; text-transform:uppercase; color:var(--muted); text-decoration:none; transition:color 0.2s; }\n"
        "  .bottom-nav:hover { color:var(--white); }\n"
        "  .bowerbird { font-size:9px; font-weight:300; letter-spacing:0.22em; text-transform:uppercase; color:var(--muted); text-decoration:none; border:0.5px solid var(--line); padding:10px 20px; transition:all 0.2s; }\n"
        "  .bowerbird:hover { color:var(--white); border-color:var(--accent); }\n"
        "  @media (max-width: 768px) {\n"
        "    .intro { padding:48px 24px; max-width:100%; }\n"
        "    .plan { max-width:100%; padding:0 24px 48px; }\n"
        "    .p-2col { grid-template-columns:1fr; }\n"
        "    .p-asymm { grid-template-columns:1fr; }\n"
        "    .p-asymm-left { display:none; }\n"
        "    .p-full, .p-2col, .p-asymm { padding:0 5%; }\n"
        "    .editorial { padding:40px 24px; }\n"
        "    .thumb { width:90px; height:60px; }\n"
        "    .thumb-strip { padding:0 20px 24px; }\n"
        "    .thumb-label { padding:24px 20px 10px; }\n"
        "    .hero-img { height:60vh; }\n"
        "    .nav { padding:16px 20px; }\n"
        "    .back { padding:16px 20px 0; }\n"
        "    .bottom { padding:20px 20px; }\n"
        "  }\n"
        "</style>\n"
        "<meta name=\"description\" content=\"" + title + " | ON Design Lab \u8a2d\u8a08\u4f5c\u54c1\">\n"
        "<meta property=\"og:title\" content=\"" + title + " \u2014 ON Design Lab\">\n"
        "<meta property=\"og:description\" content=\"" + title + " | ON Design Lab \u2014 \u53f0\u5317\u54c1\u724c\u7a7a\u9593\u8a2d\u8a08\u4e8b\u52d9\u6240\">\n"
        "<meta property=\"og:image\" content=\"https://ondesignlabltd.com/images/" + slug + "/00.jpg\">\n"
        "<meta property=\"og:url\" content=\"https://ondesignlabltd.com/commercial/" + slug + "/\">\n"
        "<meta property=\"og:type\" content=\"website\">\n"
        "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
        "</head>\n"
        "<body>\n"
        "<nav class=\"nav\">\n"
        "  <a class=\"nav-logo\" href=\"../../index.html\">ON Design Lab</a>\n"
        "  <div class=\"nav-links\">\n"
        "    <a class=\"nav-link active\" href=\"../index.html\">Commercial</a>\n"
        "    <a class=\"nav-link\" href=\"../../residential/index.html\">Residential</a>\n"
        "    <a class=\"nav-link\" href=\"../../info/index.html\">Info</a>\n"
        "  </div>\n"
        "</nav>\n"
        "<a class=\"back\" href=\"../index.html\">\u2190 Commercial</a>\n"
        "<div class=\"hero-img\">\n"
        "  <img src=\"../../images/" + slug + "/00.jpg\" alt=\"" + title + "\">\n"
        "  <div class=\"hero-overlay\">\n"
        "    <div class=\"hero-title\">" + title + "</div>\n"
        "    <div class=\"hero-meta\">\n"
        "      <span class=\"hero-type\">" + type_en + "</span>\n"
        "      <div class=\"hero-dot\"></div>\n"
        "      <span class=\"hero-type\">" + type_zh + "</span>\n"
        "      <div class=\"hero-dot\"></div>\n"
        "      <span class=\"hero-type\">" + location + "</span>\n"
        "    </div>\n"
        "  </div>\n"
        "</div>\n"
        "<div class=\"intro\">\n"
        "  <p class=\"desc-zh\">[\u5f85\u88dc\u6587\u6848]</p>\n"
        "  <p class=\"desc-en\">[Design statement \u2014 to be provided]</p>\n"
        "</div>\n"
        "<div class=\"plan\">\n"
        "  <p class=\"plan-label\">Floor Plan</p>\n"
        "  <img src=\"../../images/" + slug + "/plan.jpg\" " + onerror_attr + " alt=\"Floor Plan\">\n"
        "</div>\n"
        "<div class=\"photos\">\n"
        + photo_blocks_html +
        "</div>\n"
        "<p class=\"thumb-label\">All Photos</p>\n"
        "<div class=\"thumb-strip\">\n"
        + thumb_items +
        "</div>\n"
        "<div id=\"lightbox\" class=\"lightbox\" style=\"display:none\">\n"
        "  <div class=\"lb-close\" onclick=\"closeLightbox()\">\u00d7</div>\n"
        "  <div class=\"lb-prev\" onclick=\"lbPrev()\">\u2039</div>\n"
        "  <img id=\"lb-img\" src=\"\" alt=\"\">\n"
        "  <div class=\"lb-next\" onclick=\"lbNext()\">\u203a</div>\n"
        "</div>\n"
        "<div class=\"bottom\">\n"
        "  <a class=\"bottom-nav\" href=\"../" + prev_href + "/index.html\">\u2190 " + prev_label + "</a>\n"
        "  <a class=\"bowerbird\" href=\"#\">View on BowerBird \u2192</a>\n"
        "  <a class=\"bottom-nav\" href=\"../" + next_href + "/index.html\">" + next_label + " \u2192</a>\n"
        "</div>\n"
        "<script>\n"
        "  const lbPhotos = [" + lb_array + "\n"
        "  ];\n"
        "  let lbIndex = 0;\n"
        "  function openLightbox(i) { lbIndex=i; document.getElementById('lb-img').src=lbPhotos[i]; document.getElementById('lightbox').style.display='flex'; document.body.style.overflow='hidden'; }\n"
        "  function closeLightbox() { document.getElementById('lightbox').style.display='none'; document.body.style.overflow=''; }\n"
        "  function lbNext() { lbIndex=(lbIndex+1)%lbPhotos.length; document.getElementById('lb-img').src=lbPhotos[lbIndex]; }\n"
        "  function lbPrev() { lbIndex=(lbIndex-1+lbPhotos.length)%lbPhotos.length; document.getElementById('lb-img').src=lbPhotos[lbIndex]; }\n"
        "  document.addEventListener('keydown', e => {\n"
        "    if (document.getElementById('lightbox').style.display==='flex') {\n"
        "      if (e.key==='ArrowRight') lbNext();\n"
        "      if (e.key==='ArrowLeft') lbPrev();\n"
        "      if (e.key==='Escape') closeLightbox();\n"
        "    }\n"
        "  });\n"
        "</script>\n"
        "</body>\n"
        "</html>"
    )


for proj in projects:
    slug, title, type_en, type_zh, location, prev_href, prev_label, next_href, next_label = proj

    photos = list(img_data[slug])
    blocks = plan_layout(photos)
    photo_blocks_html = render_blocks(slug, blocks)
    all_photos = collect_all_photos(blocks)

    # Build thumb items
    thumb_lines = []
    for idx, fn in enumerate(all_photos):
        thumb_lines.append(
            '  <div class="thumb" onclick="openLightbox(' + str(idx) + ')"><img src="../../images/' + slug + '/' + fn + '.jpg" alt="' + fn + '"></div>'
        )
    thumb_items = "\n".join(thumb_lines) + "\n"

    # Build lightbox array
    lb_lines = []
    for fn in all_photos:
        lb_lines.append("    '../../images/" + slug + "/" + fn + ".jpg',")
    lb_array = "\n" + "\n".join(lb_lines)

    html = build_html(
        slug, title, type_en, type_zh, location,
        prev_href, prev_label, next_href, next_label,
        photo_blocks_html, thumb_items, lb_array
    )

    out_path = BASE + "/commercial/" + slug + "/index.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Written: " + slug + " (" + str(len(all_photos)) + " photos)")

print("Done!")
