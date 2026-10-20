/* Öz Konya Hurda — site etkileşimleri */
(function () {
  'use strict';

  /* ---- Mobil menü ---- */
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- Fotoğraf yoksa yer tutucu göster ----
     img/ klasörüne gerçek fotoğrafları atınca bu otomatik devre dışı kalır. */
  function placeholder(label) {
    var svg =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">' +
      '<rect width="800" height="600" fill="#1F2E2B"/>' +
      '<rect x="0" y="0" width="800" height="600" fill="url(#g)" opacity=".5"/>' +
      '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0" stop-color="#A85423"/><stop offset="1" stop-color="#3E7A6A"/>' +
      '</linearGradient></defs>' +
      '<text x="400" y="305" font-family="Arial,sans-serif" font-size="30" font-weight="bold" ' +
      'fill="#E9E7E2" text-anchor="middle">' + label + '</text></svg>';
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  }

  document.querySelectorAll('img[data-fallback]').forEach(function (img) {
    img.addEventListener('error', function () {
      if (img.dataset.done) return;
      img.dataset.done = '1';
      img.src = placeholder(img.dataset.fallback || 'Fotoğraf');
    });
    if (img.complete && img.naturalWidth === 0) img.dispatchEvent(new Event('error'));
  });

  /* ---- Video yoksa poster/gradyan kalsın ---- */
  document.querySelectorAll('video[data-fallback]').forEach(function (v) {
    v.addEventListener('error', function () { v.style.display = 'none'; }, true);
  });

  /* ---- Galeri lightbox ---- */
  var box = document.querySelector('.lightbox');
  if (box) {
    var boxImg = box.querySelector('img');
    var items = Array.prototype.slice.call(document.querySelectorAll('.gallery button'));
    var index = 0;

    function show(i) {
      index = (i + items.length) % items.length;
      var src = items[index].querySelector('img');
      boxImg.src = src.currentSrc || src.src;
      boxImg.alt = src.alt;
    }
    function open(i) { show(i); box.classList.add('is-open'); document.body.style.overflow = 'hidden'; }
    function close() { box.classList.remove('is-open'); document.body.style.overflow = ''; }

    items.forEach(function (btn, i) {
      btn.addEventListener('click', function () { open(i); });
    });
    box.querySelector('.lightbox__close').addEventListener('click', close);
    box.querySelector('.lightbox__nav--prev').addEventListener('click', function () { show(index - 1); });
    box.querySelector('.lightbox__nav--next').addEventListener('click', function () { show(index + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }

  /* ---- Footer yılı ---- */
  var y = document.getElementById('yil');
  if (y) y.textContent = new Date().getFullYear();
})();
