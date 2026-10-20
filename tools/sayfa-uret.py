#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alt sayfa üreticisi.

Yeni bir ilçe ya da hizmet sayfası eklemek istediğinde aşağıdaki SAYFALAR
listesine bir kayıt ekleyip bu dosyayı çalıştırman yeterli:

    python3 tools/sayfa-uret.py

Üretilen .html dosyaları proje köküne yazılır. Elle de düzenleyebilirsin,
ama o zaman betiği tekrar çalıştırırsan değişikliklerin silinir.
"""

import os
import sys
import json

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ayarlar import *  # SITE, FIRMA, TEL_GOSTERIM, TEL_LINK, WA, IG, IG_KULLANICI,
                        # EPOSTA, ADRES_HTML, ADRES_DUZ, ENLEM, BOYLAM, HARITA_Q,
                        # YOL_TARIFI, GOOGLE_DOGRULAMA

ISKELET = """<!DOCTYPE html>
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
<meta name="geo.position" content="39.09626;33.07488">
<meta name="ICBM" content="39.09626, 33.07488">
<meta property="og:type" content="website">
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
      <a href="blog.html"{blog_aktif}>Blog</a>
      <a href="iletisim.html"{iletisim_aktif}>İletişim</a>
    </nav>
    <a class="btn btn--primary" href="tel:{tel_link}">{tel_gosterim}</a>
    <button class="burger" aria-label="Menüyü aç" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<section class="section section--dark section--tight">
  <div class="wrap">
    <h1>{h1}</h1>
    <p class="lead">{spot}</p>
    <div class="hero__cta">
      <a class="btn btn--primary" href="tel:{tel_link}">Hemen ara</a>
      <a class="btn btn--wa" href="https://wa.me/{wa}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>

{govde}

<section class="section section--tight">
  <div class="wrap">
    <div class="contact-grid">
      <div class="map">
        <iframe src="https://maps.google.com/maps?q={harita_q}&z=14&output=embed"
          title="{firma} konumu" loading="lazy"
          referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </div>
      <div class="ticket">
        <h3>İletişim</h3>
        <dl>
          <div class="ticket__row"><dt>Telefon</dt><dd><a href="tel:{tel_link}">{tel_gosterim}</a></dd></div>
          <div class="ticket__row"><dt>WhatsApp</dt><dd><a href="https://wa.me/{wa}" target="_blank" rel="noopener">{tel_gosterim}</a></dd></div>
          <div class="ticket__row"><dt>Adres</dt><dd>{adres_html}</dd></div>
          <div class="ticket__row"><dt>Çalışma saatleri</dt><dd>Pzt–Cmt 08:00–19:00<br>Pazar kapalı</dd></div>
          <div class="ticket__row"><dt>Instagram</dt><dd><a href="{ig}" target="_blank" rel="noopener">@{ig_kullanici}</a></dd></div>
        </dl>
        <a class="btn btn--primary" href="tel:{tel_link}">Ara</a>
        <a class="btn btn--wa" href="https://wa.me/{wa}" target="_blank" rel="noopener">WhatsApp</a>
        <a class="btn btn--ghost" href="{yol}" target="_blank" rel="noopener">Yol tarifi al</a>
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
          <li><a href="hurda-demir.html">Hurda demir alımı</a></li>
          <li><a href="hurda-bakir-aluminyum.html">Bakır ve alüminyum</a></li>
          <li><a href="hurdaci-kulu.html">Kulu hurdacı</a></li>
          <li><a href="hurdaci-cihanbeyli.html">Cihanbeyli hurdacı</a></li>
          <li><a href="hurdaci-sereflikochisar.html">Şereflikoçhisar hurdacı</a></li>
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


def yerel_jsonld(sayfa_adi, aciklama, bolge=None):
    veri = {
        "@context": "https://schema.org",
        "@type": "RecyclingCenter",
        "name": FIRMA,
        "url": SITE + "/",
        "telephone": TEL_LINK,
        "email": EPOSTA,
        "description": aciklama,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "138606. Sk. No: 10",
            "addressLocality": "Kulu",
            "addressRegion": "Konya",
            "postalCode": "42770",
            "addressCountry": "TR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": ENLEM, "longitude": BOYLAM},
        "hasMap": "https://www.google.com/maps/search/?api=1&query=39.09626,33.07488",
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "08:00", "closes": "19:00",
        }],
        "alternateName": "Kulu Hurdacı",
        "areaServed": {"@type": "AdministrativeArea", "name": bolge or "Kulu"},
        "sameAs": [IG],
    }
    return json.dumps(veri, ensure_ascii=False, indent=2)


def madde_listesi(basliklar):
    parcalar = []
    for b, m in basliklar:
        parcalar.append(
            '      <article class="step">\n'
            '        <h3>{}</h3>\n        <p>{}</p>\n      </article>'.format(b, m)
        )
    return "\n".join(parcalar)


def sss_blogu(sorular):
    satirlar = []
    for i, (s, c) in enumerate(sorular):
        acik = " open" if i == 0 else ""
        satirlar.append(
            '      <details{}>\n        <summary>{}</summary>\n'
            '        <p>{}</p>\n      </details>'.format(acik, s, c)
        )
    return ('<section class="section"><div class="wrap">'
            '<div class="head"><h2>Sık sorulanlar</h2></div>'
            '<div class="faq">\n' + "\n".join(satirlar) + '\n</div></div></section>')


def metin_blogu(baslik, paragraflar):
    p = "\n".join("      <p>{}</p>".format(x) for x in paragraflar)
    return ('<section class="section">\n  <div class="wrap">\n'
            '    <div class="head"><h2>{}</h2></div>\n{}\n'
            '  </div>\n</section>'.format(baslik, p))


def kart_blogu(baslik, kartlar):
    return ('<section class="section section--dark">\n  <div class="wrap">\n'
            '    <div class="head"><h2>{}</h2></div>\n'
            '    <div class="steps">\n{}\n    </div>\n'
            '  </div>\n</section>'.format(baslik, madde_listesi(kartlar)))


# --------------------------------------------------------------------------
# SAYFA İÇERİKLERİ — yeni sayfa eklemek için buraya kayıt ekle
# --------------------------------------------------------------------------

SAYFALAR = []

SAYFALAR.append(dict(
    dosya="hurda-demir.html",
    baslik="Kulu Hurda Demir Alımı | Konya Kulu Tonajlı Hurda — " + FIRMA,
    aciklama="Konya Kulu'da hurda demir, sac, çelik konstrüksiyon, ahır demiri ve inşaat "
             "demiri alımı. Tonajlı alım, ücretsiz söküm ve nakliye, kantarlı tartım, anında ödeme.",
    h1="Kulu'da hurda demir alımı",
    spot="İnşaat demiri, sac, profil, çelik konstrüksiyon, ahır ve ağıl demirleri, makine "
         "gövdesi ve beyaz eşya. Tonajlı işlerde kendi ekibimiz ve aracımızla geliyoruz.",
    bolge="Kulu",
    govde=(
        metin_blogu("Kulu'da hangi demir hurdasını alıyoruz", [
            "İnşaat ve tadilat artığı nervürlü demir, kalıp demiri, kiriş ve köşebent; "
            "ahır, ağıl ve sera konstrüksiyonları; bahçe çiti, kapı ve pencere doğramaları; "
            "kazan, kalorifer peteği, boru ve sac artıkları.",
            "Tarım tarafında ömrünü doldurmuş römork, pulluk, mibzer, çizel ve biçerdöver "
            "parçalarını da alıyoruz. Tarlada ya da harmanda duran makineyi yerinde söküp "
            "yüklüyoruz; aracın girebileceği her yere geliyoruz.",
            "Beyaz eşya, klima dış ünitesi ve elektrik motorlarını da değerlendiriyoruz. "
            "Bu ürünlerde bakır ve alüminyum parçalar ayrıştırıldığı için kilogram fiyatı "
            "düz demirin üzerine çıkıyor.",
            "Kulu sanayi sitesindeki atölyeler, depo tasfiyeleri ve şantiye sonu toplamalarda "
            "sözleşmeli ve faturalı çalışıyoruz. Periyodik alım isteyen işletmeler için sabit "
            "gün planı yapıyoruz.",
        ])
        + "\n" +
        kart_blogu("Demir hurdasında fiyatı ne belirler", [
            ("Temizlik", "Demirin üzerinde beton, ahşap, plastik ya da yalıtım malzemesi "
                         "kaldıysa kilogram fiyatı düşer. Ayrıştırılmış yük daha yüksek ödenir."),
            ("Kalınlık ve cins", "Kalın sac ve konstrüksiyon parçaları, ince talaş ve "
                                 "çapaklı malzemeye göre daha iyi fiyat alır."),
            ("Günün borsası", "Demir fiyatı haftalık, bazen günlük değişir. "
                              "Aradığınız gün geçerli rakamı telefonda net olarak söylüyoruz."),
        ])
        + "\n" +
        sss_blogu([
            ("Kaç kilogramdan itibaren adrese geliyorsunuz?",
             "Demir hurdasında yaklaşık 100 kilogram ve üzeri yükler için Kulu ve çevresinde "
             "ekip gönderiyoruz. Daha az miktarı tesisimize getirdiğinizde de anında tartıp ödüyoruz."),
            ("Köyden hurda alıyor musunuz?",
             "Evet. Kulu'ya bağlı tüm köy ve beldelere gidiyoruz. Tarla, harman ve ahır "
             "işlerinde söküm ekipmanımızı yanımızda getiriyoruz."),
            ("Söküm ve nakliye için ücret alıyor musunuz?",
             "Hayır. Söküm, kesim, yükleme ve nakliye bize ait; bu kalemler kilogram "
             "fiyatından düşülmez."),
            ("Fatura kesiyor musunuz?",
             "Kurumsal alımlarda fatura düzenliyoruz. Şirket alımlarında evrak sürecini "
             "tamamen biz yürütüyoruz."),
        ])
    ),
))

SAYFALAR.append(dict(
    dosya="hurda-bakir-aluminyum.html",
    baslik="Kulu Hurda Bakır ve Alüminyum Alımı | Güncel Kilo Fiyatı — " + FIRMA,
    aciklama="Konya Kulu'da hurda bakır, kablo, alüminyum sulama borusu, profil, radyatör "
             "ve pirinç alımı. Ayrıştırmalı tartım, güncel borsa fiyatı, anında nakit ödeme.",
    h1="Kulu'da bakır, alüminyum ve pirinç alımı",
    spot="Kablo bakırı, dalgıç pompa sargısı, kalorifer ve klima boruları, alüminyum sulama "
         "borusu, doğrama, jant, radyatör ve pirinç armatür. Ayrıştırmayı birlikte yapıyoruz.",
    bolge="Kulu",
    govde=(
        metin_blogu("Renkli metalde doğru fiyat ayrıştırmadan geçer", [
            "Bakır, alüminyum ve pirinç hurdanın kilogram değeri demirin çok üzerinde. "
            "Bu yüzden karışık gelen yüklerde tartımdan önce ayrıştırma yapıyor, her metali "
            "kendi fiyatından ödüyoruz. İşlem sizin gözünüzün önünde yapılır.",
            "Kulu'da en sık gelen kalem alüminyum sulama borusu ve rakorları. Boruların "
            "içinde kalan toprak ve çamur tartımda aleyhinize çalıştığı için, yükleme "
            "öncesi birlikte temizliyoruz. Dalgıç pompa motorlarında bakır sargı ayrı tartılır.",
            "Kablolarda bakır oranı kesitine ve yalıtım kalınlığına göre değişir. İsterseniz "
            "soyulmuş bakır fiyatından, isterseniz kablo hâliyle kilogram üzerinden hesaplarız; "
            "hangisi sizin lehinize çıkıyorsa onu söylüyoruz.",
        ])
        + "\n" +
        kart_blogu("Alıma açık başlıca kalemler", [
            ("Bakır", "Kırmızı bakır levha ve boru, kablo bakırı, elektrik ve dalgıç pompa "
                      "motoru sargısı, kalorifer ve klima tesisatı, trafo sargısı."),
            ("Alüminyum", "Sulama borusu ve rakoru, pencere ve kapı profili, jant, radyatör, "
                          "pres döküm parça, alüminyum kablo, sac ve levha."),
            ("Pirinç ve bronz", "Musluk ve armatür, vana, rakor, tesisat parçaları, çeşme, "
                                "yatak burcu, dekoratif ürünler."),
        ])
        + "\n" +
        sss_blogu([
            ("Kabloyu soymam gerekiyor mu?",
             "Gerekmiyor. İki yöntemle de hesaplayıp size daha yüksek tutarı veren seçeneği "
             "uyguluyoruz."),
            ("Az miktarda bakır için geliyor musunuz?",
             "Renkli metalde kilogram değeri yüksek olduğu için 20 kilogramdan itibaren "
             "Kulu ve köylerinde adrese geliyoruz."),
            ("Sulama borularını tarladan siz mi topluyorsunuz?",
             "Evet. Tarladan toplama, taşıma ve yükleme bize ait. Sezon sonunda toplu "
             "kaldırılacak hatlar için önceden randevu almanız yeterli."),
            ("Fiyatları nereden takip edebilirim?",
             "Güncel kilogram fiyatlarını Instagram hesabımızda düzenli paylaşıyoruz. "
             "Telefonda da o gün geçerli rakamı net olarak söylüyoruz."),
        ])
    ),
))


BOLGELER = [
    ("kulu", "Kulu",
     "Kulu merkez mahalleleri ile Zincirlikuyu, Tavşançalı, Kozanlı, Celep, Köşker, "
     "Acıkuyu, Tuzyaka, Karacadere, Altılar ve Seyitahmetli başta olmak üzere ilçeye "
     "bağlı köy ve beldeler",
     "Tesisimiz Kulu'da olduğu için ilçe içinde en hızlı biz varız. Sabah aradığınızda "
     "çoğunlukla aynı gün, en geç ertesi gün adresinizdeyiz. Merkez mahallelerde tadilat "
     "ve ev boşaltma, köylerde ise tarım makinesi, sulama tesisatı ve ahır demirleri en "
     "sık aldığımız kalemler.",
     "Kulu'da yurt dışında yaşayan aileler için kapalı ev boşaltma ve tasfiye işlerini "
     "sık yapıyoruz. Anahtarı olan bir yakınınız yeterli; çalışma sırasında fotoğraf ve "
     "video göndererek süreci uzaktan takip etmenizi sağlıyoruz."),

    ("cihanbeyli", "Cihanbeyli",
     "Cihanbeyli merkez ve bağlı köyler",
     "Kulu'daki tesisimizden Cihanbeyli'ye düzenli araç çıkıyor. Tonajlı işlerde aynı "
     "hafta içinde, küçük yüklerde ise bölgeye çıktığımız gün randevu veriyoruz.",
     "Tuz Gölü çevresindeki tarım işletmelerinden çıkan sulama boruları, römork ve "
     "makine hurdaları ile köy tasfiyelerinde çalışıyoruz."),

    ("sereflikochisar", "Şereflikoçhisar",
     "Şereflikoçhisar merkez ve çevre köyler",
     "Şereflikoçhisar, Kulu'ya en yakın komşu ilçe. Karayolu üzerinden kısa mesafede "
     "olduğumuz için buraya da aynı gün çıkabiliyoruz.",
     "İlçe merkezindeki atölyeler ve tarım işletmeleriyle düzenli çalışıyor, tonajlı "
     "işlerde kendi kamyonumuzla geliyoruz."),
]

# Ana sayfa zaten "Kulu hurdacı" kelimesini hedeflediği için Kulu sayfasına
# başlık çakışmasın diye ayrı bir başlık veriyoruz.
OZEL_BASLIK = {
    "kulu": "Kulu Köyleri ve Merkez Mahalleleri | Adrese Gelen Hurda Alımı — " + FIRMA,
}

for anahtar, ad, mahalleler, ozel1, ozel2 in BOLGELER:
    SAYFALAR.append(dict(
        dosya="hurdaci-{}.html".format(anahtar),
        baslik=OZEL_BASLIK.get(
            anahtar, "{} Hurdacı | Yerinde Hurda Alımı ve Söküm — {}".format(ad, FIRMA)),
        aciklama="{} bölgesinde hurda demir, bakır, alüminyum, tarım makinesi ve hurda araç "
                 "alımı. Aynı gün adrese geliyor, söküm ve nakliyeyi biz yapıyoruz. "
                 "Arayın: {}".format(ad, TEL_GOSTERIM),
        h1="{} hurdacı: adrese gelen hurda alımı".format(ad),
        spot="{} ve çevresinde ev, ahır, tarla, atölye ve şantiye hurdası alıyoruz. "
             "Telefonla arayın, aynı gün ekip gönderelim.".format(ad),
        bolge=ad,
        govde=(
            metin_blogu("{} bölgesinde nasıl çalışıyoruz".format(ad), [
                ozel1,
                ozel2,
                "Hizmet verdiğimiz yerler: {}. Listede görmediğiniz bir yer varsa yine de "
                "arayın; bölge sınırları içinde her adrese gidiyoruz.".format(mahalleler),
                "Söküm, kesim, yükleme ve nakliye ücretsiz. Tartım kantarda, sizin yanınızda "
                "yapılıyor ve ödeme aynı anda nakit ya da havale olarak tamamlanıyor.",
            ])
            + "\n" +
            kart_blogu("{} için sık gelen işler".format(ad), [
                ("Tarla, ahır ve sulama",
                 "Hurdaya çıkan traktör ve römork, pulluk ve mibzer, sulama boruları, "
                 "dalgıç pompa, ahır ve ağıl demirleri, sera konstrüksiyonu."),
                ("Ev ve tadilat",
                 "Eski kalorifer peteği ve boruları, kombi, pencere doğraması, mutfak "
                 "dolabı metalleri, beyaz eşya ve klima üniteleri, ev boşaltma."),
                ("Atölye ve şantiye",
                 "Tezgâh ve makine sökümü, üretim fireleri, raf sistemleri, kablo "
                 "artıkları, kalıp ve inşaat demiri, iş bitimi saha temizliği."),
            ])
            + "\n" +
            sss_blogu([
                ("{} içinde ne kadar sürede geliyorsunuz?".format(ad),
                 "Sabah aradığınızda çoğunlukla aynı gün içinde ekip gönderiyoruz. "
                 "Yoğun günlerde en geç ertesi güne randevu veriyoruz."),
                ("Köye ve tarlaya geliyor musunuz?",
                 "Evet. Araç girebilen her yere gidiyoruz. Tarlada duran makineyi yerinde "
                 "söküp yüklüyor, çalışma sonrası alanı temiz bırakıyoruz."),
                ("Hafta sonu çalışıyor musunuz?",
                 "Cumartesi günleri 08:00-19:00 arası açığız. Pazar günleri için önceden "
                 "randevu alınması gerekiyor."),
            ])
        ),
    ))


ILETISIM_GOVDE = """<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>Fiyat almak için</h2>
      <p class="lead">En hızlı yol telefon ya da WhatsApp. Yazılı iletişimi tercih ederseniz
      aşağıdaki formu doldurun, aynı iş günü içinde dönüş yapıyoruz.</p>
    </div>

    <form name="teklif" method="POST" data-netlify="true" netlify-honeypot="bot-alani" class="form">
      <input type="hidden" name="form-name" value="teklif">
      <p hidden><label>Bu alanı boş bırakın: <input name="bot-alani"></label></p>

      <div class="form__row">
        <label for="ad">Adınız</label>
        <input id="ad" name="ad" type="text" required autocomplete="name">
      </div>
      <div class="form__row">
        <label for="tel">Telefon</label>
        <input id="tel" name="telefon" type="tel" required autocomplete="tel" placeholder="05xx xxx xx xx">
      </div>
      <div class="form__row">
        <label for="ilce">İlçe</label>
        <select id="ilce" name="ilce">
          <option>Kulu merkez</option>
          <option>Kulu köyleri</option>
          <option>Cihanbeyli</option>
          <option>Şereflikoçhisar</option>
          <option>Diğer</option>
        </select>
      </div>
      <div class="form__row">
        <label for="mesaj">Elinizdeki hurdayı kısaca anlatın</label>
        <textarea id="mesaj" name="mesaj" rows="5" required
          placeholder="Örnek: Tarladan kaldırılacak alüminyum sulama boruları, yaklaşık 400 kg."></textarea>
      </div>
      <button class="btn btn--primary" type="submit">Teklif iste</button>
    </form>
  </div>
</section>"""


SAYFALAR.append(dict(
    dosya="iletisim.html",
    baslik="İletişim | Kulu Hurdacı, Konya — " + FIRMA,
    aciklama="Kulu hurdacı iletişim: telefon, WhatsApp, adres, konum ve çalışma saatleri. "
             "Kulu ve çevresinde hurdanız için aynı gün fiyat alın.",
    h1="Bize ulaşın",
    spot="Telefonla arayın, WhatsApp'tan fotoğraf gönderin ya da Kulu'daki tesisimize uğrayın. "
         "Hafta içi ve cumartesi 08:00–19:00 arası açığız.",
    bolge="Kulu",
    govde=ILETISIM_GOVDE,
    iletisim_aktif=True,
))


def uret():
    for s in SAYFALAR:
        html = ISKELET.format(
            baslik=s["baslik"],
            aciklama=s["aciklama"],
            dosya=s["dosya"],
            h1=s["h1"],
            spot=s["spot"],
            govde=s["govde"],
            jsonld=yerel_jsonld(s["dosya"], s["aciklama"], s.get("bolge")),
            site=SITE,
            firma=FIRMA,
            tel_link=TEL_LINK,
            tel_gosterim=TEL_GOSTERIM,
            wa=WA,
            ig=IG,
            ig_kullanici=IG_KULLANICI,
            eposta=EPOSTA,
            adres_html=ADRES_HTML,
            adres_duz=ADRES_DUZ,
            harita_q=HARITA_Q,
            yol=YOL_TARIFI,
            iletisim_aktif=' aria-current="page"' if s.get("iletisim_aktif") else "",
            blog_aktif="",
            google_dogrulama=GOOGLE_DOGRULAMA,
        )
        yol = os.path.join(KOK, s["dosya"])
        with open(yol, "w", encoding="utf-8") as f:
            f.write(html)
        print("yazildi:", s["dosya"])


if __name__ == "__main__":
    uret()
