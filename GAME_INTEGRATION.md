# Gerçek Oyun Entegrasyonu Kılavuzu

Bu kılavuz, League of Kingdoms Crystal Bot'u gerçek oyunla entegre etmek için gerekli adımları açıklar.

## 📋 İçindekiler

- [Genel Bakış](#genel-bakış)
- [Kurulum](#kurulum)
- [Yapılandırma](#yapılandırma)
- [Entegrasyon Yöntemleri](#entegrasyon-yöntemleri)
- [Test](#test)
- [Sorun Giderme](#sorun-giderme)

## 🎯 Genel Bakış

Bu bot, League of Kingdoms oyununda kristalleri otomatik olarak tespit etmek ve bildirmek için tasarlanmıştır. Gerçek oyunla entegre edilebilmesi için üç farklı yöntem sunar:

1. **API Tabanlı Entegrasyon** - Oyunun API'sini kullanarak (önerilen)
2. **Ekran Görüntü Tabanlı** - OCR ve görüntü tanıma ile
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

#### API Entegrasyonu için
```bash
pip install requests
# Zaten requirements.txt'de mevcut
```

#### Ekran Görüntü Entegrasyonu için (Opsiyonel)
```bash
pip install pillow pytesseract opencv-python pyautogui
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

### Yöntem 1: API Tabanlı Entegrasyon (Önerilen)

API tabanlı entegrasyon, oyunun resmi API'sini kullanarak en güvenilir yöntemdir.

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

### Yöntem 2: Ekran Görüntü Tabanlı Entegrasyon

Bu yöntem ekran görüntüsü analizi ve OCR kullanır.

#### Ek Paket Kurulumu:

```bash
pip install pillow pytesseract opencv-python pyautogui
```

#### Yapılandırma:

```python
class GameIntegrationSettings:
    SIMULATION_MODE = False
    USE_API = False
    AUTOMATION_METHOD = "screen"
    
    # Ekran yakalama ayarları
    USE_SCREEN_CAPTURE = True
    SCREEN_REGION = (0, 0, 1920, 1080)  # Oyun pencere boyutu
    OCR_ENABLED = True
    IMAGE_RECOGNITION = True
    
    # Fare/Klavye kontrolü
    USE_MOUSE_CONTROL = True
    USE_KEYBOARD_CONTROL = True
```

#### Ekran Bölgesini Belirleme:

1. Oyunu tam ekran açın
2. Oyun penceresinin koordinatlarını not edin
3. `SCREEN_REGION` değerini buna göre ayarlayın

### Yöntem 3: Hibrit Entegrasyon

API ve ekran görüntü yöntemlerinin kombinasyonunu kullanır.

```python
class GameIntegrationSettings:
    SIMULATION_MODE = False
    AUTOMATION_METHOD = "hybrid"
    
    # Her iki yöntem de etkin
    USE_API = True
    USE_SCREEN_CAPTURE = True
    OCR_ENABLED = True
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

### Bağlantı Hataları

1. `GAME_SERVER_URL` doğru mu?
2. `AUTH_TOKEN` geçerli mi?
3. İnternet bağlantınız aktif mi?
4. Firewall/Antivirus engel oluyor mu?

### Kristal Tespit Edilmiyor

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
