# Hızlı Başlangıç Kılavuzu

League of Kingdoms Crystal Bot'u kullanmaya başlamak için bu kılavuzu takip edin.

## 1. Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/birolservis-max/LeagueOfkingdomsSampleBot.git
cd LeagueOfkingdomsSampleBot

# Sanal ortam oluşturun (önerilen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

## 2. Test Etme

```bash
# Tüm testleri çalıştırın
pytest tests/ -v

# Test modunda bot'u çalıştırın (15 saniye)
python src/main.py --dry-run --debug --max-time 15
```

## 3. Temel Kullanım

### İlk Çalıştırma
```bash
# Varsayılan ayarlarla başlatın
python src/main.py
```

### Özelleştirilmiş Kullanım
```bash
# Sadece yüksek seviye kristalleri topla (4 ve 5)
python src/main.py --levels 4 5

# Belirli bir bölgeyi tara
python src/main.py --center 100 200 --range 30

# Grid deseni ile tara
python src/main.py --pattern grid

# Debug modu ile çalıştır
python src/main.py --debug
```

## 4. Yapılandırma

Ayarları özelleştirmek için `config/settings.py` dosyasını düzenleyin:

```python
# Hedef kristal seviyeleri
FilterSettings.TARGET_LEVELS = [3, 4, 5]

# Otomatik toplama
CollectorSettings.AUTO_COLLECT = True

# Test modu
BotSettings.DRY_RUN = False
```

## 5. Bildirimler

### Discord Webhook
```python
NotificationSettings.DISCORD_ENABLED = True
NotificationSettings.DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
```

### Telegram Bot
```python
NotificationSettings.TELEGRAM_ENABLED = True
NotificationSettings.TELEGRAM_BOT_TOKEN = "your_bot_token"
NotificationSettings.TELEGRAM_CHAT_ID = "your_chat_id"
```

## 6. Komutlar

### Tüm Seçenekler
```bash
python src/main.py --help
```

### Yaygın Kullanım Örnekleri

**Test modu (güvenli):**
```bash
python src/main.py --dry-run --debug
```

**Sadece tespit et, toplama:**
```bash
python src/main.py --no-auto-collect
```

**1 saat çalıştır:**
```bash
python src/main.py --max-time 3600
```

**Belirli seviyedeki kristalleri topla:**
```bash
# Sadece seviye 5
python src/main.py --levels 5

# Seviye 3, 4 ve 5
python src/main.py --levels 3 4 5
```

## 7. İstatistikler

Bot çalışırken otomatik olarak istatistikler toplar:

- Taranan alan sayısı
- Tespit edilen kristal sayısı ve seviyeleri
- Toplanan kristal sayısı ve başarı oranı
- Bildirim sayısı

Bu veriler konsola ve log dosyasına (`logs/crystal_bot.log`) kaydedilir.

## 8. Sorun Giderme

### Import Hataları
```bash
# Python path'i ayarlayın
export PYTHONPATH="${PYTHONPATH}:/path/to/LeagueOfkingdomsSampleBot"
```

### Log Dosyası
Sorunları teşhis etmek için log dosyasını kontrol edin:
```bash
tail -f logs/crystal_bot.log
```

### Debug Modu
Detaylı loglama için:
```bash
python src/main.py --debug
```

## 9. Güvenli Kullanım

Bot'u ilk kez kullanırken:

1. **Test modunda başlayın:** `--dry-run` parametresi ile
2. **Düşük menzil kullanın:** `--range 10`
3. **Kısa süre çalıştırın:** `--max-time 60`
4. **Logları inceleyin:** `logs/crystal_bot.log`

## 10. Destek

Sorun yaşarsanız:

1. README.md dosyasını okuyun
2. Test dosyalarına bakın (örnekler için)
3. GitHub Issues'da sorun bildirin
4. Debug modunda log dosyasını paylaşın

## Önemli Notlar

⚠️ **Bu bot eğitim amaçlıdır**
- Oyun kurallarına uygun kullanın
- Rate limiting ayarlarını değiştirmeyin
- Diğer oyuncuları rahatsız etmeyin

✅ **İyi Uygulamalar**
- İlk kez test modunda çalıştırın
- Ayarları yavaş yavaş değiştirin
- Logları düzenli kontrol edin
- Oturum verilerini yedekleyin

---

Kolay gelsin! 🎮💎
