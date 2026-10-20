# -*- coding: utf-8 -*-
"""
Site genelinde ortak kullanılan sabitler.

Telefon, adres, Instagram gibi bir bilgi değiştiğinde SADECE bu dosyayı
güncellemen yeterli — sayfa-uret.py ve blog-uret.py buradan okuyor.
Böylece bir bilgiyi bazı sayfalarda güncelleyip diğerlerinde unutma riski
ortadan kalkıyor.

Değiştirdikten sonra sırasıyla çalıştır:

    python3 tools/sayfa-uret.py
    python3 tools/blog-uret.py
"""

SITE = "https://www.sezgenlerkuluhurda.com"
FIRMA = "Sezgenler Kulu Hurda"
TEL_GOSTERIM = "0530 528 08 19"
TEL_LINK = "+905305280819"
WA = "905305280819"
IG = "https://www.instagram.com/sezgenlerkuluhurda"
IG_KULLANICI = "sezgenlerkuluhurda"
EPOSTA = "info@sezgenlerkuluhurda.com"
ADRES_HTML = "138606. Sk. No: 10<br>42770 Kulu / Konya"
ADRES_DUZ = "138606. Sk. No: 10, 42770 Kulu / Konya"
ENLEM = 39.09626
BOYLAM = 33.07488
HARITA_Q = "39.09626,33.07488"
YOL_TARIFI = "https://www.google.com/maps/dir/?api=1&destination=39.09626,33.07488"
GOOGLE_DOGRULAMA = "MX-rv6r9uwV245M_l6a1efDAEaPgMrUqvlg_5CJ7rv8"
