/* ════════ ON Design Lab｜進站聲音（全站共用）════════
   2026-09-28 v2.58。Mo 09-28 裁定：
   - 聲音「預設開」（狀態開；瀏覽器規定訪客碰畫面前不能出聲，所以實際出聲等第一次互動）。
   - 首頁第一次進站：點黑幕＝t 0，開場檔（4 小節，含聲音 logo）起播＋淡入，蒙太奇踩 90 BPM 拍點；
     10.667 秒無縫接循環檔（12 小節 32 秒，一直循環）。
   - 不點：自動進站；第一次互動（任何地方）時循環檔淡入，不播開場檔。
   - 換頁：記住循環檔播到第幾秒，新頁從那一秒淡入接著播；開場檔同一次瀏覽只播一次。
   - 背景分頁暫停、回來淡入。左下角細字 Sound on／Sound off，狀態記在 sessionStorage。
   - 不設 navigator.audioSession（保留 iOS 靜音鍵會讓網頁無聲）。

   首頁的蒙太奇透過 window.ONSound.intro() 拿到「歌曲時鐘」（以 AudioContext 時間為準），
   用它排拍點，不靠 setTimeout 累加。 */
(function () {
  'use strict';
  if (window.ONSound) return;

  /* ── 可調參數 ── */
  var CFG = {
    volume:      0.8,     /* 整體音量（0–1）。音檔本身 -16 LUFS */
    introFadeIn: 1.2,     /* 點黑幕後開場檔淡入秒數（首頁可用 intro({fadeIn}) 覆蓋） */
    resumeFade:  0.4,     /* 換頁／第一次互動／分頁回來 的淡入秒數 */
    fadeOut:     0.25,    /* 關掉或分頁切走時的淡出秒數 */
    waitAudio:   0.35     /* 點黑幕時音檔還沒準備好，最多等幾秒再先跑畫面 */
  };

  /* 音檔規格（90 BPM：一小節 2.6667 秒）。開場檔在重擊前多留 10 ms，不削掉起音。 */
  var BAR       = 60 / 90 * 4;
  var INTRO_PRE = 0.010;           /* 開場檔：檔案第 0.010 秒＝第一拍重擊（歌曲時間 0） */
  var INTRO_LEN = 4 * BAR;         /* 10.6667：開場 4 小節，歌曲時間到這裡接循環 */
  var LOOP_LEN  = 12 * BAR;        /* 32.000：循環 12 小節 */

  var base = (function () {
    var s = document.currentScript && document.currentScript.src;
    try { return new URL('../audio/', s || location.href).href; } catch (e) { return '/assets/audio/'; }
  })();
  var FILES = {
    intro: base + 'no1-intro-4bars-logo-20260928.m4a',
    loop:  base + 'no1-loop-12bars-20260928.m4a'
  };

  /* ── sessionStorage（私密視窗可能丟例外，全部包起來） ── */
  var K_ON = 'on.sound', K_POS = 'on.sound.pos', K_INTRO = 'on.sound.intro';
  function sget(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function sset(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }

  var on = sget(K_ON) !== 'off';                 /* 預設開 */
  var ctx = null, master = null;
  var buf = {}, bufLead = { intro: 0, loop: 0 }, loading = {};
  var introSrc = null, loopSrc = null;
  var loopZero = null;        /* 循環位置 0 對應的 ctx 時間 */
  var songZero = null;        /* 歌曲時間 0（第一拍）對應的 ctx 時間 */
  var hiddenPaused = false, suspendTimer = null;
  var introInFlight = false;  /* 點了黑幕、音檔還在準備：這段時間的其他互動只負責叫醒 AudioContext */
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

  function load(name) {
    if (buf[name]) return Promise.resolve(buf[name]);
    if (loading[name]) return loading[name];
    if (!ensureCtx()) return Promise.reject(new Error('no-webaudio'));
    loading[name] = fetch(FILES[name]).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.arrayBuffer();
    }).then(function (ab) {
      return new Promise(function (res, rej) {
        var p = ctx.decodeAudioData(ab, res, rej);      /* 舊 Safari 只有 callback 版 */
        if (p && p.then) p.then(res, rej);
      });
    }).then(function (b) {
      /* AAC 解碼後，有的瀏覽器會把編碼器前導（1024 樣本）留在開頭。
         比理論長度多出 20 ms 以上，就當作有前導，排程時跳過它。 */
      var expect = name === 'intro' ? INTRO_PRE + INTRO_LEN : LOOP_LEN;
      var extra = b.duration - expect;
      bufLead[name] = extra > 0.02 ? 1024 / 48000 : 0;
      buf[name] = b;
      L('decoded', { name: name, len: b.length, dur: +b.duration.toFixed(5), sr: b.sampleRate, lead: bufLead[name] });
      return b;
    });
    loading[name].catch(function (e) { L('load-fail', { name: name, err: String(e) }); loading[name] = null; });
    return loading[name];
  }

  /* 開場檔的結尾要剛好接到循環檔第一個樣本。
     2026-09-28 實測：Chrome 依 m4a 的 edit list 把開場檔解成 512448 樣本，比原稿 wav（512480）少最後 32 樣本（0.67 ms），
     直接接會在接縫留一小段靜音＋爆音。補法：把缺的尾巴用「開場最後一個樣本 → 循環第一個樣本」直線補滿，波形連續。
     哪個瀏覽器解得完整就不會動到。 */
  var introFixed = false;
  function fixIntroTail() {
    if (introFixed || !buf.intro || !buf.loop) return;
    introFixed = true;
    var b = buf.intro, sr = b.sampleRate;
    var need = Math.round((bufLead.intro + INTRO_PRE + INTRO_LEN) * sr);
    var miss = need - b.length;
    if (miss <= 0 || miss > sr * 0.01) { L('intro-tail', { miss: miss, fixed: false }); return; }
    var nb = ctx.createBuffer(b.numberOfChannels, need, sr);
    var loopFirst = Math.round(bufLead.loop * buf.loop.sampleRate);
    for (var c = 0; c < b.numberOfChannels; c++) {
      var src = b.getChannelData(c), dst = nb.getChannelData(c);
      dst.set(src);
      var a = src[src.length - 1];
      var z = buf.loop.getChannelData(Math.min(c, buf.loop.numberOfChannels - 1))[loopFirst];
      for (var i = 0; i < miss; i++) dst[b.length + i] = a + (z - a) * (i + 1) / (miss + 1);
    }
    buf.intro = nb;
    L('intro-tail', { miss: miss, fixed: true });
  }

  /* 「聽到的」ctx 時間：扣掉輸出延遲，畫面才會跟耳朵對上 */
  var lastHeard = 0;
  function heardNow() {
    if (!ctx) return 0;
    var t;
    if (ctx.getOutputTimestamp) {
      var ts = ctx.getOutputTimestamp();
      if (ts && ts.contextTime > 0 && ts.performanceTime > 0) {
        t = ts.contextTime + (performance.now() - ts.performanceTime) / 1000;
      }
    }
    if (t === undefined) t = ctx.currentTime - (ctx.outputLatency || ctx.baseLatency || 0);
    if (t < lastHeard) t = lastHeard;                  /* 只往前走 */
    if (t > ctx.currentTime) t = ctx.currentTime;      /* 不會比排程時鐘還快 */
    lastHeard = t;
    return t;
  }

  function running() { return ctx && ctx.state === 'running'; }

  function ramp(to, sec) {
    if (!master) return;
    var now = ctx.currentTime, g = master.gain;
    try { g.cancelScheduledValues(now); } catch (e) {}
    g.setValueAtTime(g.value, now);
    g.linearRampToValueAtTime(to, now + Math.max(0.01, sec));
  }

  function stopSources() {
    [introSrc, loopSrc].forEach(function (s) { if (s) { try { s.stop(); } catch (e) {} try { s.disconnect(); } catch (e) {} } });
    introSrc = loopSrc = null; loopZero = null;
  }

  /* 循環檔：在 ctx 時間 when 開始，從循環位置 pos 起播 */
  function startLoopAt(when, pos) {
    var b = buf.loop, lead = bufLead.loop;
    var s = ctx.createBufferSource();
    s.buffer = b;
    s.loop = true;
    s.loopStart = lead;
    s.loopEnd = lead + LOOP_LEN;
    s.connect(master);
    pos = ((pos % LOOP_LEN) + LOOP_LEN) % LOOP_LEN;
    s.start(when, lead + pos);
    loopSrc = s;
    loopZero = when - pos;
    L('loop-start', { when: +when.toFixed(4), pos: +pos.toFixed(3) });
  }

  function loopPos() {
    if (!ctx || loopZero === null) return null;
    var t = ctx.currentTime - loopZero;
    if (t < 0) return 0;
    return t % LOOP_LEN;
  }

  function savePos() {
    var p = loopPos();
    if (p !== null) sset(K_POS, p.toFixed(3));
  }

  function playing() { return !!(introSrc || loopSrc); }

  /* 換頁／第一次互動：循環檔從記住的秒數淡入 */
  function resumeLoop() {
    if (introInFlight) { if (ctx && ctx.resume) ctx.resume(); return; }
    if (!on || playing() || introPendingOnPage()) return;
    if (!ensureCtx()) return;
    var p = ctx.resume ? ctx.resume() : Promise.resolve();
    load('loop').then(function () {
      return p;
    }).then(function () {
      if (!on || playing() || !running() || introPendingOnPage()) return;
      var pos = parseFloat(sget(K_POS)) || 0;
      master.gain.setValueAtTime(0, ctx.currentTime);
      startLoopAt(ctx.currentTime + 0.03, pos);
      ramp(CFG.volume, CFG.resumeFade);
      sset(K_INTRO, 'done');          /* 聲音已經開始了，回首頁不再出現「輕觸進入」 */
      render();
    }).catch(function (e) { L('resume-fail', { err: String(e) }); });
  }

  /* 首頁黑幕還在等「輕觸進入」時，全站的「第一次互動」不搶著放循環檔 */
  function introPendingOnPage() { return window.ON_SOUND_INTRO === 'pending'; }

  /* ════ 首頁：點黑幕 ════
     回傳歌曲時鐘 clock.t()：第一拍＝0，單位秒；還沒開始時回傳 null。
     音檔準備好時以 AudioContext 為準；還沒準備好就先用 performance 時鐘跑畫面，
     音檔到了再從對應的位置接進來（仍然對拍）。 */
  function intro(opt) {
    opt = opt || {};
    var fadeIn = opt.fadeIn != null ? opt.fadeIn : CFG.introFadeIn;
    sset(K_INTRO, 'done');
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
    clock.ctx = function () { return ctx; };

    function goPerf() {
      if (clock.mode !== 'wait') return;
      clock.mode = 'perf';
      clock.perfZero = performance.now();
      L('intro-perf-clock', { waited: Math.round(clock.perfZero - perfTap) });
    }

    if (!withAudio) { goPerf(); return clock; }

    stopSources();
    introInFlight = true;
    var resumed = ctx.resume ? ctx.resume() : Promise.resolve();
    var fallback = setTimeout(goPerf, CFG.waitAudio * 1000);

    Promise.all([load('intro'), load('loop'), resumed]).then(function () {
      if (!running()) throw new Error('ctx-not-running');
      clearTimeout(fallback);
      fixIntroTail();
      introInFlight = false;
      if (!on) { goPerf(); return; }
      var now = ctx.currentTime, when = now + 0.05;
      /* 歌曲時間 s 在 ctx 時間 songZero + s 被「聽到」 */
      if (clock.mode === 'wait') {
        songZero = when;
      } else {
        /* 畫面已經先跑了：算出 when 那一刻畫面走到哪，音檔從那裡接 */
        var lat = (ctx.outputLatency || ctx.baseLatency || 0);
        var sAtWhen = (performance.now() - clock.perfZero) / 1000 + (when - now) + lat;
        songZero = when - sAtWhen;
      }
      var s0 = when - songZero;                  /* when 那一刻的歌曲時間 */
      master.gain.setValueAtTime(0, now);
      if (s0 < INTRO_LEN) {
        var src = ctx.createBufferSource();
        src.buffer = buf.intro;
        src.connect(master);
        var fileAt = bufLead.intro + INTRO_PRE;  /* 檔案裡「第一拍」的位置 */
        var startCtx = songZero - INTRO_PRE;     /* 前 10 ms 的起音也要播到 */
        var off = 0;
        if (startCtx < when) { off = when - startCtx; startCtx = when; }
        /* 只播到歌曲時間 INTRO_LEN 為止，後面交給循環檔（剛好接上，沒有縫） */
        src.start(startCtx, bufLead.intro + off, (fileAt + INTRO_LEN) - (bufLead.intro + off));
        introSrc = src;
        src.onended = function () { if (introSrc === src) introSrc = null; };
        startLoopAt(songZero + INTRO_LEN, 0);
      } else {
        startLoopAt(when, s0 - INTRO_LEN);
      }
      ramp(CFG.volume, fadeIn);
      clock.mode = 'audio';
      L('intro-audio', { songZero: +songZero.toFixed(4), s0: +s0.toFixed(4), outLat: ctx.outputLatency || 0, baseLat: ctx.baseLatency || 0 });
      render();
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
      if (playing()) {
        (ctx.resume ? ctx.resume() : Promise.resolve()).then(function () { ramp(CFG.volume, CFG.resumeFade); });
      } else {
        resumeLoop();
      }
    } else if (ctx) {
      ramp(0, CFG.fadeOut);
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
      ctx.suspend();
      L('suspended');
    }, CFG.fadeOut * 1000 + 80);
  }

  function makeButton() {
    if (btn || !document.body) return;
    var css = document.createElement('style');
    css.textContent =
      '#on-sound{position:fixed;left:4px;bottom:0;z-index:150;margin:0;padding:10px 8px 10px 8px;' +
      'background:none;border:0;cursor:pointer;font-family:var(--font,inherit);font-size:12.8px;font-weight:400;' +
      'letter-spacing:.18em;line-height:1;color:rgba(255,255,255,.4);text-shadow:0 0 6px rgba(0,0,0,.55);' +
      '-webkit-tap-highlight-color:transparent;transition:color .2s}' +
      '#on-sound span{display:inline-block;border-bottom:.5px solid rgba(255,255,255,.18);padding-bottom:2px}' +
      '#on-sound:hover,#on-sound:focus-visible{color:rgba(255,255,255,.75);outline:none}' +
      '@media print{#on-sound{display:none}}';
    document.head.appendChild(css);
    btn = document.createElement('button');
    btn.id = 'on-sound';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Sound');
    btn.appendChild(document.createElement('span'));
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      /* 狀態是開、但還沒出聲（還沒互動過）：這一下就是「開始播」，不是關掉 */
      if (on && !(playing() && running())) { resumeLoop(); return; }
      setOn(!on, true);
    });
    document.body.appendChild(btn);
    render();
  }

  /* ── 第一次互動：解鎖聲音 ── */
  function onGesture(e) {
    if (btn && e && e.target && btn.contains(e.target)) return;   /* 開關自己處理 */
    if (!on) return;
    if (playing()) {
      if (!running() && !hiddenPaused && ctx.resume) ctx.resume().then(function () { ramp(CFG.volume, CFG.resumeFade); });
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
        ramp(0, 0.15);
        setTimeout(function () { if (document.hidden && ctx.suspend) { ctx.suspend(); L('hidden-suspend'); } }, 170);
      }
    } else if (hiddenPaused) {
      hiddenPaused = false;
      if (!on) return;
      (ctx.resume ? ctx.resume() : Promise.resolve()).then(function () {
        ramp(CFG.volume, CFG.resumeFade);
        L('visible-resume');
      });
    }
  });

  /* 離開這頁前記住播到第幾秒 */
  window.addEventListener('pagehide', savePos);
  window.addEventListener('pageshow', function (e) {
    if (e.persisted && on && ctx && playing() && ctx.resume) {
      ctx.resume().then(function () { ramp(CFG.volume, CFG.resumeFade); });
    }
  });
  setInterval(function () { if (playing() && running()) savePos(); }, 1000);

  /* ── 對外 API（首頁蒙太奇用） ── */
  window.ONSound = {
    intro: intro,
    isOn: function () { return on; },
    set: function (v) { setOn(v, false); },
    ctx: function () { return ctx; },
    loopPos: loopPos,
    CFG: CFG,
    _debug: function () { fixIntroTail(); return { buf: buf, lead: bufLead }; },
    BAR: BAR, INTRO_LEN: INTRO_LEN, LOOP_LEN: LOOP_LEN
  };

  /* ── 開場 ── */
  function boot() {
    makeButton();
    if (!on) return;
    /* 預先下載：首頁等點黑幕時要開場＋循環；其他頁只要循環 */
    if (introPendingOnPage()) {
      Promise.all([load('intro'), load('loop')]).then(fixIntroTail, function () {});
      return;
    }
    load('loop');
    /* 同源換頁後，有的瀏覽器允許直接出聲（例如 Chrome 記得剛剛有互動過）：試一下 */
    if (ensureCtx() && ctx.state === 'running') resumeLoop();
    else if (ctx && ctx.resume) {
      ctx.resume().then(function () { if (running()) resumeLoop(); }, function () {});
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
