# Ekran Otomasyonu ile Otomatik Kristal Toplama - Kullanım Kılavuzu

## 🎮 Genel Bakış

Bu güncelleme ile bot artık **ekran otomasyonu** kullanarak gerçek oyunda kristal toplayabilir. API token'a gerek yok - sadece oyunu açın ve bot sanki insan oynuyormuş gibi kristalleri toplayacak!

## ✨ Özellikler

- 🖱️ **İnsan Benzeri Fare Hareketi**: Bot eğri yollar takip eder ve değişken hızda hareket eder
- 🎯 **Akıllı Kristal Tespiti**: Renk analizi ile 5 seviye kristal tespit eder (beyaz, yeşil, mavi, mor, altın)
- 🗺️ **Otomatik Navigasyon**: Haritada gezinir ve kristallere gider
- 🔒 **Güvenlik**: Rastgele gecikmeler ve hız sınırlama ile anti-detection
- ⚙️ **Kolay Kurulum**: Oyunu açın, ayarları yapın, başlatın!

## 🚀 Hızlı Başlangıç

### Adım 1: Oyunu Açın

```
1. League of Kingdoms oyununu başlatın (tarayıcı veya uygulama)
2. Pencere başlığında "League of Kingdoms" yazdığından emin olun
3. Haritayı açık tutun
```

### Adım 2: Bot Ayarlarını Yapın

`config/settings.py` dosyasını bir metin editörü ile açın ve şu ayarları yapın:

```python
# Simülasyon modunu kapat
GameIntegrationSettings.SIMULATION_MODE = False

# Ekran otomasyonunu aktif et
GameIntegrationSettings.AUTOMATION_METHOD = "screen"
GameIntegrationSettings.USE_SCREEN_CAPTURE = True
GameIntegrationSettings.IMAGE_RECOGNITION = True
GameIntegrationSettings.USE_MOUSE_CONTROL = True

# Hangi seviyelerdeki kristalleri toplayacaksınız?
FilterSettings.TARGET_LEVELS = [4, 5]  # Sadece yüksek seviye (değiştirebilirsiniz)
```

### Adım 3: Bot'u Başlatın

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
python src/main.py
```

### Adım 4: Bot Çalışıyor!

Bot otomatik olarak:
1. ✅ Oyun penceresini bulur
2. ✅ Ekranda kristalleri tespit eder
3. ✅ Haritada insan gibi gezinir
4. ✅ Kristalleri toplar

## ⚙️ Gelişmiş Ayarlar

### Fare Hareket Hızı

Fare çok yavaş veya hızlı hareket ediyorsa:

```python
# config/settings.py
GameIntegrationSettings.MOVEMENT_SPEED = 0.5  # 0.1 (çok yavaş) - 2.0 (çok hızlı)
```

### Kristal Tespit Hassasiyeti

Kristaller tespit edilmiyorsa:

```python
# config/settings.py
GameIntegrationSettings.CRYSTAL_MIN_AREA = 30  # Küçük kristaller için azaltın
GameIntegrationSettings.CRYSTAL_MAX_AREA = 8000  # Büyük kristaller için artırın
GameIntegrationSettings.DETECTION_CONFIDENCE = 0.5  # 0-1 arası (düşük = daha hassas)
```

### Güvenlik Ayarları

Bot şüpheli görünmesin diye:

```python
# config/settings.py
SecuritySettings.RANDOM_DELAYS = True  # Mutlaka açık tutun!
SecuritySettings.MIN_RANDOM_DELAY = 0.5  # Minimum gecikme (saniye)
SecuritySettings.MAX_RANDOM_DELAY = 2.0  # Maksimum gecikme (saniye)

# Hız sınırlaması
SecuritySettings.MAX_REQUESTS_PER_MINUTE = 30  # Dakikada max işlem
```

### Toplama Hızı

```python
# config/settings.py
CollectorSettings.MAX_COLLECT_PER_CYCLE = 10  # Döngü başına max toplama
ScanSettings.SCAN_INTERVAL = 2.0  # Taramalar arası bekleme (saniye)
```

## 🐛 Sorun Giderme

### Oyun Penceresi Bulunamıyor

**Çözüm 1:** Pencere başlığını kontrol edin
```python
# config/settings.py
GameIntegrationSettings.GAME_WINDOW_TITLE = "LeagueOfKingdoms"  # veya başka
```

**Çözüm 2:** Oyunu tam ekran yerine pencere modunda açın

**Çözüm 3:** Bot'u yönetici olarak çalıştırın

### Kristaller Tespit Edilmiyor

1. **Ayarları kontrol edin:**
   - `SIMULATION_MODE = False` olmalı
   - `AUTOMATION_METHOD = "screen"` olmalı

2. **Oyun görünümünü kontrol edin:**
   - Harita net görünüyor mu?
   - Zoom seviyesini değiştirmeyin
   - Haritayı açık tutun

3. **Tespit parametrelerini ayarlayın:**
   ```python
   GameIntegrationSettings.CRYSTAL_MIN_AREA = 30
   GameIntegrationSettings.CRYSTAL_MAX_AREA = 8000
   GameIntegrationSettings.DETECTION_CONFIDENCE = 0.5
   ```

### Fare Hareketi Çok Yavaş

```python
# config/settings.py
GameIntegrationSettings.MOVEMENT_SPEED = 1.0  # Hızlandır
GameIntegrationSettings.CLICK_DELAY = 0.1  # Tıklama gecikmesini azalt
```

### Bağımlılık Hataları

Eğer "ModuleNotFoundError" hatası alırsanız:

```bash
pip install pyautogui pillow opencv-python pytesseract pygetwindow mss
```

## 📊 İstatistikler

Bot çalışırken detaylı istatistikler tutar:

```bash
# Logları görüntüle
type logs\crystal_bot.log  # Windows
tail -f logs/crystal_bot.log  # Linux/Mac
```

## ⚠️ Önemli Uyarılar

1. **Oyun Kuralları**: Bot kullanımı oyun kurallarına aykırı olabilir. Hesap yasaklanma riski vardır.
2. **Sorumluluk**: Bu riski kabul ederek kullanın.
3. **Etik Kullanım**: Diğer oyuncuları etkilemeyin, adil kullanın.
4. **Güvenlik**: Anti-detection ayarlarını asla kapatmayın!

## 🎯 Önerilen Kullanım

### Yeni Başlayanlar İçin

```python
# config/settings.py
GameIntegrationSettings.SIMULATION_MODE = False
GameIntegrationSettings.AUTOMATION_METHOD = "screen"
FilterSettings.TARGET_LEVELS = [5]  # Sadece en yüksek seviye
CollectorSettings.MAX_COLLECT_PER_CYCLE = 5  # Yavaş başlayın
SecuritySettings.MAX_RANDOM_DELAY = 3.0  # Daha fazla gecikme
```

### İleri Seviye Kullanıcılar

```python
# config/settings.py
FilterSettings.TARGET_LEVELS = [3, 4, 5]  # Orta-yüksek seviye
CollectorSettings.MAX_COLLECT_PER_CYCLE = 15
GameIntegrationSettings.MOVEMENT_SPEED = 0.7
```

## 📞 Destek

Sorun yaşarsanız:

1. `logs/crystal_bot.log` dosyasını kontrol edin
2. [GAME_INTEGRATION.md](GAME_INTEGRATION.md) dosyasına bakın
3. GitHub'da issue açın

## 🎉 Başarılar!

Bot'un tadını çıkarın ve kristal toplamaya başlayın! 💎

---

**Not**: Bu bot eğitim amaçlıdır. Kullanım sorumluluğu size aittir.
