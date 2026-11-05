/* ════════ ON Design Lab｜工法影片（Journal 共用）════════
   v2.108（Mo 11-05 定）：原本 14 篇 Journal 各自一段 inline script，搬到這裡共用，並接上全站音樂（sound.js）。
   - 點播放鍵才載入 YouTube（youtube-nocookie），沒點之前不連 YouTube。
   - 影片一播，背景音樂淡出：點播放 → ONSound.hold('video')；iframe 載好後用 YouTube IFrame API 的 postMessage
     （{event:'listening', id, channel:'widget'}）要它回報狀態 → onStateChange：1 播放中→hold；0 播完、2 暫停→release。
   - 換頁（on:navigate）、離開頁面（pagehide）、iframe 不在了 → release。多個 .tv 共用一個 message 監聽，用 id 對應。
   - sound.js 沒載到（或還沒載）時照常播影片，只是不壓音樂。
   - 單頁式換頁（nav.js）會重跑這支：第二次起只重新綁新頁的 .tv，不重複掛監聽。 */
(function () {
  'use strict';
  var YT = 'https://www.youtube-nocookie.com';

  if (window.ONTV) { window.ONTV.bind(); return; }

  var seq = 0;
  var frames = {};          /* id → { fig, el, state }；state：'pending'＝剛點還沒回報、或 YouTube 的 -1/0/1/2/3/5 */

  function hold() { if (window.ONSound && ONSound.hold) ONSound.hold('video'); }
  function release() { if (window.ONSound && ONSound.release) ONSound.release('video'); }

  /* 只有「播完（0）」「暫停（2）」算停；剛點還沒回報、-1 未開始、3 緩衝、5 已載入 都當還在播 → 壓住 */
  function sync() {
    var busy = false;
    Object.keys(frames).forEach(function (id) {
      var f = frames[id];
      if (!document.contains(f.el)) { delete frames[id]; return; }
      if (!(f.state === 0 || f.state === 2)) busy = true;
    });
    if (busy) hold(); else release();
  }

  function clearAll() {
    frames = {};
    release();
  }

  function bind() {
    var list = document.querySelectorAll('.tv');
    for (var i = 0; i < list.length; i++) bindOne(list[i]);
  }
  function bindOne(fig) {
    if (fig.__onTv) return;
    fig.__onTv = true;
    var btn = fig.querySelector('.tv-play');
    if (!btn) return;
    btn.addEventListener('click', function () {
      if (!fig.dataset.yt) return;
      var frame = fig.querySelector('.tv-frame'), el = document.createElement('iframe');
      var id = 'on-tv-' + (++seq);
      el.id = id;
      el.src = YT + '/embed/' + fig.dataset.yt +
        '?autoplay=1&rel=0&playsinline=1&enablejsapi=1&origin=' + encodeURIComponent(location.origin);
      el.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      el.title = fig.dataset.title || 'Video';
      el.addEventListener('load', function () {
        try { el.contentWindow.postMessage(JSON.stringify({ event: 'listening', id: id, channel: 'widget' }), YT); } catch (e) {}
      });
      frames[id] = { fig: fig, el: el, state: 'pending' };
      frame.innerHTML = ''; frame.appendChild(el);
      sync();
    });
  }

  /* YouTube 回報（只收 youtube-nocookie 來的、JSON 的） */
  window.addEventListener('message', function (e) {
    if (e.origin !== YT || typeof e.data !== 'string') return;
    var d;
    try { d = JSON.parse(e.data); } catch (err) { return; }
    if (!d || !d.id || !frames[d.id]) return;
    var st = null;
    if (d.event === 'onStateChange') st = d.info;
    else if (d.event === 'infoDelivery' && d.info && typeof d.info.playerState === 'number') st = d.info.playerState;
    if (typeof st !== 'number') return;
    var f = frames[d.id];
    if (f.state === st) return;
    f.state = st;
    sync();
  });

  document.addEventListener('on:navigate', clearAll);
  window.addEventListener('pagehide', clearAll);

  window.ONTV = { bind: bind, sync: sync, _frames: function () { return frames; } };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bind);
  else bind();
})();
