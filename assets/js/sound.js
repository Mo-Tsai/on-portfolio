/* ════════ ON Design Lab｜全站聲音（共用）════════
   v2.58。Mo 09-29 第三輪裁定（覆蓋之前的進站設計）：
   - 首頁黑幕＝ON 標誌＋「Entrance」，按下去＝t 0：開場檔（4 小節，含聲音 logo）第一拍＋黑幕打開＋對拍蒙太奇；
     10.667 秒無縫接 No.1 循環。首頁的部分在首頁 inline script，這裡提供 intro() 歌曲時鐘。
   - 站內換頁是單頁式（/assets/js/nav.js），音樂一路不斷。
   - 分線：首頁＝No.1、/commercial/ 系列＝City、/residential/ 系列＝Home、其他頁延續當下那首；
     換歌在下一個小節線等功率交叉淡化 1 小節（90 BPM，一小節 2.667 秒）。
   - 直接網址進其他頁（Google）：第一次互動（任何地方）開始播這頁的那首；瀏覽器若本來就准出聲，直接開始。
   - 左下角細字 Sound on／Sound off，sessionStorage 記開關、目前那首、播到第幾秒（整頁重新載入時接得回來）。
   - 背景分頁暫停、回來淡入。音量 0.5、淡入 0.4 秒（Mo 09-28）。
   - 不設 navigator.audioSession（保留 iOS 靜音鍵會讓網頁無聲）。 */
(function () {
  'use strict';
  if (window.ONSound) return;

  /* ── 可調參數 ── */
  var CFG = {
    volume:      0.5,     /* 整體音量（0–1）。音檔本身 -16 LUFS；Mo 09-28 定 0.5 */
    introFadeIn: 0.4,     /* 按 Entrance 後開場檔淡入秒數（首頁可用 intro({fadeIn}) 覆蓋） */
    resumeFade:  0.4,     /* 第一次互動／整頁重新載入／分頁回來 的淡入秒數 */
    fadeOut:     0.25,    /* 關掉或分頁切走時的淡出秒數 */
    xfadeBars:   1,       /* 換歌交叉淡化幾小節 */
    waitAudio:   0.35     /* 按 Entrance 時音檔還沒準備好，最多等幾秒再先跑畫面 */
  };

  /* 三首都是 90 BPM：一小節 2.6667 秒 */
  var BAR = 60 / 90 * 4;
  var INTRO_PRE = 0.010;           /* 開場檔：檔案第 0.010 秒＝第一拍重擊（歌曲時間 0） */
  var INTRO_LEN = 4 * BAR;         /* 10.6667：開場 4 小節，歌曲時間到這裡接 No.1 循環 */

  var base = (function () {
    var s = document.currentScript && document.currentScript.src;
    try { return new URL('../audio/', s || location.href).href; } catch (e) { return '/assets/audio/'; }
  })();
  /* 各首循環檔。City 用 v3 有哼唱人聲版上線（Mo 09-29 定），無人聲版 10/27 之後換新檔名 */
  var TRACKS = {
    no1:  { file: 'no1-loop-12bars-20260928.m4a', bars: 12 },
    city: { file: 'city-loop-24bars-v3vocal-20260928.m4a', bars: 24 },
    home: { file: 'home-loop-16bars-20260928.m4a', bars: 16 }
  };
  var INTRO_FILE = 'no1-intro-4bars-logo-20260928.m4a';

  /* 哪一頁放哪一首；null＝延續當下那首 */
  function trackFor(path) {
    var p = (path || location.pathname).replace(/index\.html$/, '');
    if (/^\/(en\/)?$/.test(p)) return 'no1';
    if (/^\/(en\/)?commercial\//.test(p)) return 'city';
    if (/^\/(en\/)?residential\//.test(p)) return 'home';
    return null;
  }

  /* ── sessionStorage（私密視窗可能丟例外，全部包起來） ── */
  var K_ON = 'on.sound', K_POS = 'on.sound.pos', K_TRACK = 'on.sound.track';
  function sget(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function sset(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }

  /* 測試用：網址加 ?soundblock=1 → 模擬「瀏覽器擋自動播放」（要真的點／按鍵才出聲）；?soundblock=0 取消 */
  var gestureSeen = false;
  var TEST_BLOCK = (function () {
    var m = /[?&]soundblock=([01])/.exec(location.search);
    if (m) sset('on.sound.testblock', m[1]);
    return sget('on.sound.testblock') === '1';
  })();
  function unlocked() { return !TEST_BLOCK || gestureSeen; }

  var on = sget(K_ON) !== 'off';                 /* 預設開 */
  var ctx = null, master = null;
  var buf = {}, loading = {};
  var cur = null;          /* 目前那首：{ name, src, g, zero, len }；zero＝循環位置 0 對應的 ctx 時間 */
  var pend = null;         /* 正在交叉淡化進來的那首 */
  var introSrc = null;
  var songZero = null;     /* 歌曲時間 0（開場第一拍）對應的 ctx 時間 */
  var want = trackFor() || sget(K_TRACK) || 'no1';   /* 這一頁想放的那首 */
  var hiddenPaused = false, suspendTimer = null, introInFlight = false;
  var log = window.__onSoundLog = [];
  function L(ev, extra) {
    var o = { ev: ev, perf: Math.round(performance.now()), ctx: ctx ? +ctx.currentTime.toFixed(4) : null, state: ctx ? ctx.state : 'none' };
    if (extra) for (var k in extra) o[k] = extra[k];
    log.push(o);
    if (log.length > 400) log.shift();
  }

  /* ── AudioContext ── */
  function ensureCtx() {
    if (ctx) return ctx;
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    try { ctx = new AC({ latencyHint: 'playback', sampleRate: 48000 }); }
    catch (e) { try { ctx = new AC(); } catch (e2) { return null; } }
    master = ctx.createGain();
    master.gain.value = 0;
    master.connect(ctx.destination);
    L('ctx-created', { sr: ctx.sampleRate });
    return ctx;
  }
  function running() { return ctx && ctx.state === 'running'; }

  /* 解碼。AAC 解出來可能比原稿少最後幾十個樣本（Chrome 依 m4a 的 edit list 截掉；實測開場檔、Home 各少 32），
     直接接會在接縫留一小段靜音＋爆音 → 把缺的尾巴用直線補到「接下去那個樣本」（循環檔＝自己的第一個樣本），波形連續。 */
  function expectLen(name) { return name === 'intro' ? INTRO_PRE + INTRO_LEN : TRACKS[name].bars * BAR; }
  function padTail(b, secs, nextFirst) {
    var sr = b.sampleRate, need = Math.round(secs * sr), miss = need - b.length;
    if (miss <= 0 || miss > sr * 0.01) return { b: b, miss: miss };
    var nb = ctx.createBuffer(b.numberOfChannels, need, sr);
    for (var c = 0; c < b.numberOfChannels; c++) {
      var s = b.getChannelData(c), d = nb.getChannelData(c);
      d.set(s);
      var a = s[s.length - 1], z = nextFirst ? nextFirst(c) : s[0];
      for (var i = 0; i < miss; i++) d[b.length + i] = a + (z - a) * (i + 1) / (miss + 1);
    }
    return { b: nb, miss: miss };
  }
  function load(name) {
    if (buf[name]) return Promise.resolve(buf[name]);
    if (loading[name]) return loading[name];
    if (!ensureCtx()) return Promise.reject(new Error('no-webaudio'));
    var url = base + (name === 'intro' ? INTRO_FILE : TRACKS[name].file);
    loading[name] = fetch(url).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.arrayBuffer();
    }).then(function (ab) {
      return new Promise(function (res, rej) {
        var p = ctx.decodeAudioData(ab, res, rej);      /* 舊 Safari 只有 callback 版 */
        if (p && p.then) p.then(res, rej);
      });
    }).then(function (b) {
      var len = b.length;
      if (name !== 'intro') b = padTail(b, expectLen(name)).b;
      buf[name] = b;
      L('decoded', { name: name, len: len, fixed: b.length, sr: b.sampleRate });
      return b;
    });
    loading[name].catch(function (e) { L('load-fail', { name: name, err: String(e) }); loading[name] = null; });
    return loading[name];
  }
  var introFixed = false;
  function fixIntroTail() {
    if (introFixed || !buf.intro || !buf.no1) return;
    introFixed = true;
    var r = padTail(buf.intro, expectLen('intro'), function (c) { return buf.no1.getChannelData(Math.min(c, buf.no1.numberOfChannels - 1))[0]; });
    buf.intro = r.b;
    L('intro-tail', { miss: r.miss });
  }

  /* 「聽到的」ctx 時間：扣掉輸出延遲，畫面才會跟耳朵對上 */
  var lastHeard = 0;
  function heardNow() {
    if (!ctx) return 0;
    var t;
    if (ctx.getOutputTimestamp) {
      var ts = ctx.getOutputTimestamp();
      if (ts && ts.contextTime > 0 && ts.performanceTime > 0) t = ts.contextTime + (performance.now() - ts.performanceTime) / 1000;
    }
    if (t === undefined) t = ctx.currentTime - (ctx.outputLatency || ctx.baseLatency || 0);
    if (t < lastHeard) t = lastHeard;
    if (t > ctx.currentTime) t = ctx.currentTime;
    lastHeard = t;
    return t;
  }

  function ramp(param, to, sec) {
    var t = ctx.currentTime;
    try { param.cancelScheduledValues(t); } catch (e) {}
    param.setValueAtTime(param.value, t);
    param.linearRampToValueAtTime(to, t + Math.max(0.01, sec));
  }
  /* 等功率曲線（交叉淡化用） */
  function eqCurve(up) {
    var n = 64, a = new Float32Array(n);
    for (var i = 0; i < n; i++) { var x = i / (n - 1); a[i] = up ? Math.sin(x * Math.PI / 2) : Math.cos(x * Math.PI / 2); }
    return a;
  }

  function stopTrack(t, at) {
    if (!t) return;
    try { t.src.stop(at || 0); } catch (e) {}
    var ms = Math.max(0, ((at || 0) - ctx.currentTime) * 1000) + 300;
    clearTimeout(t.kill);
    t.kill = setTimeout(function () { try { t.src.disconnect(); t.g.disconnect(); } catch (e) {} }, ms);
  }
  function stopAll() {
    if (introSrc) { try { introSrc.stop(); } catch (e) {} introSrc = null; }
    stopTrack(cur); stopTrack(pend);
    cur = pend = null;
  }

  /* 循環檔：在 ctx 時間 when 從循環位置 pos 起播，接到自己的 gain（gain0＝起始音量） */
  function makeTrack(name, when, pos, gain0) {
    var len = TRACKS[name].bars * BAR;
    var g = ctx.createGain(); g.gain.value = gain0; g.connect(master);
    var s = ctx.createBufferSource();
    s.buffer = buf[name]; s.loop = true; s.loopStart = 0; s.loopEnd = len;
    s.connect(g);
    pos = ((pos % len) + len) % len;
    s.start(when, pos);
    L('track-start', { name: name, when: +when.toFixed(4), pos: +pos.toFixed(3) });
    return { name: name, src: s, g: g, zero: when - pos, len: len };
  }
  function posOf(t) {
    if (!t || !ctx) return null;
    var x = ctx.currentTime - t.zero;
    return x < 0 ? 0 : x % t.len;
  }
  function savePos() {
    if (!cur) return;
    sset(K_TRACK, cur.name);
    sset(K_POS, posOf(cur).toFixed(3));
  }
  function playing() { return !!(cur || introSrc); }

  /* 開始出聲（第一次互動／整頁重新載入／打開聲音）：播這頁想放的那首，從記住的秒數淡入 */
  function resumeLoop() {
    if (introInFlight) { if (ctx && ctx.resume) ctx.resume(); return; }
    if (!on || playing() || introPendingOnPage() || !unlocked()) return;
    if (!ensureCtx()) return;
    var p = ctx.resume ? ctx.resume() : Promise.resolve();
    var name = want;
    load(name).then(function () { return p; }).then(function () {
      if (!on || playing() || !running() || introPendingOnPage()) return;
      var pos = sget(K_TRACK) === name ? (parseFloat(sget(K_POS)) || 0) : 0;
      master.gain.setValueAtTime(0, ctx.currentTime);
      cur = makeTrack(name, ctx.currentTime + 0.03, pos, 1);
      ramp(master.gain, CFG.volume, CFG.resumeFade);
      render();
      if (want !== name) switchTo(want);
    }).catch(function (e) { L('resume-fail', { err: String(e) }); });
  }

  /* 換歌：下一個小節線開始，等功率交叉淡化 CFG.xfadeBars 小節 */
  function switchTo(name) {
    want = name;
    if (!ctx || !cur) return;                     /* 還沒開始播：之後開始時就會放 want */
    if (pend) {                                    /* 上一個換歌還沒完成 */
      if (pend.name === name) return;
      stopTrack(pend, 0);                          /* 取消它，原本那首回到全音量 */
      try { cur.g.gain.cancelScheduledValues(0); } catch (e) {}
      cur.g.gain.setValueAtTime(1, ctx.currentTime);
      clearTimeout(cur.kill);                      /* 原本排好的「停掉舊的」也取消 */
      try { cur.src.stop(ctx.currentTime + 86400); } catch (e) {}
      if (introSrc) { try { introSrc.stop(songZero + INTRO_LEN); } catch (e) {} }
      pend = null;
    }
    if (cur.name === name) return;
    var from = cur;
    load(name).then(function () {
      if (want !== name || cur !== from || pend) return;
      if (!running()) {                            /* 聲音暫停中（背景／關掉）：直接換，不淡化 */
        stopTrack(from, 0);
        if (introSrc) { try { introSrc.stop(); } catch (e) {} introSrc = null; }
        cur = makeTrack(name, ctx.currentTime + 0.03, 0, 1); savePos(); return;
      }
      /* 小節線照「目前那首」的網格算（開場檔還在播時，網格就是開場的歌曲時鐘，一樣整齊） */
      var zero = from.zero, now = ctx.currentTime + 0.12;
      var at = zero + Math.ceil((now - zero) / BAR) * BAR;
      var dur = CFG.xfadeBars * BAR;
      var nx = makeTrack(name, at, 0, 0);
      nx.g.gain.setValueCurveAtTime(eqCurve(true), at, dur);
      from.g.gain.setValueAtTime(1, at);
      from.g.gain.setValueCurveAtTime(eqCurve(false), at, dur);
      if (introSrc) { try { introSrc.stop(at + dur); } catch (e) {} }
      stopTrack(from, at + dur + 0.05);
      pend = nx;
      L('xfade', { from: from.name, to: name, at: +at.toFixed(4), inSec: +(at - ctx.currentTime).toFixed(3) });
      setTimeout(function done() {
        if (pend !== nx) return;
        if (ctx.currentTime < at + dur) { setTimeout(done, 100); return; }   /* 暫停過：等真的淡化完 */
        cur = nx; pend = null; introSrc = null; savePos();
      }, (at + dur - ctx.currentTime) * 1000 + 60);
    });
  }

  /* 首頁黑幕還在等 Entrance：全站的「第一次互動」不搶著放循環檔（那一下交給 Entrance） */
  function introPendingOnPage() { return window.ON_SOUND_INTRO === 'pending'; }

  /* ════ 首頁：按 Entrance ════
     回傳歌曲時鐘 clock.t()：第一拍＝0，單位秒；還沒開始時回傳 null。
     音檔準備好時以 AudioContext 為準；還沒準備好就先用 performance 時鐘跑畫面，音檔到了再從對應的位置接進來。 */
  function intro(opt) {
    opt = opt || {};
    var fadeIn = opt.fadeIn != null ? opt.fadeIn : CFG.introFadeIn;
    gestureSeen = true;
    want = 'no1';
    var perfTap = performance.now();
    var clock = { mode: 'wait', perfZero: null, frozen: null };
    var withAudio = on && ensureCtx();
    clock.t = function () {
      if (clock.mode === 'audio') {
        if (!running()) return clock.frozen;                 /* 分頁在背景：時鐘停住 */
        var v = heardNow() - songZero;
        clock.frozen = v;
        return v;
      }
      if (clock.mode === 'perf') return (performance.now() - clock.perfZero) / 1000;
      return null;
    };
    function goPerf() {
      if (clock.mode !== 'wait') return;
      clock.mode = 'perf';
      clock.perfZero = performance.now();
      L('intro-perf-clock', { waited: Math.round(clock.perfZero - perfTap) });
    }
    if (!withAudio) { goPerf(); return clock; }

    stopAll();
    introInFlight = true;
    var resumed = ctx.resume ? ctx.resume() : Promise.resolve();
    var fallback = setTimeout(goPerf, CFG.waitAudio * 1000);
    Promise.all([load('intro'), load('no1'), resumed]).then(function () {
      if (!running()) throw new Error('ctx-not-running');
      clearTimeout(fallback);
      fixIntroTail();
      introInFlight = false;
      if (!on) { goPerf(); return; }
      var now = ctx.currentTime, when = now + 0.05;
      if (clock.mode === 'wait') songZero = when;
      else {
        var lat = (ctx.outputLatency || ctx.baseLatency || 0);
        songZero = when - ((performance.now() - clock.perfZero) / 1000 + (when - now) + lat);
      }
      var s0 = when - songZero;
      master.gain.setValueAtTime(0, now);
      if (s0 < INTRO_LEN) {
        cur = makeTrack('no1', songZero + INTRO_LEN, 0, 1);
        var src = ctx.createBufferSource();
        src.buffer = buf.intro;
        src.connect(cur.g);                      /* 開場檔跟 No.1 同一條音量：換歌時一起淡出 */
        var startCtx = songZero - INTRO_PRE, off = 0;
        if (startCtx < when) { off = when - startCtx; startCtx = when; }
        src.start(startCtx, off, (INTRO_PRE + INTRO_LEN) - off);   /* 只播到接縫，後面交給循環檔 */
        introSrc = src;
        src.onended = function () { if (introSrc === src) introSrc = null; };
      } else {
        cur = makeTrack('no1', when, s0 - INTRO_LEN, 1);
      }
      ramp(master.gain, CFG.volume, fadeIn);
      clock.mode = 'audio';
      L('intro-audio', { songZero: +songZero.toFixed(4), s0: +s0.toFixed(4), outLat: ctx.outputLatency || 0 });
      render();
      if (want !== 'no1') switchTo(want);        /* 開場時就點去別頁：照樣換 */
    }).catch(function (e) {
      introInFlight = false;
      L('intro-audio-fail', { err: String(e) });
      goPerf();
    });
    return clock;
  }

  /* ── 開關 ── */
  var btn = null;
  function render() {
    if (!btn) return;
    btn.firstChild.textContent = on ? 'Sound on' : 'Sound off';
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
  }
  function setOn(v, byUser) {
    on = !!v;
    sset(K_ON, on ? 'on' : 'off');
    render();
    if (byUser && typeof window.gtag === 'function') {
      try { window.gtag('event', on ? 'sound_on' : 'sound_off', { page_path: location.pathname }); } catch (e) {}
    }
    L(on ? 'on' : 'off', { byUser: !!byUser });
    clearTimeout(suspendTimer);
    if (on) {
      if (playing()) (ctx.resume ? ctx.resume() : Promise.resolve()).then(function () { ramp(master.gain, CFG.volume, CFG.resumeFade); });
      else resumeLoop();
    } else if (ctx) {
      ramp(master.gain, 0, CFG.fadeOut);
      savePos();
      suspendLater();
    }
  }
  /* 關掉聲音後讓 AudioContext 睡覺省電；但首頁蒙太奇還在用它當時鐘時先別睡 */
  function suspendLater() {
    clearTimeout(suspendTimer);
    suspendTimer = setTimeout(function () {
      if (on || !ctx || !ctx.suspend) return;
      if (window.ON_MONTAGE_BUSY) { suspendLater(); return; }
      ctx.suspend(); L('suspended');
    }, CFG.fadeOut * 1000 + 80);
  }
  function makeButton() {
    if (!document.body) return;
    if (!document.getElementById('on-sound-css')) {
      var css = document.createElement('style');
      css.id = 'on-sound-css';
      css.setAttribute('data-persist', '');
      css.textContent =
        '#on-sound{position:fixed;left:4px;bottom:0;z-index:150;margin:0;padding:10px 8px 10px 8px;' +
        'background:none;border:0;cursor:pointer;font-family:var(--font,inherit);font-size:12.8px;font-weight:400;' +
        'letter-spacing:.18em;line-height:1;color:rgba(255,255,255,.4);text-shadow:0 0 6px rgba(0,0,0,.55);' +
        '-webkit-tap-highlight-color:transparent;transition:color .2s}' +
        '#on-sound span{display:inline-block;border-bottom:.5px solid rgba(255,255,255,.18);padding-bottom:2px}' +
        '#on-sound:hover,#on-sound:focus-visible{color:rgba(255,255,255,.75);outline:none}' +
        '@media print{#on-sound{display:none}}';
      document.head.appendChild(css);
    }
    if (!btn) {
      btn = document.createElement('button');
      btn.id = 'on-sound';
      btn.type = 'button';
      btn.setAttribute('aria-label', 'Sound');
      btn.setAttribute('data-persist', '');
      btn.appendChild(document.createElement('span'));
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        gestureSeen = true;
        /* 狀態是開、但還沒出聲：這一下就是「開始播」，不是關掉 */
        if (on && !(playing() && running())) { resumeLoop(); return; }
        setOn(!on, true);
      });
    }
    if (btn.parentNode !== document.body) document.body.appendChild(btn);
    render();
  }

  /* ── 第一次互動：開始出聲 ── */
  function onGesture(e) {
    if (e && e.isTrusted !== false) gestureSeen = true;
    if (btn && e && e.target && btn.contains(e.target)) return;   /* 開關自己處理 */
    if (!on) return;
    if (playing()) {
      if (!running() && !hiddenPaused && ctx.resume) ctx.resume().then(function () { ramp(master.gain, CFG.volume, CFG.resumeFade); });
      return;
    }
    resumeLoop();
  }
  ['pointerdown', 'touchend', 'keydown', 'click'].forEach(function (t) {
    window.addEventListener(t, onGesture, { capture: true, passive: true });
  });

  /* ── 分頁切到背景：淡出暫停；回來：淡入 ── */
  document.addEventListener('visibilitychange', function () {
    if (!ctx) return;
    if (document.hidden) {
      savePos();
      if (running() && playing()) {
        hiddenPaused = true;
        ramp(master.gain, 0, 0.15);
        setTimeout(function () { if (document.hidden && ctx.suspend) { ctx.suspend(); L('hidden-suspend'); } }, 170);
      }
    } else if (hiddenPaused) {
      hiddenPaused = false;
      if (!on) return;
      (ctx.resume ? ctx.resume() : Promise.resolve()).then(function () { ramp(master.gain, CFG.volume, CFG.resumeFade); L('visible-resume'); });
    }
  });
  window.addEventListener('pagehide', savePos);
  window.addEventListener('pageshow', function (e) {
    if (e.persisted && on && ctx && playing() && ctx.resume) ctx.resume().then(function () { ramp(master.gain, CFG.volume, CFG.resumeFade); });
  });
  setInterval(function () { if (playing() && running() && !pend) savePos(); }, 1000);

  /* ── 對外 API ── */
  window.ONSound = {
    intro: intro,
    /* 單頁式換頁後由 nav.js 呼叫：照新網址決定要不要換歌，並把開關補回畫面 */
    page: function (path) {
      makeButton();
      var t = trackFor(path);
      if (t) switchTo(t);
    },
    track: function () { return pend ? pend.name : cur ? cur.name : null; },
    isOn: function () { return on; },
    set: function (v) { setOn(v, false); },
    ctx: function () { return ctx; },
    loopPos: function () { return posOf(cur); },
    CFG: CFG, BAR: BAR, INTRO_LEN: INTRO_LEN,
    _debug: function () { return { buf: buf, cur: cur, pend: pend, want: want, introSrc: !!introSrc }; }
  };

  /* ── 開場 ── */
  function boot() {
    makeButton();
    if (!on) return;
    if (introPendingOnPage()) {         /* 首頁等 Entrance：先把開場＋No.1 下載好 */
      Promise.all([load('intro'), load('no1')]).then(fixIntroTail, function () {});
      return;
    }
    load(want);
    if (!unlocked()) return;
    /* 瀏覽器本來就准出聲（少數情況）：直接開始 */
    if (ensureCtx() && ctx.state === 'running') resumeLoop();
    else if (ctx && ctx.resume) ctx.resume().then(function () { if (running()) resumeLoop(); }, function () {});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
