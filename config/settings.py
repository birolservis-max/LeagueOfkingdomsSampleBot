"""
League of Kingdoms Bot - Yapılandırma Ayarları
Bu modül bot'un tüm yapılandırma ayarlarını içerir.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class CrystalLevel:
    """Kristal seviye bilgilerini tutar."""
    level: int
    name: str
    color: str  # Tespit için renk kodu
    min_terrain_level: int  # Bu kristali bulabileceğiniz minimum arazi seviyesi
    max_terrain_level: int  # Bu kristali bulabileceğiniz maksimum arazi seviyesi
    priority: int  # Toplama önceliği (1 = en yüksek)


# Kristal Seviye Tanımları
CRYSTAL_LEVELS: Dict[int, CrystalLevel] = {
    1: CrystalLevel(
        level=1,
        name="Seviye 1 Kristal",
        color="#FFFFFF",  # Beyaz
        min_terrain_level=1,
        max_terrain_level=2,
        priority=5
    ),
    2: CrystalLevel(
        level=2,
        name="Seviye 2 Kristal",
        color="#00FF00",  # Yeşil
        min_terrain_level=2,
        max_terrain_level=3,
        priority=4
    ),
    3: CrystalLevel(
        level=3,
        name="Seviye 3 Kristal",
        color="#0000FF",  # Mavi
        min_terrain_level=3,
        max_terrain_level=4,
        priority=3
    ),
    4: CrystalLevel(
        level=4,
        name="Seviye 4 Kristal",
        color="#FF00FF",  # Mor
        min_terrain_level=4,
        max_terrain_level=5,
        priority=2
    ),
    5: CrystalLevel(
        level=5,
        name="Seviye 5 Kristal",
        color="#FFD700",  # Altın
        min_terrain_level=5,
        max_terrain_level=5,
        priority=1
    ),
}


# Arazi Seviye - Kristal Seviye Eşleştirme Tablosu
TERRAIN_CRYSTAL_MAPPING: Dict[int, List[int]] = {
    1: [1],           # Seviye 1 arazide sadece Seviye 1 kristal
    2: [1, 2],        # Seviye 2 arazide Seviye 1-2 kristal
    3: [2, 3],        # Seviye 3 arazide Seviye 2-3 kristal
    4: [3, 4],        # Seviye 4 arazide Seviye 3-4 kristal
    5: [4, 5],        # Seviye 5 arazide Seviye 4-5 kristal
}


# Tarama Ayarları
class ScanSettings:
    """Harita tarama ayarları."""
    SCAN_INTERVAL: float = 2.0  # Tarama aralığı (saniye)
    SCAN_SPEED: str = "normal"  # "slow", "normal", "fast"
    GRID_SIZE: int = 100  # Harita grid boyutu
    MAX_SCAN_RANGE: int = 50  # Maksimum tarama menzili
    MIN_SCAN_RANGE: int = 10  # Minimum tarama menzili
    SCAN_PATTERN: str = "spiral"  # "spiral", "grid", "random"


# Filtreleme Ayarları
class FilterSettings:
    """Kristal filtreleme ayarları."""
    ENABLED: bool = True  # Filtreleme açık/kapalı
    TARGET_LEVELS: List[int] = [3, 4, 5]  # Aranacak kristal seviyeleri
    IGNORE_LEVELS: List[int] = [1, 2]  # Göz ardı edilecek seviyeler
    PRIORITY_BASED: bool = True  # Öncelik bazlı toplama
    COLLECT_HIGHEST_FIRST: bool = True  # En yüksek seviyeyi önce topla


# Toplama Ayarları
class CollectorSettings:
    """Kristal toplama ayarları."""
    AUTO_COLLECT: bool = True  # Otomatik toplama açık/kapalı
    COLLECT_DELAY: float = 1.0  # Toplama işlemleri arası bekleme süresi (saniye)
    MAX_COLLECT_PER_CYCLE: int = 10  # Döngü başına maksimum toplama sayısı
    COLLECT_TIMEOUT: float = 5.0  # Toplama zaman aşımı (saniye)
    RETRY_ON_FAIL: bool = True  # Başarısız toplamayı tekrar dene
    MAX_RETRIES: int = 3  # Maksimum deneme sayısı


# Bildirim Ayarları
class NotificationSettings:
    """Bildirim sistemi ayarları."""
    ENABLED: bool = True  # Bildirimler açık/kapalı
    CONSOLE_ENABLED: bool = True  # Konsol bildirimi
    FILE_LOGGING: bool = True  # Dosyaya loglama
    LOG_FILE_PATH: str = "logs/crystal_bot.log"  # Log dosyası yolu
    
    # Discord Webhook (opsiyonel)
    DISCORD_ENABLED: bool = False
    DISCORD_WEBHOOK_URL: str = ""  # Discord webhook URL'i buraya
    
    # Telegram Bot (opsiyonel)
    TELEGRAM_ENABLED: bool = False
    TELEGRAM_BOT_TOKEN: str = ""  # Telegram bot token buraya
    TELEGRAM_CHAT_ID: str = ""  # Telegram chat ID buraya
    
    # Bildirim içeriği
    INCLUDE_COORDINATES: bool = True  # Koordinatları dahil et
    INCLUDE_TIMESTAMP: bool = True  # Zaman damgası dahil et
    INCLUDE_LEVEL: bool = True  # Kristal seviyesini dahil et
    INCLUDE_SCREENSHOT: bool = False  # Ekran görüntüsü dahil et


# Bot Genel Ayarları
class BotSettings:
    """Bot genel ayarları."""
    BOT_NAME: str = "LeagueOfKingdoms Crystal Bot"
    VERSION: str = "1.0.0"
    DEBUG_MODE: bool = False  # Debug modu
    DRY_RUN: bool = False  # Test modu (gerçekten toplama yapmaz)
    MAX_RUN_TIME: int = 3600  # Maksimum çalışma süresi (saniye), 0 = sınırsız
    PAUSE_ON_ERROR: bool = True  # Hata durumunda duraklat
    AUTO_RESTART: bool = True  # Hata sonrası otomatik yeniden başlat
    SAVE_SESSION: bool = True  # Oturum kaydet
    SESSION_FILE: str = "data/session.json"  # Oturum dosyası


# Gerçek Oyun Entegrasyon Ayarları
class GameIntegrationSettings:
    """Gerçek League of Kingdoms oyunu entegrasyon ayarları."""
    
    # Oyun Bağlantı Ayarları
    GAME_SERVER_URL: str = ""  # Oyun sunucu URL'i (örn: "https://game.leagueofkingdoms.com")
    API_ENDPOINT: str = ""  # API endpoint (örn: "/api/v1")
    USE_API: bool = False  # API kullanımı açık/kapalı
    
    # Kimlik Doğrulama
    AUTH_TOKEN: str = ""  # Oyun kimlik doğrulama token'ı
    USER_ID: str = ""  # Kullanıcı ID
    SESSION_ID: str = ""  # Oturum ID
    
    # Ekran Görüntü Ayarları (OCR/Image Recognition için)
    USE_SCREEN_CAPTURE: bool = False  # Ekran yakalama kullan
    SCREEN_REGION: tuple = (0, 0, 1920, 1080)  # Yakalama bölgesi (x, y, width, height)
    OCR_ENABLED: bool = False  # OCR (Optik Karakter Tanıma) kullan
    IMAGE_RECOGNITION: bool = False  # Görüntü tanıma kullan
    
    # Oyun Etkileşim Ayarları
    USE_MOUSE_CONTROL: bool = False  # Fare kontrolü kullan
    USE_KEYBOARD_CONTROL: bool = False  # Klavye kontrolü kullan
    AUTOMATION_METHOD: str = "api"  # "api", "screen", "hybrid"
    
    # Bağlantı Ayarları
    CONNECTION_TIMEOUT: int = 30  # Bağlantı zaman aşımı (saniye)
    REQUEST_RETRY_COUNT: int = 3  # Başarısız istek tekrar sayısı
    RETRY_DELAY: float = 2.0  # Tekrar denemeler arası bekleme (saniye)
    
    # Senkronizasyon
    SYNC_INTERVAL: float = 5.0  # Oyun durumu senkronizasyon aralığı (saniye)
    AUTO_SYNC: bool = True  # Otomatik senkronizasyon
    
    # Simülasyon Modu (Gerçek oyun yerine simülasyon)
    SIMULATION_MODE: bool = True  # True = Simülasyon, False = Gerçek oyun
    
    # Güvenlik Kontrolleri
    VERIFY_SSL: bool = True  # SSL sertifika doğrulama
    ENABLE_PROXY: bool = False  # Proxy kullanımı
    PROXY_URL: str = ""  # Proxy URL (örn: "http://proxy.example.com:8080")


# Performans Ayarları
class PerformanceSettings:
    """Performans ve optimizasyon ayarları."""
    USE_ASYNC: bool = True  # Asenkron işlemler kullan
    THREAD_POOL_SIZE: int = 4  # Thread havuzu boyutu
    CACHE_ENABLED: bool = True  # Önbellek kullan
    CACHE_TTL: int = 300  # Önbellek yaşam süresi (saniye)
    MEMORY_LIMIT_MB: int = 512  # Maksimum bellek kullanımı (MB)


# Güvenlik Ayarları
class SecuritySettings:
    """Güvenlik ve etik kullanım ayarları."""
    RATE_LIMITING: bool = True  # Hız sınırlama
    MAX_REQUESTS_PER_MINUTE: int = 30  # Dakikada maksimum istek sayısı
    RANDOM_DELAYS: bool = True  # Rastgele gecikmeler ekle
    MIN_RANDOM_DELAY: float = 0.5  # Minimum rastgele gecikme (saniye)
    MAX_RANDOM_DELAY: float = 2.0  # Maksimum rastgele gecikme (saniye)
    RESPECT_GAME_LIMITS: bool = True  # Oyun limitlerini gözetle
