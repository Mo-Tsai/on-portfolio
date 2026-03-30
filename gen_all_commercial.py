import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'C:\Users\Mo_Tsai\Desktop\Google Drive\自動化測試資料夾\ONwebsite'

PROJECTS = [
  ('de-nuit',    'de nuit',               'F&amp;B', '餐飲空間', 'Taipei, Taiwan',  '2022'),
  ('r-sanderson','R. Sanderson',           'Retail',  '零售空間', 'Taipei, Taiwan',  '2021'),
  ('monte',      'Monte',                  'F&amp;B', '餐飲空間', 'Taipei, Taiwan',  '2021'),
  ('lezun',      '樂樽爐端燒',             'F&amp;B', '餐飲空間', 'Taipei, Taiwan',  '2022'),
  ('iron-chef',  'IRON CHEF',              'F&amp;B', '餐飲空間', 'Taipei, Taiwan',  '2020'),
  ('mu-clinic',  '慕診所',                 'Other',   '診所',     'Taipei, Taiwan',  '2023'),
  ('elle-cafe',  'ELLE Café',              'F&amp;B', '餐飲空間', 'Taipei, Taiwan',  '2022'),
  ('fire-play',  'Fire Play',              'F&amp;B', '餐飲空間', 'Taipei, Taiwan',  '2023'),
  ('cava-baja',  'Cava Baja',              'F&amp;B', '餐飲空間', 'Taipei, Taiwan',  '2022'),
  ('retrodandy', 'Retrodandy',             'Retail',  '零售空間', 'Taipei, Taiwan',  '2022'),
  ('wave-flower','浪花花藝 Wave Flower',   'Retail',  '零售空間', 'Taipei, Taiwan',  '2023'),
  ('yun-jiao',   '耘角',                   'F&amp;B', '餐飲空間', 'Taipei, Taiwan',  '2023'),
  ('dunhua-32f', '敦化摩天辦公室 32F',     'Office',  '辦公空間', 'Taipei, Taiwan',  '2022'),
  ('dunnan-9f',  '敦南摩天辦公室 9F',      'Office',  '辦公空間', 'Taipei, Taiwan',  '2023'),
  ('new-vision', '新創視眼鏡',             'Retail',  '零售空間', 'Taipei, Taiwan',  '2023'),
  ('lalaport',   'Urban Revivo LaLaport',  'Retail',  '零售空間', 'Singapore',       '2024'),
]

COPY = {
  'monte': (
    '設計不是在寬裕的時候才開始工作，是在限制中，為了精確的解法而產出。13坪。弧形吧台把兩端的人往中間收攏，讓座位之間有距離但同時有聚攏感，像圓桌，不像排隊。天花板不封板——四套系統留在視線裡，但以設計的方式存在。整合，是比設計更難的事。',
    "Design does not begin with abundance. It begins with the pressure to be exact. 13 pings. The arc of the bar draws people inward — distance between seats, but a sense of gathering. Like a round table, not a queue. The ceiling stays open — four systems remain visible, but exist by design. A space that works this hard does not need a ceiling to hide behind."
  ),
  'r-sanderson': (
    'R. Sanderson 的入口刻意內縮。你不是走進一個空間，你是被引導進去的。這個縮口不是美學決定，是一個讓身體先於眼睛進場的策略——當你的腳先移動，你的注意力才會跟上。動線末端是 VIP 試穿區，曲面牆圍塑，尺度稍稍放大，讓人在不自覺間放慢、坐下、停留。路徑，才是零售設計真正的產品。',
    "R. Sanderson's entrance is deliberately compressed. You are not walking into a space — you are being guided in. This constriction is not an aesthetic decision; it is a strategy that lets the body enter before the eyes do. At the end of the path, a VIP fitting area: curved walls, expanded scale, a place where people slow down without knowing why. The path is the product."
  ),
  'lezun': (
    '樂樽選擇白色立面。不是風格，是特殊塗料——抗汙、乾淨、帶著界線感。立面不做多餘的事，只讓室內的暖光從大面玻璃透出來。推門之後，色溫轉暖，墨色天花把設備收進背景，視線回到餐檯與料理檯。木格柵發想於「堆、疊」的構造感，燈藏在第二層，光從縫隙透出，陰影有了厚度。爐端燒的核心是食物和火，每個決定都在清除與這件事無關的視覺干擾。',
    "The white facade is not a style choice — it is a material decision: anti-stain, precise, boundary-defining. It does nothing except let the warm interior light pass through the glass. Inside, temperature shifts warm. A dark ceiling absorbs the equipment. The wooden grille hides the lights in its second layer — shadow gains depth. Every decision removes visual noise from what matters: fire and food."
  ),
  'mu-clinic': (
    '大部分的診所，從外面就讓你準備好緊張了。慕診所二店從立面開始重新設計這個時刻。六棵樹種在庭院平台上，森林影像輸出在玻璃格柵後面——一層是真實的綠，一層是抽象的樹林，兩個景深疊在一起，製造出一種錯覺：你不是在走進一棟建築，你是在走進一個地方。設計在這裡做的事，不是裝飾，是提前給出一個訊號：你可以放鬆了。',
    "Most clinics prepare you to be tense before you arrive. Mu Clinic's second location redesigns that moment at the facade. Six trees in the courtyard. A forest image printed behind glass grilles — one layer real, one layer abstract. Two depths overlap, creating an illusion: you are not entering a building. You are entering a place. Design here is not decoration. It is an early signal: you can relax now."
  ),
  'dunhua-32f': (
    '走進來，百歲磚沒有上漆。從入口到隔間牆，都是它。磚的顏色是磚本來的顏色。天花板沒有封板——舊管線太多，留著就讓它留著，管線噴上品牌藍，抬頭看見的是公司的顏色。接待在外，電話亭和會議室在中間，辦公室在最裡面——對外的事在前面解決，工作的人不被打斷。沒有一個選擇是只做一件事的。',
    "The brick enters unpainted. From the entrance to the partition walls — its colour is its own colour. The ceiling stays open: too many old pipes. So they stay. Painted in the brand's blue, the pipes become the company's colour overhead. Reception at the front, phone booths and meeting rooms in the middle, workstations furthest in. No decision was made to do only one thing."
  ),
}

EDIT_TEXT = [
  '材質與光線的對話，是這個空間最核心的語言。每一個細節都經過精心考量，讓功能與美學在此交匯。',
  '動線的設計決定了人在空間裡的感受。從入口到最深處，每一步都是設計者的一個問答。',
  '細節是空間誠意的所在。這裡展示的，是設計者對品質與比例最直接的表態。',
]

def get_photos(slug):
    path = os.path.join(BASE, 'images', slug)
    if not os.path.exists(path):
        return None, [], []
    all_files = sorted(os.listdir(path))
    imgs = [f for f in all_files if f.lower().endswith(('.jpg','.jpeg','.png'))]
    plans = [f for f in imgs if 'plan' in f.lower() and f != '00.jpg']
    body_candidates = [f for f in imgs if f not in ['00.jpg'] + plans]
    hero = None
    body = []
    for f in body_candidates:
        if f in ['01.jpg', '1.jpg'] and hero is None:
            hero = f
        else:
            body.append(f)
    if hero is None and body_candidates:
        hero = body_candidates[0]
        body = body_candidates[1:]
    return hero, body, plans

def gen_photo_html(slug, body):
    base = f'../../images/{slug}/'
    parts = []
    i = 0
    layout_seq = ['full','2col','editorial','full','asymm','editorial','2col','full','editorial'] * 4
    edit_i = 0
    for block in layout_seq:
        if i >= len(body):
            break
        if block == 'full':
            parts.append(f'  <div class="p-full"><img src="{base}{body[i]}" alt=""></div>')
            i += 1
        elif block == '2col':
            if i + 1 < len(body):
                parts.append(f'  <div class="p-2col">\n    <div class="p-cell"><img src="{base}{body[i]}" alt=""></div>\n    <div class="p-cell"><img src="{base}{body[i+1]}" alt=""></div>\n  </div>\n  <div class="gap-row"></div>')
                i += 2
            else:
                parts.append(f'  <div class="p-full"><img src="{base}{body[i]}" alt=""></div>')
                i += 1
        elif block == 'asymm':
            if i + 2 < len(body):
                parts.append(f'  <div class="p-asymm">\n    <div class="p-asymm-left p-cell"><img src="{base}{body[i]}" alt=""></div>\n    <div class="p-asymm-right">\n      <div class="p-cell"><img src="{base}{body[i+1]}" alt=""></div>\n      <div class="p-cell"><img src="{base}{body[i+2]}" alt=""></div>\n    </div>\n  </div>')
                i += 3
            elif i + 1 < len(body):
                parts.append(f'  <div class="p-2col">\n    <div class="p-cell"><img src="{base}{body[i]}" alt=""></div>\n    <div class="p-cell"><img src="{base}{body[i+1]}" alt=""></div>\n  </div>')
                i += 2
            else:
                parts.append(f'  <div class="p-full"><img src="{base}{body[i]}" alt=""></div>')
                i += 1
        elif block == 'editorial':
            t = EDIT_TEXT[edit_i % len(EDIT_TEXT)]
            parts.append(f'  <div class="editorial"><p>{t}</p></div>')
            edit_i += 1
    while i < len(body):
        parts.append(f'  <div class="p-full"><img src="{base}{body[i]}" alt=""></div>')
        i += 1
    return '\n'.join(parts)

def gen_thumbs(slug, photos):
    base = f'../../images/{slug}/'
    return '\n'.join([f'  <div class="thumb" onclick="openLightbox({j})"><img src="{base}{f}" alt=""></div>' for j,f in enumerate(photos)])

def gen_lb_array(slug, photos):
    base = f'../../images/{slug}/'
    return ',\n    '.join([f"'{base}{f}'" for f in photos])

# Read CSS from de-nuit template
with open(os.path.join(BASE, 'commercial', 'de-nuit', 'index.html'), encoding='utf-8') as fh:
    denuit = fh.read()
css_start = denuit.find('<style>')
css_end = denuit.find('</style>') + len('</style>')
STYLE_BLOCK = denuit[css_start:css_end]

n = len(PROJECTS)
for idx, (slug, name, type_en, type_zh, loc, year) in enumerate(PROJECTS):
    if slug == 'de-nuit':
        continue
    hero, body, plans = get_photos(slug)
    if hero is None:
        print(f'SKIP {slug}: no photos')
        continue

    prev_slug = PROJECTS[(idx-1) % n][0]
    next_slug = PROJECTS[(idx+1) % n][0]
    prev_name = PROJECTS[(idx-1) % n][1]
    next_name = PROJECTS[(idx+1) % n][1]

    desc_zh, desc_en = COPY.get(slug, (
        '[設計說明文字將放置於此。空間的每一個決定，都在回答一個問題。]',
        '[Design description placeholder. Every spatial decision answers a question.]'
    ))

    photo_html = gen_photo_html(slug, body)
    all_display = [hero] + body
    thumb_html = gen_thumbs(slug, all_display)
    lb_arr = gen_lb_array(slug, all_display)

    if plans:
        plan_lines = ['<div class="plan">', '  <p class="plan-label">Floor Plan</p>']
        for pf in plans:
            plan_lines.append(f'  <img src="../../images/{slug}/{pf}" onerror="this.style.display=\'none\'" alt="Floor Plan" style="margin-bottom:12px">')
        plan_lines.append('</div>')
        plan_html = '\n'.join(plan_lines)
    else:
        plan_html = f'<div class="plan"><img src="../../images/{slug}/plan.jpg" onerror="this.parentElement.style.display=\'none\'" alt=""></div>'

    city = loc.split(',')[0]

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — ON Design Lab</title>
{STYLE_BLOCK}
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <a class="nav-logo" href="../../index.html">ON Design Lab</a>
  <div class="nav-links">
    <a class="nav-link active" href="../index.html">Commercial</a>
    <a class="nav-link" href="../../residential/index.html">Residential</a>
    <a class="nav-link" href="../../info/index.html">Info</a>
  </div>
</nav>

<a class="back" href="../index.html">← Commercial</a>

<!-- HERO -->
<div class="hero-img">
  <img src="../../images/{slug}/{hero}" alt="{name}">
  <div class="hero-overlay">
    <div class="hero-title">{name}</div>
    <div class="hero-meta">
      <span class="hero-type">{type_en}</span>
      <div class="hero-dot"></div>
      <span class="hero-type">{type_zh}</span>
      <div class="hero-dot"></div>
      <span class="hero-type">{city}</span>
    </div>
  </div>
</div>

<!-- TEXT AREA -->
<div class="intro">
  <div class="meta-row">
    <div class="meta-item">
      <div class="meta-label">類型</div>
      <div class="meta-value">{type_zh}</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">地點</div>
      <div class="meta-value">{loc}</div>
    </div>
    <div class="meta-item">
      <div class="meta-label">年份</div>
      <div class="meta-value">{year}</div>
    </div>
  </div>
  <p class="desc-zh">{desc_zh}</p>
  <p class="desc-en">{desc_en}</p>
</div>

{plan_html}

<!-- PHOTO AREA -->
<div class="photos">
{photo_html}
</div>

<!-- THUMBNAIL STRIP -->
<div class="thumb-strip">
{thumb_html}
</div>

<!-- LIGHTBOX -->
<div id="lightbox" class="lightbox" style="display:none">
  <div class="lb-close" onclick="closeLightbox()">×</div>
  <div class="lb-prev" onclick="lbPrev()">‹</div>
  <img id="lb-img" src="" alt="">
  <div class="lb-next" onclick="lbNext()">›</div>
</div>

<!-- BOTTOM NAV -->
<div class="bottom">
  <a class="bottom-nav" href="../{prev_slug}/index.html">← {prev_name}</a>
  <a class="bowerbird" href="#">View on BowerBird →</a>
  <a class="bottom-nav" href="../{next_slug}/index.html">{next_name} →</a>
</div>

<script>
  const lbPhotos = [
    {lb_arr}
  ];
  let lbIndex = 0;
  function openLightbox(i) {{ lbIndex=i; document.getElementById('lb-img').src=lbPhotos[i]; document.getElementById('lightbox').style.display='flex'; document.body.style.overflow='hidden'; }}
  function closeLightbox() {{ document.getElementById('lightbox').style.display='none'; document.body.style.overflow=''; }}
  function lbNext() {{ lbIndex=(lbIndex+1)%lbPhotos.length; document.getElementById('lb-img').src=lbPhotos[lbIndex]; }}
  function lbPrev() {{ lbIndex=(lbIndex-1+lbPhotos.length)%lbPhotos.length; document.getElementById('lb-img').src=lbPhotos[lbIndex]; }}
  document.addEventListener('keydown', e => {{
    if (document.getElementById('lightbox').style.display==='flex') {{
      if (e.key==='ArrowRight') lbNext();
      if (e.key==='ArrowLeft') lbPrev();
      if (e.key==='Escape') closeLightbox();
    }}
  }});
</script>

</body>
</html>"""

    out_path = os.path.join(BASE, 'commercial', slug, 'index.html')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f'OK {slug}: hero={hero}, {len(body)} body photos, plans={plans}')

print('DONE')
