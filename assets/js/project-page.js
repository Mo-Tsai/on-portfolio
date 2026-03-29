/* ============================================================
   ON Design Lab — Project Page JS
   Reads slug from URL, finds project data, renders page.
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  const parts   = window.location.pathname.replace(/\/$/, '').split('/');
  const slug    = parts[parts.length - 1];
  const section = parts[parts.length - 2]; // 'commercial' or 'residential'

  const list    = PROJECTS[section] || [];
  const project = list.find(p => p.slug === slug);

  if (!project) {
    document.title = 'Not Found — ON Design Lab';
    return;
  }

  const lang    = localStorage.getItem('on_lang') || 'zh';
  const name    = lang === 'en' ? project.nameEn : project.nameZh;
  const type    = section === 'commercial'
    ? (lang === 'en' ? project.typeEn : project.type)
    : (section === 'residential' ? (lang === 'en' ? 'Residential' : '住家空間') : '');

  /* Page title */
  document.title = `${name} — ON Design Lab`;

  /* Hero title */
  const heroTitle = document.getElementById('hero-title');
  if (heroTitle) {
    heroTitle.querySelector('.project-type').setAttribute('data-en', project.typeEn || 'Residential');
    heroTitle.querySelector('.project-type').setAttribute('data-zh', project.type  || '住家空間');
    heroTitle.querySelector('.project-type').textContent = type;
    heroTitle.querySelector('h1').setAttribute('data-en', project.nameEn);
    heroTitle.querySelector('h1').setAttribute('data-zh', project.nameZh);
    heroTitle.querySelector('h1').textContent = name;
  }

  /* Back link */
  const backLink = document.getElementById('back-link');
  if (backLink) {
    backLink.href = `/${section}/`;
    backLink.setAttribute('data-en', section === 'commercial' ? '← Commercial' : '← Residential');
    backLink.setAttribute('data-zh', section === 'commercial' ? '← 商業空間'  : '← 住家空間');
    backLink.textContent = section === 'commercial'
      ? (lang === 'en' ? '← Commercial' : '← 商業空間')
      : (lang === 'en' ? '← Residential' : '← 住家空間');
  }

  /* Photo sequence — placeholders */
  const seq = document.getElementById('photo-sequence');
  if (seq) {
    const count = project.photos || 10;
    for (let i = 2; i <= count; i++) {
      seq.innerHTML += `
        <div class="photo-item">
          <div class="photo-placeholder"></div>
        </div>`;
    }
  }

  /* Re-apply language for dynamically set data-en/zh attrs */
  if (typeof applyLang === 'function') applyLang(lang);
});
