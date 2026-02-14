# League of Kingdoms - Crystal Bot 💎

League of Kingdoms oyunu için geliştirilmiş Python tabanlı kristal tespit ve toplama botu.

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Kristal Seviyeleri](#kristal-seviyeleri)
- [Proje Yapısı](#proje-yapısı)
- [Kurulum](#kurulum)
- [Yapılandırma](#yapılandırma)
- [Kullanım](#kullanım)
- [Modüller](#modüller)
- [Test](#test)
- [Etik Kullanım Uyarısı](#etik-kullanım-uyarısı)
- [Lisans](#lisans)

## ✨ Özellikler

- 🔍 **Otomatik Kristal Tespiti**: Harita üzerinde kristalleri otomatik olarak tespit eder
- 📊 **Seviye Bazlı Filtreleme**: İstediğiniz kristal seviyelerini seçerek toplayabilirsiniz
- 🗺️ **Akıllı Harita Taraması**: Spiral, grid veya rastgele tarama desenleri
- 🎯 **Arazi Seviye Analizi**: Yüksek seviye arazilerde yüksek seviye kristaller arar
- 🤖 **Otomatik Toplama**: Tespit edilen kristalleri otomatik olarak toplar
- 🔔 **Bildirim Sistemi**: Konsol, dosya, Discord ve Telegram desteği
- 📈 **Detaylı İstatistikler**: Toplama başarı oranı, seviye dağılımı ve daha fazlası
- ⚙️ **Esnek Yapılandırma**: Tüm ayarlar özelleştirilebilir
- 🔒 **Güvenlik**: Rate limiting ve rastgele gecikmeler ile anti-detection

## 💎 Kristal Seviyeleri

Kristaller 5 seviyeye ayrılır ve arazi seviyesine bağlı olarak bulunurlar:

| Seviye | İsim | Arazi Seviyesi | Öncelik | Renk |
|--------|------|----------------|---------|------|
| 1 | Seviye 1 Kristal | 1-2 | En Düşük | Beyaz |
| 2 | Seviye 2 Kristal | 2-3 | Düşük | Yeşil |
| 3 | Seviye 3 Kristal | 3-4 | Orta | Mavi |
| 4 | Seviye 4 Kristal | 4-5 | Yüksek | Mor |
| 5 | Seviye 5 Kristal | 5 | En Yüksek | Altın |

### Arazi-Kristal Eşleştirmesi

- **Seviye 1 Arazi**: Seviye 1 kristaller
- **Seviye 2 Arazi**: Seviye 1-2 kristaller
- **Seviye 3 Arazi**: Seviye 2-3 kristaller
- **Seviye 4 Arazi**: Seviye 3-4 kristaller
- **Seviye 5 Arazi**: Seviye 4-5 kristaller

## 📁 Proje Yapısı

```
LeagueOfkingdomsSampleBot/
├── README.md                  # Bu dosya
├── requirements.txt           # Python bağımlılıkları
├── .gitignore                 # Git ignore kuralları
├── config/
│   └── settings.py            # Bot yapılandırma ayarları
├── src/
│   ├── __init__.py
│   ├── main.py                # Ana giriş noktası
│   ├── bot.py                 # Ana bot orkestratörü
│   ├── crystal_detector.py    # Kristal tespit modülü
│   ├── crystal_collector.py   # Kristal toplama modülü
│   ├── map_scanner.py         # Harita tarama modülü
│   ├── notifier.py            # Bildirim modülü
│   └── utils.py               # Yardımcı fonksiyonlar
├── tests/
│   ├── __init__.py
│   ├── test_crystal_detector.py
│   ├── test_crystal_collector.py
│   └── test_map_scanner.py
├── logs/                      # Log dosyaları (otomatik oluşturulur)
└── data/                      # Oturum verileri (otomatik oluşturulur)
```

## 🚀 Kurulum

### Gereksinimler

- Python 3.9 veya üzeri
- pip paket yöneticisi

### Adımlar

#### Windows Kullanıcıları için Hızlı Kurulum

1. **Depoyu klonlayın:**
```bash
git clone https://github.com/birolservis-max/LeagueOfkingdomsSampleBot.git
cd LeagueOfkingdomsSampleBot
```

2. **setup.bat dosyasını çalıştırın:**
```bash
setup.bat
```

Bu script otomatik olarak:
- Python versiyonunu kontrol eder
- Sanal ortam oluşturur
- Gerekli paketleri yükler
- Klasör yapısını hazırlar

3. **Yapılandırmayı düzenleyin:**
- `config/settings.py` dosyasını düzenleyin
- Oyun sunucu ayarlarını yapılandırın
- Bildirim ayarlarını düzenleyin (Discord/Telegram)

4. **Botu başlatın:**
```bash
# Test modunda
start.bat --dry-run --debug

# Normal modda
start.bat
```

#### Linux/Mac Kullanıcıları için Manuel Kurulum

1. **Depoyu klonlayın:**
```bash
git clone https://github.com/birolservis-max/LeagueOfkingdomsSampleBot.git
cd LeagueOfkingdomsSampleBot
```

2. **Sanal ortam oluşturun (önerilen):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Gerekli klasörleri oluşturun:**
```bash
mkdir -p logs data
```

5. **Yapılandırmayı düzenleyin:**
```bash
# config/settings.py dosyasını ihtiyaçlarınıza göre düzenleyin
```

## ⚙️ Yapılandırma

Tüm ayarlar `config/settings.py` dosyasında bulunur:

### Gerçek Oyun Entegrasyonu Ayarları

```python
# Gerçek oyun entegrasyonu için ayarlar
GameIntegrationSettings.SIMULATION_MODE = False  # Gerçek oyunu kullanmak için False yapın
GameIntegrationSettings.GAME_SERVER_URL = "https://game.leagueofkingdoms.com"
GameIntegrationSettings.AUTH_TOKEN = "your_auth_token_here"
GameIntegrationSettings.USER_ID = "your_user_id"

# Entegrasyon yöntemi seçin
GameIntegrationSettings.AUTOMATION_METHOD = "api"  # "api", "screen", veya "hybrid"
GameIntegrationSettings.USE_API = True  # API kullanımı

# Ekran görüntü tabanlı entegrasyon için (opsiyonel)
GameIntegrationSettings.USE_SCREEN_CAPTURE = False
GameIntegrationSettings.OCR_ENABLED = False
```

**Önemli:** Gerçek oyun entegrasyonu için `SIMULATION_MODE = False` yapın ve gerekli kimlik doğrulama bilgilerini girin.

### Temel Ayarlar

```python
# Hedef kristal seviyeleri
FilterSettings.TARGET_LEVELS = [3, 4, 5]  # Sadece seviye 3, 4 ve 5

# Otomatik toplama
CollectorSettings.AUTO_COLLECT = True

# Tarama deseni
ScanSettings.SCAN_PATTERN = "spiral"  # "spiral", "grid" veya "random"

# Test modu (gerçekten toplama yapmaz)
BotSettings.DRY_RUN = False
```

### Bildirim Ayarları

```python
# Discord Webhook (opsiyonel)
NotificationSettings.DISCORD_ENABLED = True
NotificationSettings.DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."

# Telegram Bot (opsiyonel)
NotificationSettings.TELEGRAM_ENABLED = True
NotificationSettings.TELEGRAM_BOT_TOKEN = "your_bot_token"
NotificationSettings.TELEGRAM_CHAT_ID = "your_chat_id"
```

### Güvenlik Ayarları

```python
# Hız sınırlama
SecuritySettings.RATE_LIMITING = True
SecuritySettings.MAX_REQUESTS_PER_MINUTE = 30

# Rastgele gecikmeler (anti-detection)
SecuritySettings.RANDOM_DELAYS = True
SecuritySettings.MIN_RANDOM_DELAY = 0.5  # saniye
SecuritySettings.MAX_RANDOM_DELAY = 2.0  # saniye
```

## 📖 Kullanım

### Basit Kullanım

```bash
# Varsayılan ayarlarla başlat
python src/main.py
```

### Gelişmiş Kullanım

```bash
# Belirli bir merkez noktadan başlat
python src/main.py --center 100 200

# Belirli bir menzilde tara
python src/main.py --range 30

# Sadece yüksek seviye kristalleri topla
python src/main.py --levels 4 5

# Test modunda çalıştır (gerçekten toplama yapmaz)
python src/main.py --dry-run

# Debug modu ile çalıştır
python src/main.py --debug

# Otomatik toplamayı devre dışı bırak (sadece tespit et)
python src/main.py --no-auto-collect

# Maksimum çalışma süresi belirle (saniye)
python src/main.py --max-time 3600  # 1 saat

# Tarama deseni seç
python src/main.py --pattern grid

# Tüm parametrelerle
python src/main.py --center 100 200 --range 40 --levels 3 4 5 --pattern spiral --debug
```

### Komut Satırı Argümanları

| Argüman | Açıklama | Varsayılan |
|---------|----------|------------|
| `--center X Y` | Tarama merkez koordinatı | `0 0` |
| `--range N` | Tarama menzili | `50` |
| `--pattern TYPE` | Tarama deseni (spiral/grid/random) | `spiral` |
| `--levels L1 L2 ...` | Toplanacak kristal seviyeleri | `3 4 5` |
| `--no-auto-collect` | Otomatik toplamayı kapat | - |
| `--max-collect N` | Döngü başına maks. toplama | `10` |
| `--dry-run` | Test modu | - |
| `--debug` | Debug modu | - |
| `--max-time N` | Maksimum çalışma süresi (saniye) | `3600` |

## 🧩 Modüller

### 1. MapScanner (Harita Tarayıcı)

Haritayı sistematik olarak tarar ve arazi seviyelerini tespit eder.

**Özellikler:**
- Spiral, grid veya rastgele tarama desenleri
- Arazi seviyesi tespiti
- Kristal-arazi eşleştirmesi
- Tarama istatistikleri

### 2. CrystalDetector (Kristal Dedektörü)

Harita üzerinde kristalleri tespit eder ve seviyelerini belirler.

**Özellikler:**
- Kristal tespiti
- Seviye belirleme
- Filtreleme sistemi
- Öncelik bazlı sıralama

### 3. CrystalCollector (Kristal Toplayıcı)

Tespit edilen kristalleri otomatik olarak toplar.

**Özellikler:**
- Otomatik toplama
- Seviye bazlı filtreleme
- Toplama önceliklendirme
- Başarısız toplamada tekrar deneme
- Toplama istatistikleri

### 4. Notifier (Bildirimci)

Kristal tespit ve toplama olaylarını bildirir.

**Özellikler:**
- Konsol bildirimi
- Dosya loglaması
- Discord webhook desteği
- Telegram bot desteği
- Özelleştirilebilir bildirim formatı

### 5. CrystalBot (Ana Orkestratör)

Tüm modülleri koordine eder ve yönetir.

**İş Akışı:**
1. **Tarama**: Haritayı sistematik olarak tara
2. **Tespit**: Kristalleri tespit et ve seviyelerini belirle
3. **Filtreleme**: İstenilen kristalleri filtrele ve önceliklendir
4. **Toplama**: Kristalleri otomatik olarak topla (veya sadece bildir)
5. **Tekrar**: Döngüyü tekrarla

## 🧪 Test

### Tüm Testleri Çalıştır

```bash
pytest tests/
```

### Kapsam Raporu ile Test

```bash
pytest tests/ --cov=src --cov-report=html
```

### Belirli Bir Modülü Test Et

```bash
pytest tests/test_crystal_detector.py
pytest tests/test_crystal_collector.py
pytest tests/test_map_scanner.py
```

### Test Modu ile Bot Çalıştır

```bash
python src/main.py --dry-run --debug
```

## ⚠️ Etik Kullanım Uyarısı

Bu bot **eğitim ve araştırma amaçlıdır**. Kullanırken lütfen aşağıdaki kurallara uyun:

### ✅ Yapılması Gerekenler

- Oyunun kullanım koşullarını okuyun ve anlayın
- Bot'u adil kullanım sınırları içinde kullanın
- Rate limiting ve gecikme ayarlarını kullanın
- Diğer oyuncuların deneyimini olumsuz etkilemeyin
- Sorumluluk sahibi olun

### ❌ Yapılmaması Gerekenler

- Oyunun kullanım koşullarını ihlal etmeyin
- Sunuculara aşırı yük bindirmeyin
- Diğer oyuncuların oyun deneyimini bozmayın
- Bot'u haksız avantaj için kötüye kullanmayın
- Güvenlik açıklarını istismar etmeyin

### 🔒 Güvenlik

Bot aşağıdaki güvenlik önlemlerini içerir:

- **Rate Limiting**: İstek hızı sınırlama
- **Random Delays**: Rastgele gecikmeler (anti-detection)
- **Respectful Usage**: Oyun limitlerini gözetme
- **Session Management**: Oturum yönetimi

### ⚖️ Yasal Sorumluluk

Bu bot'un kullanımından kaynaklanan herhangi bir sorumluluk kullanıcıya aittir. Geliştiriciler, bot'un kötüye kullanılmasından sorumlu değildir.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Fork'layın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📝 Değişiklik Günlüğü

### v1.0.0 (2024)
- İlk sürüm
- Temel kristal tespit ve toplama özellikleri
- Harita tarama sistemi
- Bildirim sistemi
- Yapılandırma sistemi
- Test altyapısı

## 🐛 Bilinen Sorunlar

Şu anda bilinen kritik sorun bulunmamaktadır. Bir sorun bulursanız lütfen [issue](https://github.com/birolservis-max/LeagueOfkingdomsSampleBot/issues) açın.

## 📧 İletişim

Sorularınız veya önerileriniz için:
- GitHub Issues: [Issues](https://github.com/birolservis-max/LeagueOfkingdomsSampleBot/issues)
- GitHub Discussions: [Discussions](https://github.com/birolservis-max/LeagueOfkingdomsSampleBot/discussions)

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

**Not**: Bu bot gerçek bir oyun entegrasyonu için temel altyapıyı sağlar. Gerçek kullanım için ekran görüntüsü analizi, fare kontrolü veya API entegrasyonu gibi ek implementasyonlar gereklidir.

**Eğitim Amaçlıdır**: Bu proje Python programlama, bot geliştirme ve oyun mekaniği öğrenmek için harika bir örnektir.

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!