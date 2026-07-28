/* Zetith コラム 共通JS — 最小限・プログレッシブエンハンスメント
   JSが無効でも内容は読める（目次・FAQ・料金・症例の全文はHTMLに存在） */
(function () {
  'use strict';

  /* スクロール進捗バー */
  var bar = document.getElementById('progress');
  if (bar) {
    var upd = function () {
      var h = document.documentElement, b = document.body;
      var st = h.scrollTop || b.scrollTop;
      var sh = (h.scrollHeight || b.scrollHeight) - h.clientHeight;
      bar.style.width = (sh > 0 ? (st / sh * 100) : 0) + '%';
    };
    addEventListener('scroll', upd, { passive: true });
    addEventListener('resize', upd); upd();
  }

  /* ライト/ダーク切替 */
  var tt = document.getElementById('themeToggle');
  if (tt) tt.addEventListener('click', function () {
    var root = document.documentElement, c = root.getAttribute('data-theme');
    if (!c) c = matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light';
    root.setAttribute('data-theme', c === 'dark' ? 'light' : 'dark');
  });

  /* 目次：デスクトップは開いた状態に（モバイルは閉じたまま） */
  var toc = document.querySelector('details.toc');
  if (toc && matchMedia('(min-width:1024px)').matches) toc.open = true;

  /* カテゴリ絞り込み（一覧ページ） */
  var chips = document.querySelectorAll('.cat-chip');
  if (chips.length) {
    var cards = document.querySelectorAll('.article-card[data-cat]');
    var empty = document.querySelector('.grid-empty');
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var f = chip.getAttribute('data-filter'), n = 0;
        chips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
        cards.forEach(function (card) {
          var show = (f === 'all' || card.getAttribute('data-cat') === f);
          card.style.display = show ? '' : 'none';
          if (show) n++;
        });
        if (empty) empty.style.display = n ? 'none' : 'block';
      });
    });
  }

  /* 症例ギャラリー：タブ切替（正面・斜め・横）＋キーボード操作 */
  document.querySelectorAll('.case-gallery').forEach(function (gal) {
    var tabs = Array.prototype.slice.call(gal.querySelectorAll('[role="tab"]'));
    var panels = Array.prototype.slice.call(gal.querySelectorAll('[role="tabpanel"]'));
    if (!tabs.length) return;
    function select(i) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.setAttribute('tabindex', on ? '0' : '-1');
        if (panels[j]) panels[j].hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, ni = null;
        if (k === 'ArrowRight' || k === 'ArrowDown') ni = (i + 1) % tabs.length;
        else if (k === 'ArrowLeft' || k === 'ArrowUp') ni = (i - 1 + tabs.length) % tabs.length;
        if (ni !== null) { e.preventDefault(); tabs[ni].focus(); select(ni); }
      });
    });
    select(0);
  });

  /* スマホ固定CTAがある場合、本文下部に余白を確保 */
  if (document.querySelector('.sticky-cta')) document.body.classList.add('has-sticky-cta');
})();
