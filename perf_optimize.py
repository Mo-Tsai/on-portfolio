#!/usr/bin/env python3
"""
Performance optimization for all project pages:
1. Add fetchpriority="high" to hero images (improves LCP)
2. Skip pages that already have it
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

patterns = [
    os.path.join(ROOT, 'commercial', '*', 'index.html'),
    os.path.join(ROOT, 'residential', '*', 'index.html'),
]

files = []
for p in patterns:
    files.extend(glob.glob(p))

updated = 0
skipped = 0

for fpath in sorted(files):
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Already optimized
    if 'fetchpriority="high"' in html:
        skipped += 1
        continue

    # Find hero-img img and add fetchpriority="high"
    # Pattern: inside .hero-img div, find <img ... loading="eager"
    new_html = re.sub(
        r'(<div class="hero-img">[\s\S]*?<img\s[^>]*?)(loading="eager")',
        r'\1fetchpriority="high" \2',
        html,
        count=1
    )

    if new_html != html:
        with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_html)
        rel = os.path.relpath(fpath, ROOT)
        print(f'  OK {rel}')
        updated += 1
    else:
        print(f'  - no hero-img found: {os.path.relpath(fpath, ROOT)}')
        skipped += 1

print(f'\nDone: {updated} updated, {skipped} skipped')
