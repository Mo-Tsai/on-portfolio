/* ════════ ON Design Lab｜單頁式換頁（全站共用）════════
   v2.58，Mo 09-29 第三輪：站內換頁不重新載入整頁、只換內容 → 音樂（sound.js）一路不斷。
   - 攔：同網域、HTML 頁（網址結尾 / 或 .html）的一般左鍵點擊。
   - 不攔：外部連結、mailto／tel、target=_blank、download、按著 Ctrl／⌘／Shift／Alt、同一頁的 #錨點、圖片／PDF／xml 等檔案。
   - 換頁：抓新頁 HTML → 換 <head> 的樣式／meta（樣式先載好才換，不閃）→ 換 <body>（左下 Sound 開關留著）
     → 重跑新頁的 script（首頁蒙太奇、lightbox.js 等；GA 與 sound.js／nav.js 本身不重跑）→ 通知 sound.js 換歌。
   - 上一頁／下一頁（popstate）一樣走這套，並回到當時捲動的位置。
   - GA：先換好標題再 pushState，GA4「強化型評估」會依瀏覽記錄變更自動記一次 page_view（不另外手動送，避免重複）。
   - 任何一步出錯 → 直接整頁載入那個網址（聲音靠 sessionStorage 接回）。
   - 直接網址進任何一頁都照舊（這支只接管之後的站內點擊）。 */
(function () {
  'use strict';
  if (window.ONNav || !window.fetch || !window.DOMParser || !history.pushState) return;

  var FADE = 220;              /* 換頁淡出／淡入（ms），克制 */
  var busy = null;             /* 目前這次換頁的 AbortController */
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion:reduce)').matches;
  try { history.scrollRestoration = 'manual'; } catch (e) {}
  history.replaceState(Object.assign({}, history.state || {}, { on: 1, y: window.scrollY }), '');

  function isPage(url) {
    var last = url.pathname.split('/').pop();
    return last === '' || /\.html?$/i.test(last) || last.indexOf('.') < 0;
  }

  function wanted(e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return null;
    var a = e.target && e.target.closest && e.target.closest('a[href]');
    if (!a) return null;
    if ((a.target && a.target !== '_self') || a.hasAttribute('download') || a.getAttribute('rel') === 'external') return null;
    if (a.hasAttribute('data-no-spa')) return null;
    var url;
    try { url = new URL(a.href, location.href); } catch (err) { return null; }
    if (url.origin !== location.origin || !/^https?:$/.test(url.protocol)) return null;
    if (!isPage(url)) return null;
    if (url.pathname === location.pathname && url.search === location.search && url.hash) return null;   /* 同頁錨點 */
    return url;
  }

  document.addEventListener('click', function (e) {
    var url = wanted(e);
    if (!url) return;
    e.preventDefault();
    go(url, true);
  });

  window.addEventListener('popstate', function (e) {
    go(new URL(location.href), false, e.state && e.state.y);
  });

  /* ── <head>：樣式與 meta 換成新頁的 ── */
  var HEAD_SEL = 'style, link[rel="stylesheet"], meta[name="description"], meta[property^="og:"], meta[name^="twitter:"],' +
                 'link[rel="canonical"], link[rel="alternate"], script[type="application/ld+json"], link[rel="preload"][as="image"]';
  function key(el) {
    if (el.tagName === 'LINK') return 'L|' + el.rel + '|' + el.href;
    if (el.tagName === 'META') return 'M|' + (el.name || el.getAttribute('property')) + '|' + el.content;
    return el.tagName + '|' + el.textContent;
  }
  function syncHead(doc) {
    var head = document.head, olds = [].slice.call(head.querySelectorAll(HEAD_SEL))
      .filter(function (el) { return !el.hasAttribute('data-persist'); });
    var have = {};
    olds.forEach(function (el) { have[key(el)] = el; });
    var keep = {}, waits = [];
    [].slice.call(doc.head.querySelectorAll(HEAD_SEL)).forEach(function (n) {
      var el = document.importNode(n, true);
      if (el.tagName === 'LINK') el.href = el.href;              /* 相對路徑照新網址解析 */
      var k = key(el);
      if (have[k]) { keep[k] = 1; return; }
      if (el.tagName === 'LINK' && el.rel === 'stylesheet') {
        el.removeAttribute('onload');
        if (el.media === 'print') el.media = 'all';               /* 原本的「非阻塞載入」寫法，已經載過了 */
        waits.push(new Promise(function (res) {
          el.addEventListener('load', res); el.addEventListener('error', res); setTimeout(res, 1500);
        }));
      }
      head.appendChild(el);
    });
    return Promise.all(waits).then(function () {
      olds.forEach(function (el) { if (!keep[key(el)]) el.remove(); });
    });
  }

  /* ── <body>：換內容、重跑 script ── */
  var SKIP_SCRIPT = /\/assets\/js\/(sound|nav)\.js|googletagmanager\.com/;
  function swapBody(doc) {
    var body = document.body;
    [].slice.call(body.childNodes).forEach(function (n) {
      if (!(n.nodeType === 1 && n.hasAttribute('data-persist'))) n.remove();
    });
    [].slice.call(body.attributes).forEach(function (a) { if (a.name !== 'style') body.removeAttribute(a.name); });
    [].slice.call(doc.body.attributes).forEach(function (a) { body.setAttribute(a.name, a.value); });
    var scripts = [], first = body.firstChild;
    [].slice.call(doc.body.childNodes).forEach(function (n) {
      if (n.nodeType === 1 && n.tagName === 'SCRIPT') { scripts.push(n); return; }
      var el = document.importNode(n, true);
      body.insertBefore(el, first);
      if (el.querySelectorAll) [].slice.call(el.querySelectorAll('script')).forEach(function (s) { scripts.push(s); s.remove(); });
    });
    /* 照順序執行；外部檔（lightbox.js）載完才跑下一段 */
    return scripts.reduce(function (p, s) {
      return p.then(function () {
        var src = s.getAttribute('src');
        if (src && SKIP_SCRIPT.test(new URL(src, location.href).href)) return;
        if (s.type && !/javascript|^module$/i.test(s.type)) return;
        var el = document.createElement('script');
        [].slice.call(s.attributes).forEach(function (a) { if (a.name !== 'defer' && a.name !== 'async') el.setAttribute(a.name, a.value); });
        if (src) {
          return new Promise(function (res) {
            el.onload = el.onerror = res; el.async = false; el.src = new URL(src, location.href).href;
            document.body.appendChild(el);
          });
        }
        /* 包一層大括號：各頁頂層的 const／let 重跑第二次才不會「已宣告」出錯 */
        el.textContent = '{\n' + s.textContent + '\n}';
        document.body.appendChild(el);
      });
    }, Promise.resolve());
  }

  function fade(to) {
    if (reduce) return Promise.resolve();
    var b = document.body;
    b.style.transition = 'opacity ' + FADE + 'ms ease';
    b.style.opacity = to;
    return new Promise(function (res) { setTimeout(res, FADE); });
  }

  function go(url, push, y) {
    if (busy) busy.abort();
    var ac = window.AbortController ? new AbortController() : { abort: function () {}, signal: undefined };
    busy = ac;
    if (push) history.replaceState(Object.assign({}, history.state || {}, { on: 1, y: window.scrollY }), '');
    var fetched = fetch(url.href, { signal: ac.signal, credentials: 'same-origin' }).then(function (r) {
      var ct = r.headers.get('content-type') || '';
      if (!r.ok || ct.indexOf('text/html') < 0) throw new Error('not-page');
      return r.text();
    });
    Promise.all([fetched, fade(0)]).then(function (res) {
      if (busy !== ac) return;
      var doc = new DOMParser().parseFromString(res[0], 'text/html');
      document.title = doc.title;                               /* 先換標題，GA 記到的才是新頁 */
      if (push) history.pushState({ on: 1, y: 0 }, '', url.href);
      document.documentElement.lang = doc.documentElement.lang || document.documentElement.lang;
      return syncHead(doc).then(function () {
        if (busy !== ac) return;
        window.ON_SPA_NAV = true;                               /* 首頁看到這個：不出 Entrance、不重播開場 */
        var ran = swapBody(doc);
        if (url.hash) {
          var t = document.getElementById(decodeURIComponent(url.hash.slice(1)));
          if (t) t.scrollIntoView(); else window.scrollTo(0, 0);
        } else window.scrollTo(0, push ? 0 : (y || 0));
        if (window.ONSound) ONSound.page(url.pathname);
        document.dispatchEvent(new CustomEvent('on:navigate', { detail: { path: url.pathname } }));
        return ran.then(function () { return fade(1); });
      });
    }).catch(function (err) {
      if (err && err.name === 'AbortError') return;
      location.href = url.href;                                 /* 出錯就整頁載入 */
    }).then(function () { if (busy === ac) busy = null; });
  }

  window.ONNav = { go: function (href) { go(new URL(href, location.href), true); } };
})();
