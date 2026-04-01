#!/usr/bin/env python3
"""
fix_lightbox.py  (v2 – safe nested-div removal)
Batch-fix all 27 project pages:
  1. Remove "All Photos" thumb-label + thumb-strip (duplicate images)
  2. Remove old lightbox HTML div (#lightbox)
  3. Remove old lightbox JS script (contains lbPhotos / openLightbox)
  4. Remove onclick="openLightbox(N)" attributes from content divs
  5. Remove THUMBNAILS / LIGHTBOX section comments
  6. Inject unified lightbox HTML + JS before </body>
  7. Add SEO meta tags if missing
"""

import re
import os

FILES = [
    "commercial/de-nuit/index.html",
    "commercial/monte/index.html",
    "commercial/r-sanderson/index.html",
    "commercial/lezun/index.html",
    "commercial/mu-clinic/index.html",
    "commercial/dunhua-32f/index.html",
    "commercial/elle-cafe/index.html",
    "commercial/fire-play/index.html",
    "commercial/iron-chef/index.html",
    "commercial/cava-baja/index.html",
    "commercial/retrodandy/index.html",
    "commercial/wave-flower/index.html",
    "commercial/yun-jiao/index.html",
    "commercial/dunnan-9f/index.html",
    "commercial/new-vision/index.html",
    "commercial/lalaport/index.html",
    "residential/residence-g/index.html",
    "residential/residence-s/index.html",
    "residential/residence-h/index.html",
    "residential/residence-l/index.html",
    "residential/residence-o/index.html",
    "residential/residence-p/index.html",
    "residential/residence-k/index.html",
    "residential/residence-c/index.html",
    "residential/residence-v/index.html",
    "residential/residence-m/index.html",
    "residential/residence-r/index.html",
]

NEW_LIGHTBOX = '''\n<!-- Lightbox -->
<div id="lb" style="display:none;position:fixed;inset:0;z-index:999;background:rgba(0,0,0,.93);align-items:center;justify-content:center;">
  <button id="lb-close" style="position:absolute;top:1.5rem;right:2rem;font-size:24px;opacity:.5;cursor:pointer;background:none;border:none;color:#fafaf8;transition:opacity .2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.5">&#10005;</button>
  <button id="lb-prev" style="position:absolute;top:50%;transform:translateY(-50%);left:1rem;background:none;border:none;color:#fafaf8;font-size:2rem;opacity:.3;cursor:pointer;padding:1rem;transition:opacity .2s;" onmouseover="this.style.opacity=.9" onmouseout="this.style.opacity=.3">&#8249;</button>
  <img id="lb-img" src="" alt="" style="max-width:90vw;max-height:88vh;object-fit:contain;display:block;">
  <button id="lb-next" style="position:absolute;top:50%;transform:translateY(-50%);right:1rem;background:none;border:none;color:#fafaf8;font-size:2rem;opacity:.3;cursor:pointer;padding:1rem;transition:opacity .2s;" onmouseover="this.style.opacity=.9" onmouseout="this.style.opacity=.3">&#8250;</button>
  <span id="lb-counter" style="position:absolute;bottom:1.5rem;left:50%;transform:translateX(-50%);font-size:11px;opacity:.35;letter-spacing:.1em;color:#fafaf8;"></span>
</div>
<script>
(function(){
  const imgs=[...document.querySelectorAll('img[src]:not([src=""])')]
    .filter(i=>!i.closest('#lb'));
  const srcs=imgs.map(i=>i.src);
  const lb=document.getElementById('lb');
  const lbImg=document.getElementById('lb-img');
  const lbC=document.getElementById('lb-counter');
  let cur=0;
  function show(i){cur=i;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length;lb.style.display='flex';}
  function close(){lb.style.display='none';lbImg.src='';}
  imgs.forEach((img,i)=>{img.style.cursor='zoom-in';img.addEventListener('click',()=>show(i));});
  document.getElementById('lb-close').onclick=close;
  document.getElementById('lb-prev').onclick=()=>{cur=(cur-1+srcs.length)%srcs.length;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length;};
  document.getElementById('lb-next').onclick=()=>{cur=(cur+1)%srcs.length;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length;};
  lb.addEventListener('click',e=>{if(e.target===lb)close();});
  document.addEventListener('keydown',e=>{
    if(lb.style.display==='none')return;
    if(e.key==='ArrowLeft')document.getElementById('lb-prev').click();
    if(e.key==='ArrowRight')document.getElementById('lb-next').click();
    if(e.key==='Escape')close();
  });
})();
</script>'''


def find_closing_div(html, open_pos):
    """
    Given the index of a '<div' opening tag in html,
    return the index of the LAST char of its matching '</div>' (exclusive end).
    Uses a simple depth counter.
    """
    depth = 0
    i = open_pos
    length = len(html)
    while i < length:
        if html[i:i+4] == '<div':
            # Make sure it's actually a tag (followed by space, >, or /)
            if i + 4 < length and html[i+4] in (' ', '>', '/', '\t', '\n', '\r'):
                depth += 1
                i += 4
                continue
        if html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return i + 6  # exclusive end
            i += 6
            continue
        i += 1
    raise ValueError(f"No matching </div> found starting at position {open_pos}")


def remove_div_block(html, id_attr):
    """Remove <div id="id_attr" ...> ... </div> and any preceding HTML comment on its own line."""
    marker = f'id="{id_attr}"'
    pos = html.find(f'<div {marker}')
    if pos == -1:
        return html

    # Walk back to find any preceding single-line comment (e.g. <!-- ═══ LIGHTBOX ═══ -->)
    start = pos
    line_start = html.rfind('\n', 0, pos)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1  # skip the \n itself
    prefix = html[line_start:pos]
    if prefix.strip() == '':
        # Check the line before for a comment
        prev_line_end = line_start - 1  # the \n before line_start
        if prev_line_end > 0:
            prev_line_start = html.rfind('\n', 0, prev_line_end)
            if prev_line_start == -1:
                prev_line_start = 0
            else:
                prev_line_start += 1
            prev_line = html[prev_line_start:prev_line_end]
            stripped = prev_line.strip()
            if stripped.startswith('<!--') and stripped.endswith('-->'):
                start = prev_line_start

    end = find_closing_div(html, pos)
    # Consume trailing newline if present
    if end < len(html) and html[end] == '\n':
        end += 1

    return html[:start] + html[end:]


def remove_thumb_section(html):
    """Remove <p class="thumb-label">All Photos</p> and the following <div class="thumb-strip">."""
    label = '<p class="thumb-label">All Photos</p>'
    pos = html.find(label)
    if pos == -1:
        return html

    # Walk back to include any preceding blank-ish line / comment
    start = pos
    line_start = html.rfind('\n', 0, pos)
    if line_start != -1:
        prev = html[line_start + 1:pos]
        if prev.strip() == '':
            start = line_start  # include the preceding \n

    # Find thumb-strip div after the label
    after_label = pos + len(label)
    strip_start = html.find('<div class="thumb-strip">', after_label)
    if strip_start == -1:
        # Just remove the label line
        end = after_label
        if end < len(html) and html[end] == '\n':
            end += 1
        return html[:start] + html[end:]

    end = find_closing_div(html, strip_start)
    # Consume trailing newline
    if end < len(html) and html[end] == '\n':
        end += 1

    return html[:start] + html[end:]


def remove_lightbox_script(html):
    """
    Remove <script> blocks that contain lightbox-related code
    (identified by presence of 'lbPhotos' or 'openLightbox' or 'closeLightbox').
    """
    result = []
    i = 0
    while i < len(html):
        script_open = html.find('<script>', i)
        if script_open == -1:
            result.append(html[i:])
            break
        script_close = html.find('</script>', script_open)
        if script_close == -1:
            result.append(html[i:])
            break
        block = html[script_open:script_close + 9]
        if ('lbPhotos' in block or 'openLightbox' in block or 'closeLightbox' in block):
            # Remove block; also consume trailing newline
            result.append(html[i:script_open])
            i = script_close + 9
            if i < len(html) and html[i] == '\n':
                i += 1
        else:
            result.append(html[i:script_open + 8])  # include <script>
            i = script_open + 8
    return ''.join(result)


def remove_section_comments(html):
    """Remove single-line HTML comments like <!-- ═══ THUMBNAILS ═══ --> and <!-- ═══ LIGHTBOX ═══ -->."""
    # Only match comments on their own line (no DOTALL — won't cross newlines)
    html = re.sub(r'\n[ \t]*<!--[^\n]*?(?:THUMBNAILS|LIGHTBOX)[^\n]*?-->[ \t]*(?=\n)', '', html)
    return html


def get_project_slug(filepath):
    parts = filepath.replace('\\', '/').split('/')
    return parts[-2]


def add_seo_meta(html, filepath):
    if '<meta name="description"' in html:
        return html

    title_match = re.search(r'<title>([^<]+)</title>', html)
    title_text = title_match.group(1) if title_match else 'ON Design Lab'
    slug = get_project_slug(filepath)
    folder_type = 'commercial' if filepath.startswith('commercial') else 'residential'

    seo = (
        f'\n<meta name="description" content="{title_text} | ON Design Lab 設計作品">'
        f'\n<meta property="og:title" content="{title_text}">'
        f'\n<meta property="og:description" content="{title_text} | ON Design Lab — 台北品牌空間設計事務所">'
        f'\n<meta property="og:image" content="https://ondesignlabltd.com/images/{slug}/00.jpg">'
        f'\n<meta property="og:url" content="https://ondesignlabltd.com/{folder_type}/{slug}/">'
        f'\n<meta property="og:type" content="website">'
        f'\n<meta name="twitter:card" content="summary_large_image">'
    )
    return html.replace('</head>', seo + '\n</head>')


def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Step 1: Remove "All Photos" thumb-label + thumb-strip
    content = remove_thumb_section(content)

    # Step 2: Remove old lightbox HTML div
    content = remove_div_block(content, 'lightbox')

    # Step 3: Remove old lightbox JS script
    content = remove_lightbox_script(content)

    # Step 4: Remove onclick="openLightbox(N)" attributes
    content = re.sub(r'\s*onclick="openLightbox\(\d+\)"', '', content)

    # Step 5: Remove THUMBNAILS / LIGHTBOX section comments
    content = remove_section_comments(content)

    # Step 6: Inject new lightbox before </body> (only if not already present)
    if 'id="lb"' not in content:
        content = content.replace('</body>', NEW_LIGHTBOX + '\n</body>')

    # Step 7: Add SEO meta tags if missing
    content = add_seo_meta(content, filepath)

    if content == original:
        print(f"  NO CHANGE: {filepath}")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  FIXED:     {filepath}")
    return True


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}\n")

    fixed = 0
    skipped = 0
    for fp in FILES:
        result = process_file(fp)
        if result:
            fixed += 1
        else:
            skipped += 1

    print(f"\nDone. {fixed} file(s) fixed, {skipped} unchanged/skipped.")


if __name__ == '__main__':
    main()
