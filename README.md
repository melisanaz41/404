# Sezgenler Kulu Hurda — site dosyaları

Saf HTML + CSS + JavaScript. Derleme aracı, npm kurulumu, sunucu yazılımı gerekmez.
VS Code'da açıp kaydettiğin an çalışır.

## Dosya yapısı

```
konya-hurda/
├── index.html                    Ana sayfa (hero video, galeri, konum, SSS)
├── hurda-demir.html              Hizmet sayfası
├── hurda-bakir-aluminyum.html    Hizmet sayfası
├── hurdaci-kulu.html             Kulu köy ve mahalle sayfası
├── hurdaci-cihanbeyli.html       Komşu ilçe sayfası
├── hurdaci-sereflikochisar.html  Komşu ilçe sayfası
├── iletisim.html                 İletişim + teklif formu
├── 404.html                      Hatalı adres sayfası
├── css/style.css                 Tüm tasarım burada
├── js/main.js                    Menü, galeri büyütme, yer tutucular
├── img/                          Fotoğraflar buraya
├── video/                        Videolar buraya
├── robots.txt                    Arama motoru yönergesi
├── sitemap.xml                   Site haritası
├── netlify.toml                  Yayın ayarları
└── tools/sayfa-uret.py           Yeni ilçe/hizmet sayfası üretici (isteğe bağlı)
```

---

## 1. Adım — VS Code'da açma

1. VS Code'u kur: https://code.visualstudio.com
2. Eklentiler (sol menüde kare ikon) → şunları yükle:
   - **Live Server** (Ritwick Dey) — kaydettiğin an tarayıcıda görürsün
   - **Prettier** — kodu düzgün hizalar
3. `File → Open Folder` ile `konya-hurda` klasörünü aç
4. `index.html` dosyasına sağ tıkla → **Open with Live Server**

Tarayıcı açılır. Artık bir şey değiştirip kaydettiğinde (Ctrl+S) sayfa kendi kendine yenilenir.

---

## 2. Adım — Kendi bilgilerini yaz

VS Code'da **Ctrl+Shift+H** (Değiştir) ile tüm dosyalarda topluca değiştir.
Sırayla şunları ara ve değiştir:

| Ara | Şu an ne yazıyor | Değiştirmen gerekiyor mu |
|---|---|---|
| Firma adı | `Sezgenler Kulu Hurda` | Hayır, doğru |
| Telefon (görünen) | `0530 528 08 19` | Hayır, doğru |
| Telefon (link) | `+905305280819` | Hayır, doğru |
| WhatsApp | `905305280819` | WhatsApp farklı bir numaraysa değiştir |
| Adres | `138606. Sk. No: 10, 42770 Kulu / Konya` | Hayır, doğru |
| Koordinat | `39.09626`, `33.07488` | Hayır, doğru |
| Alan adı | `www.sezgenlerkuluhurda.com` | **.com mu .com.tr mi aldıysan ona göre düzelt** |
| Instagram | `sezgenlerkuluhurda` | **Gerçek kullanıcı adınla değiştir** |
| E-posta | `info@sezgenlerkuluhurda.com` | **Gerçek adresinle değiştir** |

Telefon, adres ve koordinatlar zaten senin bilgilerinle dolduruldu. Sadece son üç
satırı kontrol etmen yeterli.

**Harita ve koordinatlar** verdiğin 39.09626 K / 33.07488 D değerleriyle ayarlandı.
Harita gömülü çerçevede, Schema işaretlemesinde, `geo.position` meta etiketinde ve
"yol tarifi al" butonlarında aynı koordinat kullanılıyor. Konum kayıklığı görürsen
tüm dosyalarda `39.09626,33.07488` arayıp düzeltmen yeterli.

---

## 3. Adım — Fotoğraf ve video

- `img/` klasörüne `galeri-1.jpg` … `galeri-8.jpg` koy
- `video/` klasörüne `tanitim.mp4` koy
- Detaylı boyut önerileri bu klasörlerdeki not dosyalarında

Fotoğraf yoksa site yine düzgün görünür, yerine renkli bloklar gelir.
Fotoğrafları **squoosh.app** üzerinden küçült — 300 KB'ı geçen görsel siteyi yavaşlatır
ve Google sıralamanı düşürür.

---

## 4. Adım — Yayına alma (ücretsiz)

### GitHub'a yükle
1. https://github.com → ücretsiz hesap aç
2. Sağ üst `+` → **New repository** → isim: `sezgenler-kulu-hurda` → **Create**
3. Açılan sayfada **uploading an existing file** bağlantısına tıkla
4. Klasördeki tüm dosyaları sürükle bırak → **Commit changes**

### Netlify'a bağla
1. https://netlify.com → **Sign up with GitHub**
2. **Add new site → Import an existing project → GitHub**
3. `sezgenler-kulu-hurda` deposunu seç → **Deploy**
4. 1-2 dakikada site yayında: `rastgele-isim.netlify.app`

Bundan sonra GitHub'a yüklediğin her değişiklik otomatik yayına geçer.

### Alan adını bağla
1. Alan adını al (Cloudflare Registrar, Namecheap, Natro veya İsimtescil)
2. Netlify → **Domain settings → Add a domain** → alan adını yaz
3. Netlify sana DNS kayıtlarını gösterir; alan adını aldığın sitenin panelinde bu kayıtları gir
4. SSL sertifikası (https) birkaç saat içinde otomatik gelir — ekstra işlem yok

### Form
`iletisim.html` içindeki teklif formu Netlify'da **hiçbir ek kurulum olmadan** çalışır.
Gelen mesajları Netlify panelinde `Forms` sekmesinde görürsün. Bildirim maili için:
`Forms → Settings → Form notifications → Add notification → Email`.

> Netlify dışında bir yerde yayınlarsan form çalışmaz. O durumda formu silip sadece
> telefon/WhatsApp bırakmak en pratiği.

---

## 5. Adım — Google'a tanıtma

Site yayına girdikten sonra sırasıyla:

1. **Google Search Console** (search.google.com/search-console)
   - Alan adını ekle, doğrula
   - `Sitemaps` bölümüne `sitemap.xml` yaz ve gönder
   - `URL Denetimi` ile ana sayfayı dizine ekletme talebi gönder

2. **Google İşletme Profili** (google.com/business) — *yerel sıralamanın en kritik parçası*
   - Kategori: Hurda metal alım satımı / Geri dönüşüm merkezi
   - Konum: Kulu, Konya — haritada tam noktaya pin koy (39.09626, 33.07488)
   - Hizmet alanı: Kulu merkez + bağlı köyler, Cihanbeyli, Şereflikoçhisar
   - Adres doğrulamasını mutlaka tamamla
   - En az 15-20 gerçek fotoğraf yükle
   - Web sitesi alanına alan adını gir
   - Müşterilerden düzenli yorum iste

3. **Bing Webmaster Tools** — Search Console'dan tek tıkla içe aktarılır

4. **Yandex Webmaster** — Türkiye'de azımsanmayacak trafik getirir

---

## Blog

Site artık bir blog altyapısıyla geldi: `blog.html` (liste sayfası) ve
`blog-<konu>.html` şeklindeki 8 hazır yazı. Hepsi Kulu'ya özel, gerçek
sorulara cevap veren, anahtar kelime doldurmayan içerikler — "kulu hurda
demir fiyatı", "kulu hurda traktör satışı" gibi aramalarda avantaj sağlamak
için yazıldı.

### Yeni yazı ekleme

`tools/blog-uret.py` dosyasındaki `YAZILAR` listesine yeni bir `dict` kaydı
ekle (mevcut kayıtları örnek al — `slug`, `tag`, `baslik`, `aciklama`, `h1`,
`spot`, `tarih`, `govde`, `ilgili` alanlarını doldurman yeterli), sonra:

```bash
python3 tools/blog-uret.py
```

Bu hem yeni yazının sayfasını hem de güncellenmiş `blog.html` listesini
üretir. Yeni yazı eklediğinde `sitemap.xml`'e bir `<url>` satırı eklemeyi
unutma.

> Dikkat: Bu betik tüm blog-*.html dosyalarını ve blog.html'i **sıfırdan
> yeniden yazar**. Bir yazıda elle değişiklik yaptıysan betiği çalıştırma,
> ya da değişikliği `YAZILAR` listesindeki ilgili kayda taşı.

### Ortak bilgiler artık tek yerde

Telefon, adres, Instagram gibi bilgiler artık `tools/ayarlar.py` dosyasında
tek bir yerde tutuluyor. Bir bilgi değiştiğinde sadece bu dosyayı
güncelleyip sırasıyla iki betiği çalıştırman yeterli:

```bash
python3 tools/sayfa-uret.py
python3 tools/blog-uret.py
```

Böylece geçen sefer yaşanan gibi bazı sayfalarda eski, bazılarında yeni
bilgi kalma riski ortadan kalkıyor.

### Blog için ekstra SEO ipuçları

- Yeni bir yazı yayınladığında Search Console'da o sayfanın "URL denetimi"
  ile dizine ekletme talebi gönder — indekslenmeyi hızlandırır.
- Instagram'da her yeni yazıyı paylaşıp bio'daki linki güncellemek, hem
  trafik getirir hem Google'a "aktif site" sinyali verir.
- Ayda 1-2 yeni yazı, onlarca yazıyı bir günde yayınlamaktan daha iyi sonuç
  verir — düzenli yayın, ani yığılmadan daha güvenilir bir sinyal.

## 6. Adım — Yeni bölge sayfası ekleme

Kulu'ya bağlı bir köy ya da yakın bir ilçe için ayrı sayfa açmak, o kelimede
sıralanmanın en hızlı yolu. Örnek: `hurdaci-kozanlı.html`, `hurdaci-yunak.html`.

`tools/sayfa-uret.py` dosyasındaki `BOLGELER` listesine yeni bir satır ekle:

```python
("yunak", "Yunak",
 "Yunak merkez ve bağlı köyler",
 "Buraya o bölgede nasıl çalıştığını anlatan bir paragraf.",
 "Buraya o bölgeye özgü ikinci bir paragraf."),
```

Sonra terminalde çalıştır:

```bash
python3 tools/sayfa-uret.py
```

> Dikkat: Bu betik hizmet ve bölge sayfalarını **sıfırdan yeniden yazar**.
> O dosyalarda elle değişiklik yaptıysan betiği çalıştırma, ya da değişikliği
> betiğin içine taşı. `index.html` betikten etkilenmez, onu elle düzenle.

Yeni sayfa eklediğinde `sitemap.xml` dosyasına bir `<url>` satırı, `index.html`
içindeki "Hizmet verdiğimiz bölgeler" bloğuna da bir bağlantı eklemeyi unutma.

---

## Kulu için SEO notları

- Ana sayfa **"Kulu hurdacı"** ve **"Konya Kulu hurda"** kelimelerini hedefliyor.
  `hurdaci-kulu.html` ise köy ve mahalle aramalarını topluyor; ikisinin başlıkları
  bilerek farklı tutuldu, aynı kelimede birbirleriyle yarışmasınlar diye.
- Kulu'da rekabet Konya merkeze göre çok daha düşük. Doğru kurulumla 1-3 ay
  içinde ilk sayfada olman gerçekçi bir beklenti.
- Google İşletme Profili bu ölçekte siteden bile önemli. Kulu'da haritada
  görünen az sayıda hurdacı olduğu için profil doğrulaması tamamlandığı anda
  ciddi fark yaratır.
- İçerik fikri: "Kulu'da sulama borusu hurda fiyatı", "Kulu'da hurda traktör
  alımı", "Kulu'da ev boşaltma" gibi başlıklarla ayrı sayfalar açmak. Bunlar
  ilçede gerçekten aranan ama karşılığında neredeyse hiç sayfa olmayan konular.
- Yurt dışında yaşayan Kulu'lular önemli bir kitle. İletişim sayfasında
  WhatsApp'ın öne çıkması bu yüzden değerli — uluslararası arama ücreti ödemeden
  ulaşabiliyorlar.

## Yayına almadan önce kontrol listesi

- [ ] Instagram kullanıcı adı ve e-posta gerçek bilgilerle değişti mi
- [ ] Harita doğru konumu gösteriyor mu
- [ ] Alan adı aldığın uzantıyla (.com / .com.tr) her yerde eşleşiyor mu
- [ ] Instagram bağlantısı doğru hesaba gidiyor mu
- [ ] `sitemap.xml` ve `robots.txt` içindeki alan adı güncellendi mi
- [ ] Tüm sayfalarda `canonical` etiketi kendi alan adını gösteriyor mu
- [ ] Fotoğraflar 300 KB altında mı
- [ ] Telefondan açıp test ettin mi (trafiğin %80'i mobilden gelecek)
- [ ] PageSpeed Insights (pagespeed.web.dev) puanı 90+ mı
