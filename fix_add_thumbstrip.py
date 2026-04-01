#!/usr/bin/env python3
"""
fix_add_thumbstrip.py
Re-add the "All Photos" thumb-strip to all 27 project pages.
Also updates the lightbox JS to:
  - exclude .thumb-strip imgs from the main lightbox sequence (no duplicates)
  - add click handlers on .thumb so clicking a thumbnail opens lightbox at the right position
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

# Updated lightbox JS — excludes .thumb-strip, handles thumb clicks
NEW_LB_JS = '''\n<!-- Lightbox -->
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
    .filter(i=>!i.closest('#lb')&&!i.closest('.thumb-strip'));
  const srcs=imgs.map(i=>i.src);
  const lb=document.getElementById('lb');
  const lbImg=document.getElementById('lb-img');
  const lbC=document.getElementById('lb-counter');
  let cur=0;
  function show(i){cur=i;lbImg.src=srcs[cur];lbC.textContent=(cur+1)+' / '+srcs.length;lb.style.display='flex';}
  function close(){lb.style.display='none';lbImg.src='';}
  imgs.forEach((img,i)=>{img.style.cursor='zoom-in';img.addEventListener('click',()=>show(i));});
  document.querySelectorAll('.thumb-strip .thumb').forEach(t=>{
    t.style.cursor='zoom-in';
    t.addEventListener('click',()=>{
      const s=t.querySelector('img').src;
      const i=srcs.findIndex(x=>x===s);
      if(i>=0)show(i);
    });
  });
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


def extract_photos_srcs(html):
    """Extract img srcs from inside .photos div, excluding plan/hero/onerror images."""
    # Find .photos div
    photos_start = html.find('<div class="photos">')
    if photos_start == -1:
        photos_start = html.find('<div class="photos"')
    if photos_start == -1:
        return []

    # Find end of photos div by counting nesting
    depth = 0
    i = photos_start
    photos_end = len(html)
    while i < len(html):
        if html[i:i+4] == '<div':
            if i + 4 < len(html) and html[i+4] in (' ', '>', '/', '\t', '\n'):
                depth += 1
                i += 4
                continue
        if html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                photos_end = i + 6
                break
            i += 6
            continue
        i += 1

    photos_html = html[photos_start:photos_end]

    # Extract all img srcs (skip onerror images like plan.jpg)
    srcs = []
    for m in re.finditer(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', photos_html):
        full_tag = m.group(0)
        if 'onerror' in full_tag:
            continue  # skip plan img
        src = m.group(1)
        if src and src not in srcs:
            srcs.append(src)

    return srcs


def build_thumb_strip(srcs):
    """Build the All Photos thumb-strip HTML from a list of src paths."""
    thumbs = '\n'.join(
        f'<div class="thumb"><img loading="lazy" decoding="async" src="{src}" alt=""></div>'
        for src in srcs
    )
    return (
        '\n<p class="thumb-label">All Photos</p>\n'
        '<div class="thumb-strip">\n'
        f'{thumbs}\n'
        '</div>'
    )


def remove_old_lb_block(html):
    """Remove existing lightbox div + script injected by previous fix."""
    # Remove <!-- Lightbox --> comment + #lb div + script
    pos = html.find('<!-- Lightbox -->')
    if pos != -1:
        end = html.find('</script>', pos)
        if end != -1:
            end += 9  # len('</script>')
            if end < len(html) and html[end] == '\n':
                end += 1
            html = html[:pos] + html[end:]
    return html


def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Step 1: Extract photo srcs from content area
    srcs = extract_photos_srcs(content)
    if not srcs:
        print(f"  SKIP (no photos found): {filepath}")
        return False

    # Step 2: Build thumb-strip HTML
    thumb_html = build_thumb_strip(srcs)

    # Step 3: Remove old lightbox block (will re-inject updated version)
    content = remove_old_lb_block(content)

    # Step 4: Insert thumb-strip before <div class="bottom">
    bottom_marker = '<div class="bottom">'
    if bottom_marker in content:
        content = content.replace(bottom_marker, thumb_html + '\n' + bottom_marker)
    else:
        # Fallback: insert before </body>
        content = content.replace('</body>', thumb_html + '\n</body>')

    # Step 5: Inject updated lightbox before </body>
    content = content.replace('</body>', NEW_LB_JS + '\n</body>')

    if content == original:
        print(f"  NO CHANGE: {filepath}")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  FIXED:     {filepath}  ({len(srcs)} photos)")
    return True


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}\n")

    fixed = 0
    for fp in FILES:
        if process_file(fp):
            fixed += 1

    print(f"\nDone. {fixed} file(s) updated.")


if __name__ == '__main__':
    main()
