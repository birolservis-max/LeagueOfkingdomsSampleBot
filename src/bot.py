"""
Ana Bot Sınıfı
Bu modül tüm bot bileşenlerini koordine eder ve yönetir.
"""

import logging
from typing import Optional, Dict, List
import time
import signal
import sys

from config.settings import (
    BotSettings,
    ScanSettings,
    FilterSettings,
    CollectorSettings,
    NotificationSettings,
    GameIntegrationSettings
)
from src.map_scanner import MapScanner
from src.crystal_detector import CrystalDetector
from src.crystal_collector import CrystalCollector
from src.notifier import Notifier
from src.utils import (
    setup_logging,
    save_session,
    load_session,
    get_timestamp
)


class CrystalBot:
    """
    Ana Bot Sınıfı - Crystal Bot Orkestratörü
    
    Tüm modülleri koordine eder ve çalışma döngüsünü yönetir:
    scan → detect → filter → collect/notify → repeat
    """
    
    def __init__(
        self,
        center_position: tuple = (0, 0),
        scan_range: int = ScanSettings.MAX_SCAN_RANGE,
        debug_mode: bool = BotSettings.DEBUG_MODE
    ):
        """
        CrystalBot başlatıcı.
        
        Args:
            center_position: Başlangıç merkez koordinatı
            scan_range: Tarama menzili
            debug_mode: Debug modu
        """
        # Logging kurulumu
        self.logger = setup_logging(
            log_file=NotificationSettings.LOG_FILE_PATH,
            level=logging.DEBUG if debug_mode else logging.INFO,
            debug_mode=debug_mode
        )
        
        self.logger.info(f"=== {BotSettings.BOT_NAME} v{BotSettings.VERSION} ===")
        self.logger.info("Bot başlatılıyor...")
        
        # Bot durumu
        self.running = False
        self.paused = False
        self.session_start_time = None
        self.total_cycles = 0
        
        # Ekran otomasyonu modüllerini başlat (eğer screen modu aktifse)
        self.screen = None
        self.navigator = None
        self.image_detector = None
        
        if (GameIntegrationSettings.AUTOMATION_METHOD == "screen" and 
            not GameIntegrationSettings.SIMULATION_MODE):
            try:
                from src.screen_automation import ScreenAutomation
                from src.game_navigator import GameNavigator
                from src.image_detector import ImageDetector
                
                self.logger.info("Ekran otomasyonu modülleri yükleniyor...")
                
                self.screen = ScreenAutomation()
                self.navigator = GameNavigator(self.screen)
                self.image_detector = ImageDetector()
                
                # Oyun penceresini bul
                if self.screen.find_game_window():
                    self.navigator.calibrate_map()
                    self.logger.info("Ekran otomasyonu hazır")
                else:
                    self.logger.warning(
                        "Oyun penceresi bulunamadı. Lütfen oyunu açın ve pencere başlığında "
                        "'League of Kingdoms' olduğundan emin olun."
                    )
                    
            except ImportError as e:
                self.logger.error(
                    f"Ekran otomasyonu bağımlılıkları yüklenemedi: {e}\n"
                    "Lütfen şu komutu çalıştırın: pip install pyautogui pillow opencv-python pytesseract pygetwindow mss"
                )
                self.screen = None
                self.navigator = None
                self.image_detector = None
        
        # Modülleri başlat
        self.scanner = MapScanner(
            center_position=center_position,
            scan_range=scan_range,
            scan_pattern=ScanSettings.SCAN_PATTERN
        )
        
        self.detector = CrystalDetector(
            enable_filtering=FilterSettings.ENABLED
        )
        
        self.collector = CrystalCollector(
            auto_collect=CollectorSettings.AUTO_COLLECT,
            dry_run=BotSettings.DRY_RUN,
            screen_automation=self.screen,
            game_navigator=self.navigator
        )
        
        self.notifier = Notifier(
            console_enabled=NotificationSettings.CONSOLE_ENABLED,
            file_logging=NotificationSettings.FILE_LOGGING,
            log_file_path=NotificationSettings.LOG_FILE_PATH
        )
        
        # Oturum yönetimi
        self.session_data = {}
        if BotSettings.SAVE_SESSION:
            self._load_session()
        
        # Sinyal işleyicileri (Ctrl+C için)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("Bot başarıyla başlatıldı")
    
    def start(self) -> None:
        """Bot'u başlatır ve ana döngüyü çalıştırır."""
        if self.running:
            self.logger.warning("Bot zaten çalışıyor")
            return
        
        self.running = True
        self.paused = False
        self.session_start_time = time.time()
        
        self.logger.info("Bot çalışmaya başladı")
        self.notifier.notify_info("Bot çalışmaya başladı")
        
        try:
            self._run_main_loop()
        except Exception as e:
            self.logger.error(f"Bot çalışma hatası: {e}", exc_info=True)
            self.notifier.notify_error("Bot çalışma hatası", e)
            
            if BotSettings.AUTO_RESTART:
                self.logger.info("Bot otomatik olarak yeniden başlatılıyor...")
                time.sleep(5)
                self.start()
            else:
                self.stop()
    
    def _run_main_loop(self) -> None:
        """Ana çalışma döngüsü: scan → detect → filter → collect/notify → repeat"""
        while self.running:
            if self.paused:
                self.logger.debug("Bot duraklatıldı, bekleniyor...")
                time.sleep(1)
                continue
            
            try:
                # Maksimum çalışma süresi kontrolü
                if BotSettings.MAX_RUN_TIME > 0:
                    elapsed = time.time() - self.session_start_time
                    if elapsed > BotSettings.MAX_RUN_TIME:
                        self.logger.info("Maksimum çalışma süresine ulaşıldı")
                        break
                
                # Bir döngü çalıştır
                self._run_cycle()
                
                # Döngü sayacını artır
                self.total_cycles += 1
                
                # Döngüler arası bekleme
                time.sleep(ScanSettings.SCAN_INTERVAL)
                
            except KeyboardInterrupt:
                self.logger.info("Kullanıcı tarafından durduruldu")
                break
            except Exception as e:
                self.logger.error(f"Döngü hatası: {e}", exc_info=True)
                
                if BotSettings.PAUSE_ON_ERROR:
                    self.pause()
                    self.notifier.notify_error("Döngü hatası, bot duraklatıldı", e)
                else:
                    self.notifier.notify_error("Döngü hatası", e)
        
        self.stop()
    
    def _run_cycle(self) -> None:
        """Tek bir bot döngüsü çalıştırır."""
        cycle_start = time.time()
        self.logger.info(f"--- Döngü #{self.total_cycles + 1} Başladı ---")
        
        # Ekran otomasyonu modu
        if (GameIntegrationSettings.AUTOMATION_METHOD == "screen" and 
            self.screen and self.image_detector and not GameIntegrationSettings.SIMULATION_MODE):
            self._run_cycle_screen_mode()
            return
        
        # Normal mod (simülasyon veya API)
        # 1. TARAMA: Haritayı tara
        self.logger.info("Adım 1: Harita taranıyor...")
        scan_results = self.scanner.scan_area(
            target_terrain_levels=self._get_target_terrain_levels(),
            max_scans=CollectorSettings.MAX_COLLECT_PER_CYCLE * 2  # Daha fazla tara
        )
        
        if not scan_results:
            self.logger.info("Tarama sonucu bulunamadı")
            return
        
        # 2. TESPİT: Kristalleri tespit et
        self.logger.info("Adım 2: Kristaller tespit ediliyor...")
        detected_crystals = self.detector.detect_crystals_in_area(scan_results)
        
        if not detected_crystals:
            self.logger.info("Kristal tespit edilemedi")
            return
        
        # Bildirimleri gönder
        self.notifier.notify_multiple_detected(detected_crystals)
        
        # 3. FİLTRELEME VE SIRALAMA: Kristalleri filtrele ve sırala
        self.logger.info("Adım 3: Kristaller filtreleniyor ve sıralanıyor...")
        filtered_crystals = self.detector.sort_by_priority(detected_crystals)
        
        # 4. TOPLAMA: Kristalleri topla (otomatik toplama açıksa)
        if CollectorSettings.AUTO_COLLECT:
            self.logger.info("Adım 4: Kristaller toplanıyor...")
            
            collection_results = self.collector.collect_multiple(
                filtered_crystals,
                max_collect=CollectorSettings.MAX_COLLECT_PER_CYCLE
            )
            
            # Toplama özetini bildir
            self.notifier.notify_collection_summary(collection_results)
        else:
            self.logger.info("Adım 4: Otomatik toplama kapalı, atlandı")
        
        # Döngü süresi
        cycle_duration = time.time() - cycle_start
        self.logger.info(
            f"--- Döngü #{self.total_cycles + 1} Tamamlandı "
            f"(Süre: {cycle_duration:.2f}s) ---"
        )
        
        # Oturumu kaydet
        if BotSettings.SAVE_SESSION:
            self._save_session()
    
    def _run_cycle_screen_mode(self) -> None:
        """Ekran otomasyonu modunda tek bir bot döngüsü çalıştırır."""
        cycle_start = time.time()
        self.logger.info("Ekran otomasyonu modu - Tarama başlıyor...")
        
        try:
            # 1. EKRAN GÖRÜNTÜSÜ AL
            screenshot = self.screen.capture_screen()
            if screenshot is None:
                self.logger.error("Ekran görüntüsü alınamadı")
                return
            
            # 2. GÖRÜNTÜDE KRİSTALLERİ TESPİT ET
            self.logger.info("Adım 1: Ekranda kristaller tespit ediliyor...")
            detected_crystals = self.image_detector.detect_crystals_in_image(
                screenshot,
                target_levels=FilterSettings.TARGET_LEVELS
            )
            
            if not detected_crystals:
                self.logger.info("Ekranda kristal bulunamadı, harita kaydırılıyor...")
                # Haritayı rastgele bir yöne kaydır
                import random
                region = self.screen.get_game_region()
                if region:
                    x, y, w, h = region
                    center_x, center_y = x + w // 2, y + h // 2
                    # Rastgele yön
                    angle = random.uniform(0, 2 * 3.14159)
                    import math
                    offset = 100
                    target_x = center_x + int(offset * math.cos(angle))
                    target_y = center_y + int(offset * math.sin(angle))
                    self.navigator.move_to_position(target_x, target_y, smooth=True)
                return
            
            self.logger.info(f"{len(detected_crystals)} kristal tespit edildi")
            
            # 3. KRİSTALLERİ SIRALA (öncelik bazlı)
            detected_crystals.sort(key=lambda c: c['level'], reverse=True)
            
            # Tespit edilen kristalleri bildir
            self.notifier.notify_info(
                f"{len(detected_crystals)} kristal tespit edildi (Seviyeler: "
                f"{[c['level'] for c in detected_crystals]})"
            )
            
            # 4. KRİSTALLERİ TOPLA
            if CollectorSettings.AUTO_COLLECT:
                self.logger.info("Adım 2: Kristaller toplanıyor...")
                
                collected = 0
                failed = 0
                max_collect = min(len(detected_crystals), CollectorSettings.MAX_COLLECT_PER_CYCLE)
                
                for i, crystal_info in enumerate(detected_crystals[:max_collect]):
                    self.logger.info(f"İlerleme: {i+1}/{max_collect}")
                    
                    # Kristal objesi oluştur (basit)
                    class Crystal:
                        def __init__(self, level, position):
                            self.level = level
                            self.position = (0, 0)  # Oyun koordinatı
                            self.screen_position = position  # Ekran koordinatı
                            self.collected = False
                    
                    crystal = Crystal(crystal_info['level'], crystal_info['position'])
                    
                    # Kristali topla
                    if self.collector.collect_crystal(crystal):
                        collected += 1
                    else:
                        failed += 1
                
                # Toplama özetini bildir
                self.notifier.notify_info(
                    f"Toplama tamamlandı - Başarılı: {collected}, "
                    f"Başarısız: {failed}, Toplam: {collected + failed}"
                )
            else:
                self.logger.info("Otomatik toplama kapalı")
            
            # Döngü süresi
            cycle_duration = time.time() - cycle_start
            self.logger.info(
                f"--- Döngü #{self.total_cycles + 1} Tamamlandı "
                f"(Süre: {cycle_duration:.2f}s) ---"
            )
            
        except Exception as e:
            self.logger.error(f"Ekran modu döngü hatası: {e}", exc_info=True)
        
        # Oturumu kaydet
        if BotSettings.SAVE_SESSION:
            self._save_session()
    
    def _get_target_terrain_levels(self) -> List[int]:
        """
        Hedef kristal seviyelerine göre taranacak arazi seviyelerini belirler.
        
        Returns:
            List[int]: Hedef arazi seviyeleri
        """
        if not FilterSettings.TARGET_LEVELS:
            return [1, 2, 3, 4, 5]  # Tümü
        
        # Hedef kristal seviyelerine göre arazi seviyelerini belirle
        from config.settings import TERRAIN_CRYSTAL_MAPPING
        
        target_terrains = set()
        for terrain_level, crystal_levels in TERRAIN_CRYSTAL_MAPPING.items():
            for crystal_level in crystal_levels:
                if crystal_level in FilterSettings.TARGET_LEVELS:
                    target_terrains.add(terrain_level)
        
        return list(target_terrains)
    
    def pause(self) -> None:
        """Bot'u duraklatır."""
        if not self.running:
            self.logger.warning("Bot çalışmıyor, duraklatılamaz")
            return
        
        self.paused = True
        self.logger.info("Bot duraklatıldı")
        self.notifier.notify_info("Bot duraklatıldı")
    
    def resume(self) -> None:
        """Bot'u devam ettirir."""
        if not self.running:
            self.logger.warning("Bot çalışmıyor, devam ettirilemez")
            return
        
        if not self.paused:
            self.logger.warning("Bot zaten çalışıyor")
            return
        
        self.paused = False
        self.logger.info("Bot devam ettiriliyor")
        self.notifier.notify_info("Bot devam ettiriliyor")
    
    def stop(self) -> None:
        """Bot'u durdurur."""
        if not self.running:
            self.logger.warning("Bot zaten durmuş")
            return
        
        self.running = False
        self.paused = False
        
        self.logger.info("Bot durduruluyor...")
        
        # Ekran otomasyonu kaynaklarını temizle
        if self.screen:
            try:
                self.screen.close()
                self.logger.debug("Ekran otomasyonu kapatıldı")
            except Exception as e:
                self.logger.error(f"Ekran otomasyonu kapatma hatası: {e}")
        
        # Oturumu kaydet
        if BotSettings.SAVE_SESSION:
            self._save_session()
        
        # Özet istatistikler
        self._print_session_summary()
        
        self.logger.info("Bot durduruldu")
        self.notifier.notify_info("Bot durduruldu")
    
    def _signal_handler(self, sig, frame) -> None:
        """Sinyal işleyici (Ctrl+C için)."""
        self.logger.info("Durdurma sinyali alındı")
        self.stop()
        sys.exit(0)
    
    def _save_session(self) -> None:
        """Oturum verilerini kaydeder."""
        self.session_data = {
            "timestamp": get_timestamp(),
            "total_cycles": self.total_cycles,
            "session_duration": time.time() - self.session_start_time if self.session_start_time else 0,
            "scanner_stats": self.scanner.get_statistics(),
            "detector_stats": self.detector.get_statistics(),
            "collector_stats": self.collector.get_statistics(),
            "notifier_stats": self.notifier.get_statistics()
        }
        
        save_session(self.session_data, BotSettings.SESSION_FILE)
        self.logger.debug("Oturum kaydedildi")
    
    def _load_session(self) -> None:
        """Oturum verilerini yükler."""
        session_data = load_session(BotSettings.SESSION_FILE)
        
        if session_data:
            self.session_data = session_data
            self.logger.info("Önceki oturum yüklendi")
        else:
            self.logger.debug("Yüklenecek oturum bulunamadı")
    
    def _print_session_summary(self) -> None:
        """Oturum özetini yazdırır."""
        if not self.session_start_time:
            return
        
        duration = time.time() - self.session_start_time
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        
        self.logger.info("\n" + "=" * 60)
        self.logger.info("OTURUM ÖZETİ")
        self.logger.info("=" * 60)
        self.logger.info(f"Toplam Süre: {hours}s {minutes}d {seconds}s")
        self.logger.info(f"Toplam Döngü: {self.total_cycles}")
        self.logger.info("")
        
        # Tarama istatistikleri
        scan_stats = self.scanner.get_statistics()
        self.logger.info("TARAMA İSTATİSTİKLERİ:")
        self.logger.info(f"  Toplam Taranan: {scan_stats['total_scanned']}")
        self.logger.info(f"  Arazi Dağılımı: {scan_stats['terrain_counts']}")
        self.logger.info("")
        
        # Tespit istatistikleri
        detect_stats = self.detector.get_statistics()
        self.logger.info("TESPİT İSTATİSTİKLERİ:")
        self.logger.info(f"  Toplam Tespit: {detect_stats['total_detected']}")
        self.logger.info(f"  Seviye Dağılımı: {detect_stats['by_level']}")
        self.logger.info(f"  Toplanmamış: {detect_stats['uncollected']}")
        self.logger.info("")
        
        # Toplama istatistikleri
        collect_stats = self.collector.get_statistics()
        self.logger.info("TOPLAMA İSTATİSTİKLERİ:")
        self.logger.info(f"  Toplam Toplanan: {collect_stats['total_collected']}")
        self.logger.info(f"  Seviye Dağılımı: {collect_stats['by_level']}")
        self.logger.info(f"  Başarısız: {collect_stats['failed_collections']}")
        self.logger.info(f"  Başarı Oranı: {collect_stats['success_rate']:.2%}")
        self.logger.info("")
        
        # Bildirim istatistikleri
        notify_stats = self.notifier.get_statistics()
        self.logger.info("BİLDİRİM İSTATİSTİKLERİ:")
        self.logger.info(f"  Toplam Bildirim: {notify_stats['total_notifications']}")
        self.logger.info(f"  Tür Dağılımı: {notify_stats['by_type']}")
        
        self.logger.info("=" * 60 + "\n")
    
    def get_status(self) -> Dict:
        """
        Bot durumunu döndürür.
        
        Returns:
            Dict: Bot durum bilgileri
        """
        return {
            "running": self.running,
            "paused": self.paused,
            "total_cycles": self.total_cycles,
            "session_duration": time.time() - self.session_start_time if self.session_start_time else 0,
            "scanner": self.scanner.get_statistics(),
            "detector": self.detector.get_statistics(),
            "collector": self.collector.get_statistics(),
            "notifier": self.notifier.get_statistics()
        }
