# Gerçek Oyun Entegrasyonu Kılavuzu

Bu kılavuz, League of Kingdoms Crystal Bot'u gerçek oyunla entegre etmek için gerekli adımları açıklar.

## 📋 İçindekiler

- [Genel Bakış](#genel-bakış)
- [Kurulum](#kurulum)
- [Yapılandırma](#yapılandırma)
- [Entegrasyon Yöntemleri](#entegrasyon-yöntemleri)
- [Ekran Otomasyonu ile Kullanım](#ekran-otomasyonu-ile-kullanım)
- [Test](#test)
- [Sorun Giderme](#sorun-giderme)

## 🎯 Genel Bakış

Bu bot, League of Kingdoms oyununda kristalleri otomatik olarak tespit etmek ve toplamak için tasarlanmıştır. Gerçek oyunla entegre edilebilmesi için üç farklı yöntem sunar:

1. **Ekran Otomasyonu (Screen-Based)** - Ekran görüntüsü analizi ve fare kontrolü (API gerektirmez, önerilen)
2. **API Tabanlı Entegrasyon** - Oyunun API'sini kullanarak
3. **Hibrit Yöntem** - Her ikisinin kombinasyonu

## 🚀 Kurulum

### Adım 1: Bot'u Yükleyin

```bash
# Depoyu klonlayın
git clone https://github.com/birolservis-max/LeagueOfkingdomsSampleBot.git
cd LeagueOfkingdomsSampleBot

# Windows için: setup.bat dosyasını çalıştırın
setup.bat

# Linux/Mac için: Manuel kurulum
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir -p logs data
```

### Adım 2: Gerekli Bağımlılıkları Yükleyin

Bot zaten temel işlevsellik için gerekli paketleri içerir. Ancak, farklı entegrasyon yöntemleri için ek paketlere ihtiyacınız olabilir:

#### Ekran Otomasyonu için (Önerilen)
```bash
pip install pyautogui pillow opencv-python pytesseract pygetwindow mss
# Zaten requirements.txt'de mevcut - setup.bat otomatik yükler
```

#### API Entegrasyonu için
```bash
pip install requests
# Zaten requirements.txt'de mevcut
```

## ⚙️ Yapılandırma

### config/settings.py Dosyasını Düzenleyin

Bot'un gerçek oyunla çalışması için `config/settings.py` dosyasındaki `GameIntegrationSettings` sınıfını yapılandırmanız gerekir.

### Temel Yapılandırma

```python
# config/settings.py dosyasını açın ve aşağıdaki ayarları düzenleyin:

class GameIntegrationSettings:
    # Simülasyon modunu kapatın (gerçek oyun için)
    SIMULATION_MODE = False  # ⚠️ ÖNEMLİ: False yapın
    
    # Oyun sunucu bilgileri
    GAME_SERVER_URL = "https://game.leagueofkingdoms.com"  # Gerçek URL'i girin
    API_ENDPOINT = "/api/v1"  # API endpoint'i
    USE_API = True  # API kullanımı
    
    # Kimlik doğrulama bilgileri
    AUTH_TOKEN = "your_auth_token_here"  # Oyun token'ınız
    USER_ID = "your_user_id"  # Kullanıcı ID'niz
    SESSION_ID = ""  # Oturum ID (opsiyonel)
    
    # Entegrasyon yöntemi
    AUTOMATION_METHOD = "api"  # "api", "screen", veya "hybrid"
```

## 🔧 Entegrasyon Yöntemleri

### Yöntem 1: Ekran Otomasyonu (Önerilen - API Gerektirmez) 🆕

**Bu yöntem API gerektirmez ve oyunu manuel olarak açarak kullanabilirsiniz!**

Ekran otomasyonu, oyun ekranını analiz ederek kristalleri tespit eder ve fare kontrolü ile sanki insan oynuyormuş gibi kristalleri toplar.

#### Avantajlar:
- ✅ API token'a gerek yok
- ✅ Oyunu manuel açmanız yeterli
- ✅ İnsan benzeri davranış
- ✅ Kolay kurulum
- ✅ Gerçek oyun deneyimi

#### Yapılandırma:

```python
# config/settings.py
class GameIntegrationSettings:
    # Simülasyon modunu kapat
    SIMULATION_MODE = False
    
    # Ekran otomasyonu modunu aktif et
    AUTOMATION_METHOD = "screen"
    
    # Ekran yakalama ayarları
    USE_SCREEN_CAPTURE = True
    IMAGE_RECOGNITION = True
    
    # Fare kontrolü
    USE_MOUSE_CONTROL = True
    HUMAN_LIKE_MOVEMENT = True  # İnsan benzeri hareket
    MOVEMENT_SPEED = 0.5  # Hareket hızı
    
    # Oyun penceresi
    GAME_WINDOW_TITLE = "League of Kingdoms"
    AUTO_FOCUS_WINDOW = True
    
    # Kristal tespit ayarları
    CRYSTAL_MIN_AREA = 50
    CRYSTAL_MAX_AREA = 5000
    DETECTION_CONFIDENCE = 0.6
```

#### Kullanım Adımları:

1. **Oyunu Açın:**
   ```
   League of Kingdoms oyununu tarayıcıda veya uygulamada açın
   Pencere başlığında "League of Kingdoms" olduğundan emin olun
   ```

2. **Ayarları Yapın:**
   ```python
   # config/settings.py dosyasını düzenleyin
   GameIntegrationSettings.SIMULATION_MODE = False
   GameIntegrationSettings.AUTOMATION_METHOD = "screen"
   ```

3. **Bot'u Başlatın:**
   ```bash
   # Windows
   start.bat
   
   # Linux/Mac
   python src/main.py
   ```

4. **Bot Otomatik Olarak:**
   - Oyun penceresini bulacak
   - Ekranda kristalleri tespit edecek
   - Haritada insan gibi gezinecek
   - Kristallere tıklayarak toplayacak

### Yöntem 2: API Tabanlı Entegrasyon

API tabanlı entegrasyon, oyunun resmi API'sini kullanır. (Token gerektirir)

#### Yapılandırma:

```python
class GameIntegrationSettings:
    SIMULATION_MODE = False
    USE_API = True
    AUTOMATION_METHOD = "api"
    
    # API bilgileri
    GAME_SERVER_URL = "https://game.leagueofkingdoms.com"
    API_ENDPOINT = "/api/v1"
    
    # Kimlik doğrulama
    AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Gerçek token
    USER_ID = "12345"
    
    # Bağlantı ayarları
    CONNECTION_TIMEOUT = 30
    REQUEST_RETRY_COUNT = 3
    VERIFY_SSL = True
```

#### Token Nasıl Alınır?

1. Oyuna tarayıcıda giriş yapın
2. Tarayıcı geliştirici araçlarını açın (F12)
3. Network sekmesine gidin
4. Oyun içi bir aksiyon yapın
5. İstekleri inceleyin ve Authorization header'ında token'ı bulun

### Yöntem 3: Hibrit Entegrasyon

API ve ekran otomasyonu yöntemlerinin kombinasyonunu kullanır.

```python
class GameIntegrationSettings:
    SIMULATION_MODE = False
    AUTOMATION_METHOD = "hybrid"
    
    # Her iki yöntem de etkin
    USE_API = True
    USE_SCREEN_CAPTURE = True
    IMAGE_RECOGNITION = True
```

## 🖱️ Ekran Otomasyonu ile Kullanım

### Adım Adım Kılavuz

#### 1. Oyunu Hazırlayın

```
1. League of Kingdoms oyununu açın (tarayıcı veya uygulama)
2. Pencere başlığında "League of Kingdoms" yazıp yazmadığını kontrol edin
3. Oyun penceresini istediğiniz boyutta ayarlayın
4. Oyun haritasını açık tutun
```

#### 2. Bot Ayarlarını Yapın

`config/settings.py` dosyasını düzenleyin:

```python
# Simülasyon modunu kapat
GameIntegrationSettings.SIMULATION_MODE = False

# Ekran otomasyonu aktif et
GameIntegrationSettings.AUTOMATION_METHOD = "screen"
GameIntegrationSettings.USE_SCREEN_CAPTURE = True
GameIntegrationSettings.IMAGE_RECOGNITION = True
GameIntegrationSettings.USE_MOUSE_CONTROL = True

# İnsan benzeri hareket
GameIntegrationSettings.HUMAN_LIKE_MOVEMENT = True

# Kristal seviyeleri seç (örnek: sadece yüksek seviye)
FilterSettings.TARGET_LEVELS = [4, 5]
```

#### 3. Bot'u Başlatın

```bash
# Windows
start.bat

# Linux/Mac
python src/main.py
```

#### 4. Bot Çalışırken

Bot otomatik olarak şunları yapacak:

```
1. ✓ Oyun penceresini bulma
   - "League of Kingdoms" başlıklı pencereyi arar
   - Pencereyi aktif hale getirir
   - Harita merkezini kalibre eder

2. ✓ Ekran tarama
   - Oyun ekranının görüntüsünü alır
   - Kristalleri renk ve şekil analizi ile tespit eder
   - Kristal seviyelerini belirler (beyaz, yeşil, mavi, mor, altın)

3. ✓ Navigasyon
   - İnsan benzeri fare hareketleri ile haritada gezinir
   - Kristal pozisyonlarına doğru hareket eder
   - Haritayı yumuşak bir şekilde kaydırır

4. ✓ Toplama
   - Kristal üzerine tıklar
   - Toplama animasyonunu bekler
   - Başarıyı kontrol eder

5. ✓ Tekrar
   - Bir sonraki kristale geçer
   - Döngüyü tekrarlar
```

#### 5. Güvenlik ve Anti-Detection

Bot insan benzeri davranış sergiler:

```python
# Rastgele gecikmeler
SecuritySettings.RANDOM_DELAYS = True
SecuritySettings.MIN_RANDOM_DELAY = 0.5  # saniye
SecuritySettings.MAX_RANDOM_DELAY = 2.0  # saniye

# Hız sınırlama
SecuritySettings.RATE_LIMITING = True
SecuritySettings.MAX_REQUESTS_PER_MINUTE = 30

# İnsan benzeri hareket
- Eğri fare yolu (ara nokta ile)
- Değişken hareket hızı
- Rastgele duraklamalar
```

### İpuçları ve Püf Noktaları

**✓ Pencere Tespiti Sorunları:**
```python
# Farklı pencere başlığı varsa:
GameIntegrationSettings.GAME_WINDOW_TITLE = "LeagueOfKingdoms"  # veya başka

# Veya manuel olarak pencereyi tam ekran yapın
```

**✓ Kristal Tespit İyileştirme:**
```python
# Kristal boyutlarını ayarlayın
GameIntegrationSettings.CRYSTAL_MIN_AREA = 50  # Daha küçük kristaller için azaltın
GameIntegrationSettings.CRYSTAL_MAX_AREA = 5000  # Daha büyük kristaller için artırın

# Tespit hassasiyetini artırın
GameIntegrationSettings.DETECTION_CONFIDENCE = 0.7  # 0-1 arası
```

**✓ Performans Optimizasyonu:**
```python
# Tarama hızını ayarlayın
ScanSettings.SCAN_INTERVAL = 2.0  # Taramalar arası bekleme (saniye)

# Döngü başına toplama sayısını sınırlayın
CollectorSettings.MAX_COLLECT_PER_CYCLE = 10
```

## 🎮 Bildirim Ayarları

Kristal tespiti için bildirim sistemini yapılandırın:

### Discord Bildirimi

```python
class NotificationSettings:
    # Discord webhook
    DISCORD_ENABLED = True
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_url"
```

Discord Webhook Oluşturma:
1. Discord sunucunuzda Sunucu Ayarları > Entegrasyonlar
2. Webhook'lar > Yeni Webhook
3. URL'i kopyalayın ve yapılandırmaya ekleyin

### Telegram Bildirimi

```python
class NotificationSettings:
    # Telegram bot
    TELEGRAM_ENABLED = True
    TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    TELEGRAM_CHAT_ID = "987654321"
```

Telegram Bot Oluşturma:
1. @BotFather'a mesaj gönderin
2. `/newbot` komutunu kullanın
3. Token'ı alın
4. Chat ID için bota mesaj gönderin ve ID'yi alın

## 🧪 Test

### Adım 1: Simülasyon Modunda Test

Gerçek oyuna bağlanmadan önce simülasyon modunda test edin:

```bash
# Windows
start.bat --dry-run --debug --max-time 30

# Linux/Mac
python src/main.py --dry-run --debug --max-time 30
```

### Adım 2: Gerçek Modda Kısa Test

`SIMULATION_MODE = False` yaptıktan sonra:

```bash
# Windows
start.bat --no-auto-collect --max-time 60 --no-confirm

# Linux/Mac
python src/main.py --no-auto-collect --max-time 60 --no-confirm
```

Bu mod sadece tespit eder, toplama yapmaz.

### Adım 3: Tam Fonksiyonel Test

Her şey çalışıyorsa:

```bash
# Windows
start.bat --max-time 300

# Linux/Mac
python src/main.py --max-time 300
```

## 🎯 Kristal Filtreleme

Hangi kristalleri toplayacağınızı ayarlayın:

```python
class FilterSettings:
    TARGET_LEVELS = [3, 4, 5]  # Sadece yüksek seviye kristaller
    IGNORE_LEVELS = [1, 2]  # Düşük seviye kristalleri görmezden gel
    COLLECT_HIGHEST_FIRST = True  # En yüksek seviyeyi önce topla
```

## 📊 İstatistikler ve Loglama

Bot otomatik olarak istatistik toplar:

- `logs/crystal_bot.log` - Detaylı log dosyası
- `data/session.json` - Oturum verileri

Logları görüntüleyin:

```bash
# Windows
type logs\crystal_bot.log

# Linux/Mac
tail -f logs/crystal_bot.log
```

## ⚠️ Güvenlik ve Etik Kullanım

### ⚖️ Önemli Uyarılar

1. **Oyun Kurallarına Uyun**: Bot kullanımı oyun kurallarına aykırı olabilir
2. **Rate Limiting**: Sunucuya aşırı yük bindirmeyin
3. **Adil Kullanım**: Diğer oyuncuları etkilemeyin
4. **Sorumluluk**: Hesap yasaklanma riski size aittir

### 🔒 Güvenlik Ayarları

```python
class SecuritySettings:
    RATE_LIMITING = True  # ⚠️ ASLA kapatmayın
    MAX_REQUESTS_PER_MINUTE = 30  # Oyun limitlerine uygun
    RANDOM_DELAYS = True  # Anti-detection için
    MIN_RANDOM_DELAY = 0.5
    MAX_RANDOM_DELAY = 2.0
    RESPECT_GAME_LIMITS = True  # ⚠️ ASLA kapatmayın
```

## 🐛 Sorun Giderme

### Bot Başlamıyor

1. Python versiyonunu kontrol edin: `python --version` (3.9+)
2. Bağımlılıkları yeniden yükleyin: `pip install -r requirements.txt`
3. Log dosyasını kontrol edin: `logs/crystal_bot.log`

### Ekran Otomasyonu Sorunları

**Oyun Penceresi Bulunamıyor:**
```
1. Oyun açık mı? Oyunu başlatın
2. Pencere başlığını kontrol edin - "League of Kingdoms" içermeli
3. settings.py'de GAME_WINDOW_TITLE'ı düzenleyin
4. Bot'u admin olarak çalıştırmayı deneyin
```

**Kristaller Tespit Edilmiyor:**
```
1. SIMULATION_MODE = False olmalı
2. AUTOMATION_METHOD = "screen" olmalı
3. Oyun zoom seviyesini değiştirmeyin
4. Harita net görünüyor mu?
5. CRYSTAL_MIN_AREA ve CRYSTAL_MAX_AREA ayarlarını düzenleyin
```

**Fare Hareketi Yavaş veya Hızlı:**
```python
# settings.py
GameIntegrationSettings.MOVEMENT_SPEED = 0.5  # 0.1-2.0 arası ayarlayın
GameIntegrationSettings.CLICK_DELAY = 0.2  # Tıklama gecikmesi
```

**Bağımlılık Hataları:**
```bash
# Tüm ekran otomasyonu paketlerini yükleyin
pip install pyautogui pillow opencv-python pytesseract pygetwindow mss

# Windows'ta Tesseract OCR gerekiyorsa:
# https://github.com/UB-Mannheim/tesseract/wiki adresinden indirin
```

**Bot Pencereyi Kaybediyor:**
```python
# Pencereyi otomatik aktif et
GameIntegrationSettings.AUTO_FOCUS_WINDOW = True

# Oyun penceresini tam ekran yapmayın, pencere modunda kullanın
```

### Bağlantı Hataları (API Modu)

1. `GAME_SERVER_URL` doğru mu?
2. `AUTH_TOKEN` geçerli mi?
3. İnternet bağlantınız aktif mi?
4. Firewall/Antivirus engel oluyor mu?

### Kristal Tespit Edilmiyor (Simülasyon Modu)

1. `SIMULATION_MODE = False` olduğundan emin olun
2. `TARGET_LEVELS` ayarını kontrol edin
3. Oyun koordinatlarınız doğru mu?
4. Entegrasyon yöntemi doğru seçildi mi?

### Bildirimler Gelmiyor

**Discord:**
- Webhook URL'i doğru mu?
- `DISCORD_ENABLED = True` olduğundan emin olun

**Telegram:**
- Bot token ve chat ID doğru mu?
- Bot'a en az bir mesaj gönderdiniz mi?

### Performance Sorunları

**Bot Çok Yavaş:**
```python
# Tarama aralığını azaltın
ScanSettings.SCAN_INTERVAL = 1.0  # saniye

# Fare hızını artırın
GameIntegrationSettings.MOVEMENT_SPEED = 1.0
```

**Bot Çok Hızlı (Şüpheli):**
```python
# Güvenlik ayarlarını kontrol edin
SecuritySettings.RANDOM_DELAYS = True  # Mutlaka True
SecuritySettings.MIN_RANDOM_DELAY = 0.5
SecuritySettings.MAX_RANDOM_DELAY = 2.0

# Hız sınırlaması
SecuritySettings.RATE_LIMITING = True
SecuritySettings.MAX_REQUESTS_PER_MINUTE = 30
```

## 📞 Destek

Sorunlar için:

1. Log dosyasını kontrol edin
2. GitHub Issues'da arayın
3. Yeni issue açın (log dosyasını ekleyin)

## 📚 Ek Kaynaklar

- [README.md](README.md) - Ana dokümantasyon
- [QUICKSTART.md](QUICKSTART.md) - Hızlı başlangıç
- [GitHub Issues](https://github.com/birolservis-max/LeagueOfkingdomsSampleBot/issues)

---

**Son Güncelleme**: Şubat 2026

**Lisans**: MIT License

**Uyarı**: Bu bot eğitim amaçlıdır. Kullanım sorumluluğu kullanıcıya aittir.
