"""
Kristal Toplama Modülü
Bu modül tespit edilen kristalleri otomatik olarak toplar.
"""

import logging
from typing import List, Optional, Dict
import time

from config.settings import (
    CollectorSettings,
    SecuritySettings,
    BotSettings,
    GameIntegrationSettings
)
from src.utils import random_delay, format_coordinates


class CrystalCollector:
    """
    Kristal Toplama Sınıfı
    
    Tespit edilen kristalleri otomatik olarak toplar, seviye bazlı
    filtreleme yapar ve toplama istatistiklerini tutar.
    """
    
    def __init__(
        self,
        auto_collect: bool = CollectorSettings.AUTO_COLLECT,
        dry_run: bool = BotSettings.DRY_RUN,
        screen_automation=None,
        game_navigator=None
    ):
        """
        CrystalCollector başlatıcı.
        
        Args:
            auto_collect: Otomatik toplama aktif mi
            dry_run: Test modu (gerçekten toplama yapmaz)
            screen_automation: ScreenAutomation nesnesi (ekran otomasyonu için)
            game_navigator: GameNavigator nesnesi (navigasyon için)
        """
        self.logger = logging.getLogger("CrystalBot.CrystalCollector")
        self.auto_collect = auto_collect
        self.dry_run = dry_run
        
        # Ekran otomasyonu modülleri
        self.screen = screen_automation
        self.navigator = game_navigator
        
        # İstatistikler
        self.total_collected = 0
        self.collection_by_level = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.failed_collections = 0
        self.collection_history: List[Dict] = []
        
        self.logger.info(
            f"CrystalCollector başlatıldı - Otomatik: {auto_collect}, "
            f"Test Modu: {dry_run}, "
            f"Ekran Otomasyonu: {screen_automation is not None}"
        )
    
    def collect_crystal(self, crystal) -> bool:
        """
        Tek bir kristali toplar.
        
        Bu fonksiyon gerçek bir oyun entegrasyonunda fare tıklaması simülasyonu
        veya API çağrısı yapacaktır. Şimdilik simülasyon için basit bir
        algoritma kullanıyoruz.
        
        Args:
            crystal: Toplanacak kristal (Crystal objesi)
            
        Returns:
            bool: Başarılı ise True
        """
        if not self.auto_collect and not self.dry_run:
            self.logger.warning("Otomatik toplama kapalı")
            return False
        
        self.logger.info(f"Kristal toplanıyor: {crystal}")
        
        try:
            # Test modunda gerçekten toplama yapmaz
            if self.dry_run:
                self.logger.info("[TEST MODU] Kristal toplanmış gibi yapıldı")
                time.sleep(0.1)  # Simülasyon gecikmesi
                success = True
            else:
                # Gerçek toplama işlemi
                success = self._perform_collection(crystal)
            
            if success:
                # Kristali toplanmış olarak işaretle
                crystal.collected = True
                
                # İstatistikleri güncelle
                self.total_collected += 1
                self.collection_by_level[crystal.level] += 1
                
                # Geçmişe ekle
                self.collection_history.append({
                    "crystal": crystal,
                    "position": crystal.position,
                    "level": crystal.level,
                    "timestamp": time.time(),
                    "success": True
                })
                
                self.logger.info(f"✓ Kristal başarıyla toplandı: {crystal}")
                
                # Anti-detection için gecikme
                if SecuritySettings.RANDOM_DELAYS:
                    random_delay(
                        SecuritySettings.MIN_RANDOM_DELAY,
                        SecuritySettings.MAX_RANDOM_DELAY
                    )
                
                return True
            else:
                self.failed_collections += 1
                self.logger.warning(f"✗ Kristal toplama başarısız: {crystal}")
                return False
                
        except Exception as e:
            self.logger.error(f"Kristal toplama hatası: {e}")
            self.failed_collections += 1
            return False
    
    def _perform_collection(self, crystal) -> bool:
        """
        Gerçek toplama işlemini gerçekleştirir.
        
        Bu fonksiyon gerçek oyun entegrasyonunda:
        - Fare pozisyonunu kristal koordinatına taşır
        - Tıklama yapar
        - Toplama animasyonunu bekler
        - Başarıyı kontrol eder
        
        Args:
            crystal: Kristal objesi
            
        Returns:
            bool: Başarılı ise True
        """
        # Ekran otomasyonu modunda
        if (GameIntegrationSettings.AUTOMATION_METHOD == "screen" and 
            self.screen and self.navigator and not GameIntegrationSettings.SIMULATION_MODE):
            
            try:
                self.logger.info(f"Ekran otomasyonu ile kristal toplanıyor: {crystal}")
                
                # Kristale git ve tıkla
                if hasattr(crystal, 'screen_position'):
                    success = self.navigator.navigate_to_crystal(
                        crystal.screen_position,
                        click_to_collect=True
                    )
                    
                    if success:
                        # Toplama animasyonunu bekle
                        time.sleep(CollectorSettings.COLLECT_DELAY)
                        return True
                    else:
                        self.logger.warning("Kristale gidilemedi")
                        return False
                else:
                    self.logger.warning("Kristal ekran pozisyonu bulunamadı")
                    return False
                    
            except Exception as e:
                self.logger.error(f"Ekran otomasyonu toplama hatası: {e}")
                return False
        
        # Simülasyon modu veya API modu
        else:
            # Simülasyon için basit bir gecikme ve %90 başarı oranı
            time.sleep(CollectorSettings.COLLECT_DELAY)
            
            import random
            return random.random() > 0.1  # %90 başarı şansı
    
    def collect_multiple(
        self,
        crystals: List,
        max_collect: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Birden fazla kristal toplar.
        
        Args:
            crystals: Toplanacak kristaller
            max_collect: Maksimum toplama sayısı (None ise tümü)
            
        Returns:
            Dict[str, int]: Toplama sonuçları (başarılı, başarısız)
        """
        if not crystals:
            self.logger.info("Toplanacak kristal yok")
            return {"successful": 0, "failed": 0, "total": 0}
        
        self.logger.info(
            f"{len(crystals)} kristal toplama işlemi başlatılıyor "
            f"(Maksimum: {max_collect or 'sınırsız'})"
        )
        
        successful = 0
        failed = 0
        
        # Maksimum toplama sayısı kontrolü
        crystals_to_collect = crystals
        if max_collect:
            crystals_to_collect = crystals[:max_collect]
        
        for i, crystal in enumerate(crystals_to_collect, 1):
            # Zaten toplanmış mı?
            if crystal.collected:
                self.logger.debug(f"Kristal zaten toplanmış: {crystal}")
                continue
            
            self.logger.info(f"İlerleme: {i}/{len(crystals_to_collect)}")
            
            # Kristali topla
            if self.collect_crystal(crystal):
                successful += 1
            else:
                failed += 1
                
                # Başarısız toplamada tekrar dene
                if CollectorSettings.RETRY_ON_FAIL:
                    self.logger.info("Tekrar deneniyor...")
                    
                    for retry in range(CollectorSettings.MAX_RETRIES):
                        time.sleep(CollectorSettings.COLLECT_DELAY * 2)
                        
                        if self.collect_crystal(crystal):
                            successful += 1
                            failed -= 1
                            break
            
            # Döngü başına maksimum toplama kontrolü
            if max_collect and successful >= max_collect:
                break
        
        results = {
            "successful": successful,
            "failed": failed,
            "total": successful + failed
        }
        
        self.logger.info(
            f"Toplama tamamlandı - Başarılı: {successful}, "
            f"Başarısız: {failed}, Toplam: {results['total']}"
        )
        
        return results
    
    def collect_by_level(
        self,
        crystals: List,
        target_levels: List[int]
    ) -> Dict[str, int]:
        """
        Belirli seviyelerdeki kristalleri toplar.
        
        Args:
            crystals: Kristal listesi
            target_levels: Toplanacak seviyeler
            
        Returns:
            Dict[str, int]: Toplama sonuçları
        """
        filtered_crystals = [
            c for c in crystals
            if c.level in target_levels and not c.collected
        ]
        
        self.logger.info(
            f"Seviye filtreleme: {len(filtered_crystals)} kristal "
            f"(Seviyeler: {target_levels})"
        )
        
        return self.collect_multiple(filtered_crystals)
    
    def collect_highest_priority(
        self,
        crystals: List,
        count: int = 10
    ) -> Dict[str, int]:
        """
        En yüksek öncelikli kristalleri toplar.
        
        Args:
            crystals: Kristal listesi
            count: Toplanacak kristal sayısı
            
        Returns:
            Dict[str, int]: Toplama sonuçları
        """
        # Toplanmamış kristalleri al
        uncollected = [c for c in crystals if not c.collected]
        
        # Seviyeye göre sırala (yüksek seviye önce)
        sorted_crystals = sorted(uncollected, key=lambda c: c.level, reverse=True)
        
        # İlk N tanesini al
        priority_crystals = sorted_crystals[:count]
        
        self.logger.info(
            f"Öncelikli toplama: {len(priority_crystals)} kristal "
            f"(İlk {count} tanesi)"
        )
        
        return self.collect_multiple(priority_crystals)
    
    def get_collection_rate(self) -> float:
        """
        Toplama başarı oranını hesaplar.
        
        Returns:
            float: Başarı oranı (0-1)
        """
        total_attempts = self.total_collected + self.failed_collections
        
        if total_attempts == 0:
            return 0.0
        
        return self.total_collected / total_attempts
    
    def get_statistics(self) -> Dict:
        """
        Toplama istatistiklerini döndürür.
        
        Returns:
            Dict: İstatistik bilgileri
        """
        return {
            "total_collected": self.total_collected,
            "by_level": self.collection_by_level.copy(),
            "failed_collections": self.failed_collections,
            "success_rate": self.get_collection_rate(),
            "history_count": len(self.collection_history),
            "auto_collect": self.auto_collect,
            "dry_run": self.dry_run
        }
    
    def get_recent_collections(self, count: int = 10) -> List[Dict]:
        """
        Son toplanan kristalleri döndürür.
        
        Args:
            count: Döndürülecek kristal sayısı
            
        Returns:
            List[Dict]: Son toplanan kristaller
        """
        return self.collection_history[-count:]
    
    def reset_statistics(self) -> None:
        """İstatistikleri sıfırlar."""
        self.total_collected = 0
        self.collection_by_level = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.failed_collections = 0
        self.collection_history.clear()
        self.logger.info("Toplama istatistikleri sıfırlandı")
    
    def enable_auto_collect(self) -> None:
        """Otomatik toplamayı aktif eder."""
        self.auto_collect = True
        self.logger.info("Otomatik toplama aktif edildi")
    
    def disable_auto_collect(self) -> None:
        """Otomatik toplamayı devre dışı bırakır."""
        self.auto_collect = False
        self.logger.info("Otomatik toplama devre dışı bırakıldı")
