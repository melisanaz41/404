#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog üreticisi.

Yeni bir blog yazısı eklemek için aşağıdaki YAZILAR listesine bir kayıt
ekleyip bu dosyayı çalıştırman yeterli:

    python3 tools/blog-uret.py

Bu, hem blog-<slug>.html sayfasını hem de blog.html listeleme sayfasını
yeniden üretir. Telefon/adres gibi bilgiler ayarlar.py dosyasından okunur.

Not: Bu betik blog-*.html dosyalarını ve blog.html'i SIFIRDAN yeniden yazar.
Bir yazıda elle değişiklik yaptıysan betiği çalıştırma, ya da değişikliği
YAZILAR listesindeki ilgili kayda taşı.
"""

import os
import sys
import json
from datetime import date

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ayarlar import *  # noqa

# --------------------------------------------------------------------------
# Sayfa iskeleti — sayfa-uret.py'deki üst bar / footer / alt çubukla birebir
# aynı, sadece gövde kısmı blog yazısına göre değişiyor.
# --------------------------------------------------------------------------

ISKELET_YAZI = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="google-site-verification" content="{google_dogrulama}" />
<title>{baslik}</title>
<meta name="description" content="{aciklama}">
<link rel="canonical" href="{site}/{dosya}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="TR-42">
<meta name="geo.placename" content="Kulu, Konya">
<meta property="og:type" content="article">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{firma}">
<meta property="og:title" content="{baslik}">
<meta property="og:description" content="{aciklama}">
<meta property="og:url" content="{site}/{dosya}">
<meta property="og:image" content="{site}/img/og-kapak.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%23A85423'/><text x='50' y='70' font-size='58' font-family='Arial Black,Arial' font-weight='900' fill='%23fff' text-anchor='middle'>S</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>

<header class="topbar">
  <div class="wrap topbar__in">
    <a class="brand" href="index.html">
      <span class="brand__mark">S</span>
      <span>
        <span class="brand__name">{firma}</span>
        <span class="brand__sub">Kulu / Konya · hurda alımı</span>
      </span>
    </a>
    <nav class="nav" aria-label="Ana menü">
      <a href="index.html#malzemeler">Ne alıyoruz</a>
      <a href="index.html#nasil">Nasıl işliyor</a>
      <a href="index.html#galeri">Galeri</a>
      <a href="index.html#konum">Konum</a>
      <a href="blog.html" aria-current="page">Blog</a>
      <a href="iletisim.html">İletişim</a>
    </nav>
    <a class="btn btn--primary" href="tel:{tel_link}">{tel_gosterim}</a>
    <button class="burger" aria-label="Menüyü aç" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<section class="section section--tight">
  <div class="wrap">
    <nav class="breadcrumb" aria-label="Konum">
      <a href="index.html">Ana sayfa</a><span aria-hidden="true">/</span>
      <a href="blog.html">Blog</a><span aria-hidden="true">/</span>
      <span>{kisa_baslik}</span>
    </nav>
    <div class="post-meta"><span>{tarih_gosterim}</span><span>·</span><span>{okuma}</span></div>
    <h1>{h1}</h1>
    <p class="lead">{spot}</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <article class="article">
{govde}
    </article>

    <div class="cta-box">
      <div>
        <h3>Elinizde bu türden bir hurda mı var?</h3>
        <p>Fotoğrafını WhatsApp'tan gönderin, aynı gün fiyat verelim.</p>
      </div>
      <div class="hero__cta">
        <a class="btn btn--primary" href="tel:{tel_link}">Hemen ara</a>
        <a class="btn btn--wa" href="https://wa.me/{wa}" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>

    <div class="related">
      <div class="head"><h2>İlgili yazılar</h2></div>
      <div class="links">
{ilgili}
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <h4>{firma}</h4>
        <p>Konya Kulu ve çevre ilçelerde hurda demir, bakır, alüminyum, pirinç, tarım makinesi ve hurda araç alımı. Yerinde söküm, kantarlı tartım, anında ödeme.</p>
        <p>{adres_duz}</p>
      </div>
      <div>
        <h4>Sayfalar</h4>
        <ul>
          <li><a href="index.html">Ana sayfa</a></li>
          <li><a href="hurdaci-kulu.html">Kulu hurdacı</a></li>
          <li><a href="hurda-demir.html">Hurda demir alımı</a></li>
          <li><a href="hurda-bakir-aluminyum.html">Bakır ve alüminyum</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="iletisim.html">İletişim</a></li>
        </ul>
      </div>
      <div>
        <h4>Bize ulaşın</h4>
        <ul>
          <li><a href="tel:{tel_link}">{tel_gosterim}</a></li>
          <li><a href="https://wa.me/{wa}" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:{eposta}">{eposta}</a></li>
          <li><a href="{ig}" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>&copy; <span id="yil">2026</span> {firma}. Tüm hakları saklıdır.</span>
      <span>Kulu hurdacı · Konya Kulu hurda alımı · geri dönüşüm</span>
    </div>
  </div>
</footer>

<nav class="callbar" aria-label="Hızlı iletişim">
  <a href="tel:{tel_link}">Ara</a>
  <a href="https://wa.me/{wa}" target="_blank" rel="noopener">WhatsApp</a>
  <a href="{yol}" target="_blank" rel="noopener">Yol tarifi</a>
</nav>

<script src="js/main.js"></script>
</body>
</html>
"""

ISKELET_LISTE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="google-site-verification" content="{google_dogrulama}" />
<title>Blog | Kulu Hurda ve Geri Dönüşüm Rehberi — {firma}</title>
<meta name="description" content="Kulu'da hurda demir, bakır, alüminyum, tarım makinesi fiyatları ve hurda satmadan önce bilinmesi gerekenler. Güncel rehber yazıları.">
<link rel="canonical" href="{site}/blog.html">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="TR-42">
<meta name="geo.placename" content="Kulu, Konya">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{firma}">
<meta property="og:title" content="Blog | Kulu Hurda ve Geri Dönüşüm Rehberi — {firma}">
<meta property="og:description" content="Kulu'da hurda demir, bakır, alüminyum, tarım makinesi fiyatları ve hurda satmadan önce bilinmesi gerekenler.">
<meta property="og:url" content="{site}/blog.html">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%23A85423'/><text x='50' y='70' font-size='58' font-family='Arial Black,Arial' font-weight='900' fill='%23fff' text-anchor='middle'>S</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Manrope:wght@500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<header class="topbar">
  <div class="wrap topbar__in">
    <a class="brand" href="index.html">
      <span class="brand__mark">S</span>
      <span>
        <span class="brand__name">{firma}</span>
        <span class="brand__sub">Kulu / Konya · hurda alımı</span>
      </span>
    </a>
    <nav class="nav" aria-label="Ana menü">
      <a href="index.html#malzemeler">Ne alıyoruz</a>
      <a href="index.html#nasil">Nasıl işliyor</a>
      <a href="index.html#galeri">Galeri</a>
      <a href="index.html#konum">Konum</a>
      <a href="blog.html" aria-current="page">Blog</a>
      <a href="iletisim.html">İletişim</a>
    </nav>
    <a class="btn btn--primary" href="tel:{tel_link}">{tel_gosterim}</a>
    <button class="burger" aria-label="Menüyü aç" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<section class="section section--dark section--tight">
  <div class="wrap">
    <h1>Kulu hurda ve geri dönüşüm rehberi</h1>
    <p class="lead">Fiyatlar nasıl belirlenir, hangi malzeme nereye satılır, hurdacıya vermeden önce nelere dikkat edilmeli — Kulu'ya özel, güncel yazılar.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="blog-grid">
{kartlar}
    </div>
  </div>
</section>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <h4>{firma}</h4>
        <p>Konya Kulu ve çevre ilçelerde hurda demir, bakır, alüminyum, pirinç, tarım makinesi ve hurda araç alımı. Yerinde söküm, kantarlı tartım, anında ödeme.</p>
        <p>{adres_duz}</p>
      </div>
      <div>
        <h4>Sayfalar</h4>
        <ul>
          <li><a href="index.html">Ana sayfa</a></li>
          <li><a href="hurdaci-kulu.html">Kulu hurdacı</a></li>
          <li><a href="hurda-demir.html">Hurda demir alımı</a></li>
          <li><a href="hurda-bakir-aluminyum.html">Bakır ve alüminyum</a></li>
          <li><a href="iletisim.html">İletişim</a></li>
        </ul>
      </div>
      <div>
        <h4>Bize ulaşın</h4>
        <ul>
          <li><a href="tel:{tel_link}">{tel_gosterim}</a></li>
          <li><a href="https://wa.me/{wa}" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:{eposta}">{eposta}</a></li>
          <li><a href="{ig}" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>&copy; <span id="yil">2026</span> {firma}. Tüm hakları saklıdır.</span>
      <span>Kulu hurdacı · Konya Kulu hurda alımı · geri dönüşüm</span>
    </div>
  </div>
</footer>

<nav class="callbar" aria-label="Hızlı iletişim">
  <a href="tel:{tel_link}">Ara</a>
  <a href="https://wa.me/{wa}" target="_blank" rel="noopener">WhatsApp</a>
  <a href="{yol}" target="_blank" rel="noopener">Yol tarifi</a>
</nav>

<script src="js/main.js"></script>
</body>
</html>
"""


def p(*metinler):
    return "\n".join('      <p>{}</p>'.format(m) for m in metinler)


def h2(baslik):
    return '      <h2>{}</h2>'.format(baslik)


def ul(maddeler):
    satirlar = "\n".join('        <li>{}</li>'.format(m) for m in maddeler)
    return '      <ul>\n{}\n      </ul>'.format(satirlar)


# --------------------------------------------------------------------------
# YAZILAR — yeni yazı eklemek için buraya kayıt ekle
# --------------------------------------------------------------------------

YAZILAR = [

    dict(
        slug="kulu-hurda-demir-fiyati-nasil-belirlenir",
        tag="Fiyat Rehberi",
        baslik="Kulu'da Hurda Demir Fiyatı Nasıl Belirlenir? | " + FIRMA,
        aciklama="Kulu'da hurda demir fiyatını etkileyen faktörler: cins, temizlik, "
                 "kalınlık ve günlük borsa değeri. Doğru fiyatı nasıl öğreneceğinizi anlatıyoruz.",
        h1="Kulu'da hurda demir fiyatı nasıl belirlenir?",
        kisa_baslik="Hurda demir fiyatı nasıl belirlenir",
        spot="\"Kulu'da hurda demir kaç para\" sorusunun tek bir cevabı yok. Fiyatı "
             "belirleyen dört ana faktörü ve doğru rakamı nasıl öğreneceğinizi anlatıyoruz.",
        okuma="4 dk okuma",
        tarih="2026-01-15",
        govde="\n".join([
            p("Kulu'da hurda demir fiyatı sorulduğunda tek bir rakam vermek doğru "
              "olmaz, çünkü fiyat malzemenin durumuna göre kilogram başına ciddi "
              "şekilde değişebilir. Aşağıda fiyatı belirleyen dört ana etkeni ve "
              "elinizdeki hurdanın hangi aralığa gireceğini nasıl anlayacağınızı anlattık."),

            h2("1. Demirin cinsi"),
            p("İnşaat demiri, sac, döküm parça ve talaş birbirinden farklı fiyatlandırılır. "
              "Kalın ve temiz konstrüksiyon parçaları genelde ince talaş ve çapaklı "
              "malzemeye göre daha yüksek fiyat alır, çünkü işlenmesi daha az emek gerektirir."),

            h2("2. Temizlik durumu"),
            p("Demirin üzerinde beton, ahşap, plastik ya da yalıtım malzemesi kaldıysa "
              "kilogram fiyatı düşer — çünkü bu yabancı maddeler tartıma dahil olup "
              "gerçek metal ağırlığını gizler. Ayrıştırılmış, temiz gelen yük her zaman "
              "daha iyi fiyat alır. Büyük bir yükünüz varsa, mümkünse çivi, ahşap ve "
              "beton parçalarını ayırarak getirmeniz faydanıza olur."),

            h2("3. Kalınlık ve miktar"),
            p("Kalın sac ve profil, ince telden daha değerlidir. Ayrıca tonajlı "
              "işlerde (bir fabrika ya da şantiye tasfiyesi gibi) toplu alım "
              "yapıldığı için kilogram fiyatı genelde küçük miktarlara göre daha "
              "avantajlı olur."),

            h2("4. Günlük borsa değeri"),
            p("Demir fiyatı, uluslararası hurda metal piyasasındaki hareketlere bağlı "
              "olarak haftalık, bazen günlük değişir. Geçen ay duyduğunuz bir rakam "
              "bugün geçerli olmayabilir. Bu yüzden en doğru bilgiyi almanın yolu, "
              "aradığınız gün telefonla sormaktan geçiyor."),

            h2("Kulu'da en sık gelen demir hurdası türleri"),
            ul([
                "İnşaat ve tadilat artığı nervürlü demir, kalıp demiri, kiriş ve köşebent",
                "Ahır, ağıl ve sera konstrüksiyonları",
                "Kazan, kalorifer peteği, boru ve sac artıkları",
                "Beyaz eşya ve klima dış üniteleri — bunlarda bakır/alüminyum içerik "
                "ayrıştırıldığı için fiyat düz demirin üzerine çıkar",
            ]),

            h2("Doğru fiyatı en hızlı nasıl öğrenirsiniz"),
            p("Elinizdeki demiri anlatan birkaç cümle ya da WhatsApp'tan çektiğiniz "
              "birkaç fotoğraf, telefonda size o günkü gerçek fiyat aralığını "
              "söylememiz için yeterli. Tartım kantarımızda, sizin gözünüzün önünde "
              "yapılır; söylenen rakamla tartımdan çıkan sonuç arasında sürpriz olmaz."),
        ]),
        ilgili=["kulu-koylerinde-en-cok-cikan-hurda-turleri",
                "hurdaciya-satmadan-once-dikkat-edilmesi-gerekenler"],
    ),

    dict(
        slug="kulu-hurda-traktor-tarim-makinesi-satisi",
        tag="Tarım",
        baslik="Kulu'da Hurda Traktör ve Tarım Makinesi Nasıl Satılır? | " + FIRMA,
        aciklama="Kulu'da ömrünü tamamlamış traktör, biçerdöver, römork ve pulluk nasıl "
                 "hurdaya ayrılır? Süreç, evrak ve fiyatı etkileyen faktörler.",
        h1="Kulu'da hurda traktör ve tarım makinesi nasıl satılır?",
        kisa_baslik="Hurda traktör ve tarım makinesi satışı",
        spot="Tarlada duran, artık çalışmayan bir traktör ya da biçerdöver aslında "
             "nakde çevrilebilir bir değer. Süreç nasıl işliyor, anlatıyoruz.",
        okuma="5 dk okuma",
        tarih="2026-01-22",
        govde="\n".join([
            p("Kulu ve çevre köylerde yıllarca kullanılıp artık ekonomik ömrünü "
              "tamamlamış traktör, biçerdöver, römork ve pulluk gibi tarım makineleri "
              "sık karşılaştığımız bir durum. Bu makineler çoğu zaman yıllarca bahçede "
              "ya da ahırın yanında beklerken, aslında içindeki demir, bakır ve "
              "alüminyum parçalar doğrudan değerlendirilebilir."),

            h2("Hangi tarım makineleri hurdaya ayrılır"),
            ul([
                "Motoru arızalanmış ya da yenileme maliyeti kullanım değerini aşan traktörler",
                "Hasat sonrası kullanım dışı kalan biçerdöver parçaları",
                "Kırık ya da eskimiş römork, pulluk, mibzer ve çizel",
                "Sulama sistemlerinde kullanılan dalgıç pompa motorları",
            ]),

            h2("Evrak konusunda dikkat edilmesi gerekenler"),
            p("Ruhsatlı bir aracı (traktör gibi) hurdaya ayırmadan önce resmî "
              "prosedürün nasıl işlediği il ve ilçeye göre küçük farklılıklar "
              "gösterebilir; bu yüzden kesin adımlar için ilgili trafik tescil "
              "birimine ya da noterinize danışmanızı öneririz. Biz kendi tarafımızdan, "
              "alım sürecinde gereken evrak takibinde size eşlik ediyor ve süreci "
              "mümkün olduğunca sorunsuz hale getirmeye çalışıyoruz."),

            h2("Tarlada söküm nasıl işliyor"),
            p("Makine tarlada, harmanda ya da ahırın yanında duruyorsa, aracımızla "
              "yerinde söküm yapıyoruz. Büyük parçaları kesip taşınabilir hale "
              "getirmek, yükleme ve nakliye tamamen bize ait; sizden ek bir ücret "
              "talep etmiyoruz. Çalışma bitince alanı temiz bırakıyoruz."),

            h2("Fiyatı etkileyen faktörler"),
            ul([
                "Toplam ağırlık — büyük bir traktör gövdesi küçük parçalara göre "
                "daha yüksek toplam tutar getirir",
                "Motor ve şanzıman gibi parçaların sökülüp ayrı değerlendirilebilir "
                "olması",
                "Üzerindeki lastik, akü ve elektronik aksamın durumu",
                "Bakır içeren elektrik tesisatı ve motor sargılarının ayrıştırılabilirliği",
            ]),

            h2("En doğru yaklaşım"),
            p("Elinizdeki makinenin birkaç fotoğrafını WhatsApp'tan gönderirseniz, "
              "telefonda tahmini bir fiyat aralığı verip, uygun bulursanız aynı gün "
              "ya da ertesi gün ekibimizi gönderebiliriz. Tartım ve ödeme, söküm "
              "tamamlandıktan hemen sonra yerinde yapılır."),
        ]),
        ilgili=["kulu-sulama-borusu-aluminyum-hurda-fiyati",
                "kulu-koylerinde-en-cok-cikan-hurda-turleri"],
    ),

    dict(
        slug="kulu-sulama-borusu-aluminyum-hurda-fiyati",
        tag="Sulama",
        baslik="Kulu'da Sulama Borusu ve Alüminyum Hurda Fiyatı | " + FIRMA,
        aciklama="Kulu'da alüminyum sulama borusu, rakor ve dalgıç pompa hurdası nasıl "
                 "değerlendirilir? Fiyatı etkileyen temizlik ve ayrıştırma detayları.",
        h1="Kulu'da sulama borusu ve alüminyum hurda fiyatı",
        kisa_baslik="Sulama borusu ve alüminyum hurda fiyatı",
        spot="Alüminyum sulama borusu, Kulu'da en sık karşılaştığımız hurda "
             "kalemlerinden biri. Fiyatı neyin belirlediğini anlatıyoruz.",
        okuma="4 dk okuma",
        tarih="2026-01-29",
        govde="\n".join([
            p("Kulu'nun tarımsal yapısı nedeniyle en sık aldığımız kalemlerden biri "
              "alüminyum sulama borusu ve rakorları. Sezon sonunda ya da sulama "
              "sistemi yenilendiğinde tarlada biriken bu borular, doğru "
              "değerlendirildiğinde ciddi bir gelire dönüşebiliyor."),

            h2("Neden bu kadar değerli"),
            p("Alüminyum, demire göre çok daha yüksek kilogram fiyatına sahip bir "
              "metal. Sulama borusu genelde saf alüminyumdan üretildiği için, temiz "
              "geldiğinde iyi bir fiyat alır — özellikle karışık gelen demir "
              "hurdasına göre kilogram başına belirgin bir fark oluşur."),

            h2("Temizlik fiyatı doğrudan etkiliyor"),
            p("Borunun içinde kalan toprak ve çamur, tartımda gerçek alüminyum "
              "ağırlığını gizlediği için fiyatı aşağı çeker. Mümkünse yükleme "
              "öncesi boruları silkeleyip içini boşaltmanız faydanıza olur; "
              "gerekirse bu işlemi ekibimiz sizinle birlikte yapıyor."),

            h2("Rakor ve conta parçaları ayrı değerlendirilir"),
            p("Sulama hattında bulunan plastik contalar ve bazı bağlantı parçaları "
              "alüminyumdan farklı fiyatlandırılır. Tartım sırasında bu parçaları "
              "ayırarak her birini kendi doğru fiyatından hesaplıyoruz; karışık "
              "geldiğinde de sorun değil, ayrıştırmayı biz yapıyoruz."),

            h2("Dalgıç pompa motorları"),
            p("Sulama sistemlerinde kullanılan dalgıç pompaların içinde bakır "
              "sargı bulunur. Motor gövdesi ayrı, içindeki bakır sargı ayrı "
              "fiyatlandırıldığı için, pompayı parçalamadan olduğu gibi "
              "getirmeniz genelde daha pratik ve sizin için daha kârlı olur."),

            h2("Sezon sonu toplu kaldırma"),
            p("Sulama sezonu bittiğinde ya da sistem yenilendiğinde tarlada "
              "toplanan büyük miktarlardaki boru hatları için önceden randevu "
              "alarak aracımızı planlı şekilde gönderebiliyoruz. Bu, hem sizin "
              "için hem bizim için en verimli çalışma şekli."),
        ]),
        ilgili=["hurda-bakir-aluminyum-fiyat-farki",
                "kulu-hurda-traktor-tarim-makinesi-satisi"],
    ),

    dict(
        slug="yurtdisindan-kulu-ev-bosaltma-tasfiye",
        tag="Ev Boşaltma",
        baslik="Yurt Dışındayken Kulu'daki Evinizi Nasıl Boşalttırırsınız? | " + FIRMA,
        aciklama="Yurt dışında yaşayan Kulu'lular için kapalı ev boşaltma ve metal "
                 "tasfiyesi süreci adım adım. Uzaktan nasıl takip edebileceğinizi anlatıyoruz.",
        h1="Yurt dışındayken Kulu'daki evinizi nasıl boşalttırırsınız?",
        kisa_baslik="Yurt dışından ev boşaltma süreci",
        spot="Kulu'da boş duran bir ev ya da miras kalan bir mülkün tasfiyesi, "
             "yurt dışındayken de güvenle ve uzaktan takip edilerek yapılabilir.",
        okuma="4 dk okuma",
        tarih="2026-02-05",
        govde="\n".join([
            p("Kulu'da pek çok aile yurt dışında yaşıyor ve zaman zaman ilçedeki "
              "bir ev, artık kimsenin oturmadığı halde kapalı duruyor. Evin "
              "içindeki eski eşyaların, metal aksamın ve kullanılmayan malzemelerin "
              "tasfiyesi bu durumda genelde ertelenen bir iş haline geliyor. Bu "
              "süreci uzaktan da güvenle yönetebileceğiniz bir düzen kurduk."),

            h2("Süreç nasıl işliyor"),
            p("Genelde bir yakınınız ya da evin anahtarına ulaşabilen bir kişi "
              "bizimle telefon ya da WhatsApp üzerinden iletişime geçiyor. Evin "
              "durumunu ve içeriğini kısaca anlatmanız, mümkünse birkaç fotoğraf "
              "göndermeniz yeterli oluyor. Buna göre size tahmini bir bilgi veriyor, "
              "uygun bir tarihte ekibimizi gönderiyoruz."),

            h2("Çalışma sırasında bilgilendirme"),
            p("Çalışma günü, evden çıkan malzemenin fotoğraf ve videosunu "
              "WhatsApp üzerinden paylaşarak süreci uzaktan takip etmenizi "
              "sağlıyoruz. Tartım tamamlandığında sonucu da aynı şekilde "
              "iletiyoruz, böylece yurt dışındayken de neyin ne kadar "
              "değerlendirildiğini görebiliyorsunuz."),

            h2("Hangi malzemeler değerlendirilir"),
            ul([
                "Eski kalorifer peteği, boru ve kombi",
                "Pencere ve kapı doğramaları",
                "Beyaz eşya ve elektronik aletler",
                "Mutfak ve bahçedeki metal eşyalar",
                "Evin bahçesinde ya da damında biriken metal artıklar",
            ]),

            h2("Ödeme nasıl yapılır"),
            p("Yurt dışındaysanız nakit ödeme pratik olmayacağı için genelde banka "
              "havalesi tercih ediliyor. Tartım tamamlandığı anda, sizin ya da "
              "yetki verdiğiniz yakınınızın onayıyla ödeme gerçekleştiriliyor."),

            h2("Güven konusunda"),
            p("Evinize bir yabancının girmesi doğal olarak endişe verici bir "
              "durum. Bu yüzden çalışma boyunca şeffaf iletişimi ve fotoğraflı "
              "bilgilendirmeyi önemsiyoruz — anlaşmadan önce sorularınızı "
              "telefonda cevaplamaktan memnuniyet duyarız."),
        ]),
        ilgili=["kulu-koylerinde-en-cok-cikan-hurda-turleri",
                "hurdaciya-satmadan-once-dikkat-edilmesi-gerekenler"],
    ),

    dict(
        slug="hurda-bakir-aluminyum-fiyat-farki",
        tag="Karşılaştırma",
        baslik="Hurda Bakır ile Alüminyum Arasındaki Fiyat Farkı Neden Bu Kadar Büyük? | " + FIRMA,
        aciklama="Bakır ve alüminyum hurdanın kilogram fiyatı neden bu kadar farklı? "
                 "Sebebini ve karışık gelen hurdada doğru değerlendirmenin önemini anlatıyoruz.",
        h1="Hurda bakır ile alüminyum arasındaki fiyat farkı neden bu kadar büyük?",
        kisa_baslik="Bakır ve alüminyum fiyat farkı",
        spot="Elindeki hurdanın bakır mı alüminyum mu olduğunu bilmeyen pek çok kişi "
             "aradan geçen fiyat farkına şaşırıyor. Sebebini açıklıyoruz.",
        okuma="3 dk okuma",
        tarih="2026-02-12",
        govde="\n".join([
            p("Hurda getiren pek çok kişi, bakırın alüminyuma göre neden bu kadar "
              "yüksek fiyattan alındığını merak ediyor. Aradaki fark rastgele "
              "değil; iki metalin doğadaki bulunma oranından kullanım alanlarına "
              "kadar birkaç somut sebebi var."),

            h2("Bakırın değerli olmasının sebebi"),
            p("Bakır, elektrik iletkenliği çok yüksek bir metal ve dünya genelinde "
              "çıkarılabilir rezervi sınırlı. Bu yüzden birincil üretim (madenden "
              "çıkarma) maliyeti yüksek, hurdadan geri kazanım ise nispeten daha "
              "ucuz ve verimli. Bu durum hurda bakırın kilogram fiyatını sürekli "
              "yüksek tutuyor."),

            h2("Alüminyum neden farklı fiyatlanıyor"),
            p("Alüminyum de değerli bir metal, ama doğada daha bol bulunuyor ve "
              "üretim süreci bakıra göre farklı bir maliyet yapısına sahip. Bu "
              "yüzden kilogram fiyatı bakırın belirgin şekilde altında kalıyor — "
              "yine de demire göre çok daha değerli olduğunu unutmamak lazım."),

            h2("Karışık gelen hurdada ayrıştırma neden önemli"),
            p("Bir yükte hem bakır hem alüminyum hem de demir parçalar varsa, "
              "hepsini tek fiyattan değerlendirmek sizin aleyhinize olur. Bu "
              "yüzden tartımdan önce ayrıştırma yapıyor, her metali kendi gerçek "
              "fiyatından hesaplıyoruz. İşlem sizin gözünüzün önünde yapılır."),

            h2("Kablo örneği"),
            p("Elektrik kablosu bu farkın en somut göründüğü örneklerden biri: "
              "dışı plastik yalıtım, içi bakır tel. Kabloyu soyup soymamanın "
              "fiyata etkisini ayrı bir yazıda detaylı anlattık — kısaca, hangi "
              "yöntemin sizin için daha kârlı olduğunu telefonda birlikte "
              "hesaplıyoruz."),
        ]),
        ilgili=["hurda-kablo-soyulmus-mu-soyulmamis-mi-satilmali",
                "kulu-sulama-borusu-aluminyum-hurda-fiyati"],
    ),

    dict(
        slug="kulu-koylerinde-en-cok-cikan-hurda-turleri",
        tag="Bölge",
        baslik="Kulu ve Köylerinde En Çok Çıkan Hurda Türleri | " + FIRMA,
        aciklama="Kulu merkez, köyler ve sanayi sitesinde en sık karşılaştığımız hurda "
                 "türleri neler? Bölgeye göre değişen hurda profilini anlatıyoruz.",
        h1="Kulu ve köylerinde en çok çıkan hurda türleri",
        kisa_baslik="Kulu'da en çok çıkan hurda türleri",
        spot="Kulu merkezde, köylerde ve sanayi sitesinde çıkan hurda birbirinden "
             "oldukça farklı. Bölgeye göre neyin daha sık geldiğini anlatıyoruz.",
        okuma="4 dk okuma",
        tarih="2026-02-19",
        govde="\n".join([
            p("Yıllardır Kulu ve bağlı köylerde çalışırken bölgeye göre hurda "
              "profilinin belirgin şekilde farklılaştığını gördük. Merkez "
              "mahallede karşılaştığımız hurda ile bir köyde ya da sanayi "
              "sitesinde çıkan hurda çoğu zaman birbirinden oldukça farklı."),

            h2("Merkez mahallelerde"),
            p("Kulu merkezde en sık aldığımız kalemler ev tadilatı ve yenileme "
              "sonrası çıkan malzemeler: eski kalorifer peteği ve boruları, "
              "kombi, pencere doğraması, mutfak dolabı metalleri ve kullanım "
              "dışı kalan beyaz eşyalar. Apartman ve müstakil ev tasfiyeleri "
              "de bu kategoriye giriyor."),

            h2("Köylerde"),
            p("Köylerde tablo tamamen değişiyor. En sık karşılaştığımız kalemler "
              "tarım makineleri: traktör ve römork parçaları, pulluk, mibzer, "
              "sulama boruları ve dalgıç pompa motorları. Ayrıca ahır ve ağıl "
              "yapılarının demir aksamı, sera konstrüksiyonları da köylerde "
              "sık gördüğümüz kalemler."),

            h2("Sanayi sitesinde"),
            p("Kulu sanayi sitesindeki atölyelerden ise daha düzenli, tekrarlayan "
              "bir hurda akışı oluyor: üretim fireleri, tezgâh ve hat sökümü "
              "parçaları, metal talaş ve kesim artıkları. Bu tür işlerde genelde "
              "sözleşmeli ve düzenli günlerde çalışıyoruz."),

            h2("Mevsimsel farklar"),
            p("Hasat döneminin bitişiyle birlikte tarım makinesi ve sulama "
              "ekipmanı hurdası biraz daha sık gelme eğiliminde oluyor. Kış "
              "öncesinde ise ev tadilatı ve bakım işleri artıyor. Bu genel bir "
              "gözlem; elinizdeki hurdayı yılın hangi ayında getirdiğinizin "
              "fiyata doğrudan bir etkisi yok, borsa değeri o günkü rakamı "
              "belirliyor."),
        ]),
        ilgili=["kulu-hurda-demir-fiyati-nasil-belirlenir",
                "kulu-hurda-traktor-tarim-makinesi-satisi"],
    ),

    dict(
        slug="hurdaciya-satmadan-once-dikkat-edilmesi-gerekenler",
        tag="Güvenlik",
        baslik="Hurdacıya Satmadan Önce Nelere Dikkat Etmeli? | " + FIRMA,
        aciklama="Hurdanızı satarken dolandırılmamak için tartım, fiyat ve ödeme "
                 "konusunda dikkat etmeniz gereken pratik noktalar.",
        h1="Hurdacıya satmadan önce nelere dikkat etmeli?",
        kisa_baslik="Hurdacıya satmadan önce dikkat edilmesi gerekenler",
        spot="Hurda satarken haksız bir tartıma ya da belirsiz bir fiyata maruz "
             "kalmamak için birkaç basit kontrol yeterli. Neye dikkat etmeli, anlatıyoruz.",
        okuma="4 dk okuma",
        tarih="2026-02-26",
        govde="\n".join([
            p("Hurda satmak çoğu insan için sık yapılan bir işlem değil, bu "
              "yüzden nelere dikkat edilmesi gerektiği net olmayabiliyor. "
              "Aşağıdaki birkaç kontrol, hem gönlünüzün rahat etmesini hem de "
              "adil bir fiyat almanızı sağlar."),

            h2("Tartımı yakından takip edin"),
            p("Güvenilir bir hurdacı, tartımı sizin gözünüzün önünde, kantarın "
              "dijital ekranını görebileceğiniz şekilde yapar. Tartım sırasında "
              "ekrana bakmaktan çekinmeyin; bu gayet normal ve beklenen bir "
              "davranıştır."),

            h2("Fiyatı önceden netleştirin"),
            p("Mümkünse malzemenizi telefonda ya da WhatsApp'tan fotoğrafla "
              "anlatıp yaklaşık bir fiyat aralığı alın. Ekip geldiğinde "
              "söylenen aralıkla tartım sonucu arasında büyük bir fark "
              "çıkıyorsa, bunun sebebini sormaktan çekinmeyin."),

            h2("Ödemenin ne zaman yapıldığına dikkat edin"),
            p("Düzgün çalışan bir hurdacı, tartım tamamlanır tamamlanmaz ödemeyi "
              "yapar — nakit ya da anlaştığınız şekilde havale olarak. \"Sonra "
              "göndeririz\" gibi belirsiz ifadeler sizi rahatsız ediyorsa, "
              "ödemenin ne zaman yapılacağını net olarak sormanız yerinde olur."),

            h2("Kurumsal alımlarda evrak isteyin"),
            p("Şirket adına ya da kurumsal bir tasfiye yapıyorsanız, faturalı "
              "çalışan bir hurdacıyla işlem yapmak ileride çıkabilecek "
              "belirsizlikleri önler. Bu konuyu işleme başlamadan önce "
              "netleştirmek en sağlıklısı."),

            h2("Güvenilir bir hurdacıyı nasıl ayırt edersiniz"),
            ul([
                "Telefonda net bir fiyat aralığı verebiliyor mu",
                "Tartımı sizinle birlikte, açık şekilde yapıyor mu",
                "Söküm ve nakliye için ek, önceden söylenmemiş bir ücret talep "
                "ediyor mu",
                "Yorumları ve geçmiş işleri (örneğin Google profili üzerinden) "
                "kontrol edilebiliyor mu",
            ]),

            p("Bu birkaç basit kontrol, hem büyük hem küçük hurda satışlarında "
              "işinizi kolaylaştırır. Aklınıza takılan bir soru olursa, işleme "
              "başlamadan önce sormaktan çekinmeyin."),
        ]),
        ilgili=["kulu-hurda-demir-fiyati-nasil-belirlenir",
                "yurtdisindan-kulu-ev-bosaltma-tasfiye"],
    ),

    dict(
        slug="hurda-kablo-soyulmus-mu-soyulmamis-mi-satilmali",
        tag="Kablo",
        baslik="Hurda Kablo Soyulmuş mu Soyulmamış mı Satılmalı? | " + FIRMA,
        aciklama="Elektrik kablosu hurdasını soyup soymamak fiyatı nasıl etkiler? "
                 "Hangi durumda hangisi daha kârlı, açıklıyoruz.",
        h1="Hurda kablo soyulmuş mu soyulmamış mı satılmalı?",
        kisa_baslik="Kablo soyulmuş mu soyulmamış mı satılmalı",
        spot="Kablo hurdasını soyup soymamak konusunda net bir kural yok — durumunuza "
             "göre değişiyor. İki yöntemin avantajlarını karşılaştırıyoruz.",
        okuma="3 dk okuma",
        tarih="2026-03-05",
        govde="\n".join([
            p("Elektrik kablosu hurdası getiren pek çok kişi, kabloyu soyup "
              "soymamanın daha kârlı olup olmadığını soruyor. Net bir kural "
              "yok; hangisinin sizin için daha uygun olduğu elinizdeki "
              "miktara ve zamanınıza bağlı."),

            h2("Soyulmuş kablonun avantajı"),
            p("Kablonun içindeki saf bakır ortaya çıktığında, bakır fiyatından "
              "değerlendirilir — bu genelde kilogram başına daha yüksek bir "
              "rakam demektir. Küçük miktarlarda ve vaktiniz varsa, soyarak "
              "getirmek kilogram fiyatını artırabilir."),

            h2("Soyulmamış kablonun avantajı"),
            p("Kabloyu elle soymak zaman ve emek gerektirir; büyük miktarlarda "
              "bu iş günler sürebilir. Soyulmamış kablo kilogram üzerinden "
              "biraz daha düşük fiyattan değerlendirilse de, zaman "
              "kaybetmeden aynı gün elinizden çıkarmış olursunuz. Kesit ve "
              "yalıtım kalınlığına göre bakır oranı hesaplanarak adil bir "
              "fiyat veriyoruz."),

            h2("Kabloyu yakarak soymayın"),
            p("Bazı yerlerde kabloyu ateşle yakarak yalıtımdan ayırma yöntemi "
              "uygulandığını duyuyoruz. Bu yöntem hem çevre kirliliğine yol "
              "açtığı hem de yanık dumanı sağlığa zararlı olduğu için "
              "önermiyoruz. İster soyulmuş ister soyulmamış getirin, biz her "
              "iki durumda da adil bir fiyat hesaplıyoruz."),

            h2("Hangi durumda hangisi daha kârlı"),
            p("Küçük miktarda, saf ve kalın kesitli kablonuz varsa soyarak "
              "getirmek genelde daha kârlı çıkar. Büyük miktarda karışık "
              "kablonuz varsa, zaman kaybetmeden olduğu gibi getirmeniz daha "
              "pratik olur. Emin değilseniz, elinizdeki kabloyu anlatın, "
              "hangi yöntemin sizin için daha avantajlı olduğunu telefonda "
              "birlikte hesaplayalım."),
        ]),
        ilgili=["hurda-bakir-aluminyum-fiyat-farki",
                "kulu-hurda-demir-fiyati-nasil-belirlenir"],
    ),
]


def yazi_jsonld(y):
    dosya = "blog-{}.html".format(y["slug"])
    veri = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "mainEntityOfPage": {"@type": "WebPage", "@id": "{}/{}".format(SITE, dosya)},
        "headline": y["h1"],
        "description": y["aciklama"],
        "image": "{}/img/galeri-1.jpg".format(SITE),
        "datePublished": y["tarih"],
        "dateModified": y["tarih"],
        "inLanguage": "tr-TR",
        "author": {"@type": "Organization", "name": FIRMA, "url": SITE + "/"},
        "publisher": {
            "@type": "Organization",
            "name": FIRMA,
            "url": SITE + "/",
            "sameAs": [IG],
        },
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog.html"},
            {"@type": "ListItem", "position": 3, "name": y["kisa_baslik"], "item": SITE + "/" + dosya},
        ],
    }
    return json.dumps(veri, ensure_ascii=False, indent=2) + "\n</script>\n<script type=\"application/ld+json\">\n" \
        + json.dumps(breadcrumb, ensure_ascii=False, indent=2)


def ilgili_kartlar(yazi, tumu):
    sozluk = {y["slug"]: y for y in tumu}
    parcalar = []
    for slug in yazi["ilgili"]:
        ilgili_yazi = sozluk.get(slug)
        if not ilgili_yazi:
            continue
        parcalar.append(
            '        <a class="link-card" href="blog-{slug}.html">'
            '<strong>{baslik}</strong><span>{spot}</span></a>'.format(
                slug=slug, baslik=ilgili_yazi["kisa_baslik"], spot=ilgili_yazi["spot"][:80] + "…"
            )
        )
    return "\n".join(parcalar)


def tarih_uzun(iso):
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    y, a, g = [int(x) for x in iso.split("-")]
    return "{} {} {}".format(g, aylar[a - 1], y)


def uret():
    for y in YAZILAR:
        dosya = "blog-{}.html".format(y["slug"])
        html = ISKELET_YAZI.format(
            baslik=y["baslik"], aciklama=y["aciklama"], dosya=dosya,
            h1=y["h1"], kisa_baslik=y["kisa_baslik"], spot=y["spot"],
            okuma=y["okuma"], tarih_gosterim=tarih_uzun(y["tarih"]),
            govde=y["govde"], ilgili=ilgili_kartlar(y, YAZILAR),
            jsonld=yazi_jsonld(y),
            site=SITE, firma=FIRMA, tel_link=TEL_LINK, tel_gosterim=TEL_GOSTERIM,
            wa=WA, ig=IG, eposta=EPOSTA, adres_duz=ADRES_DUZ, yol=YOL_TARIFI,
            google_dogrulama=GOOGLE_DOGRULAMA,
        )
        with open(os.path.join(KOK, dosya), "w", encoding="utf-8") as f:
            f.write(html)
        print("yazildi:", dosya)

    kartlar = []
    for y in YAZILAR:
        kartlar.append(
            '      <a class="blog-card" href="blog-{slug}.html">\n'
            '        <span class="blog-card__tag">{tag}</span>\n'
            '        <h3>{baslik}</h3>\n'
            '        <p>{spot}</p>\n'
            '        <span class="blog-card__more">Devamını oku →</span>\n'
            '      </a>'.format(slug=y["slug"], tag=y["tag"], baslik=y["kisa_baslik"], spot=y["spot"])
        )
    liste_html = ISKELET_LISTE.format(
        kartlar="\n".join(kartlar),
        site=SITE, firma=FIRMA, tel_link=TEL_LINK, tel_gosterim=TEL_GOSTERIM,
        wa=WA, ig=IG, eposta=EPOSTA, adres_duz=ADRES_DUZ, yol=YOL_TARIFI,
        google_dogrulama=GOOGLE_DOGRULAMA,
    )
    with open(os.path.join(KOK, "blog.html"), "w", encoding="utf-8") as f:
        f.write(liste_html)
    print("yazildi: blog.html")


if __name__ == "__main__":
    uret()
