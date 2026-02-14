"""
Kristal Tespit Modülü
Bu modül harita üzerinde kristalleri tespit eder ve seviyelerini belirler.
"""

import logging
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import time
import random

from config.settings import (
    CRYSTAL_LEVELS,
    TERRAIN_CRYSTAL_MAPPING,
    FilterSettings
)
from src.utils import (
    validate_crystal_level,
    get_crystal_name,
    format_coordinates
)


@dataclass
class Crystal:
    """Kristal bilgilerini tutar."""
    position: Tuple[int, int]
    level: int
    name: str
    color: str
    terrain_level: int
    detected_at: float
    collected: bool = False
    
    def __str__(self) -> str:
        """String representasyonu."""
        return (
            f"{self.name} - Pozisyon: {format_coordinates(*self.position)}, "
            f"Arazi Seviyesi: {self.terrain_level}"
        )


class CrystalDetector:
    """
    Kristal Tespit Sınıfı
    
    Harita üzerindeki kristalleri tespit eder, seviyelerini belirler
    ve filtreleme yapar.
    """
    
    def __init__(self, enable_filtering: bool = FilterSettings.ENABLED):
        """
        CrystalDetector başlatıcı.
        
        Args:
            enable_filtering: Filtreleme aktif mi
        """
        self.logger = logging.getLogger("CrystalBot.CrystalDetector")
        self.enable_filtering = enable_filtering
        
        # Tespit edilen kristaller
        self.detected_crystals: List[Crystal] = []
        
        # İstatistikler
        self.detection_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.total_detected = 0
        
        self.logger.info(
            f"CrystalDetector başlatıldı - Filtreleme: {enable_filtering}"
        )
    
    def detect_crystal_at_position(
        self,
        position: Tuple[int, int],
        terrain_level: int
    ) -> Optional[Crystal]:
        """
        Belirli bir pozisyonda kristal tespit eder.
        
        Bu fonksiyon gerçek bir oyun entegrasyonunda ekran görüntüsü analizi
        veya API çağrısı yapacaktır. Şimdilik simülasyon için basit bir
        algoritma kullanıyoruz.
        
        Args:
            position: Koordinat
            terrain_level: Arazi seviyesi
            
        Returns:
            Optional[Crystal]: Tespit edilen kristal veya None
        """
        # Simülasyon: %30 şansla kristal bulunur
        if random.random() > 0.3:
            return None
        
        # Bu arazide bulunabilecek kristal seviyelerini al
        possible_levels = TERRAIN_CRYSTAL_MAPPING.get(terrain_level, [])
        
        if not possible_levels:
            return None
        
        # Rastgele bir kristal seviyesi seç
        crystal_level = random.choice(possible_levels)
        
        # Kristal bilgilerini al
        crystal_info = CRYSTAL_LEVELS.get(crystal_level)
        
        if not crystal_info:
            self.logger.warning(f"Geçersiz kristal seviyesi: {crystal_level}")
            return None
        
        # Kristal objesi oluştur
        crystal = Crystal(
            position=position,
            level=crystal_level,
            name=crystal_info.name,
            color=crystal_info.color,
            terrain_level=terrain_level,
            detected_at=time.time()
        )
        
        self.logger.debug(f"Kristal tespit edildi: {crystal}")
        return crystal
    
    def detect_crystals_in_area(
        self,
        scan_results: List
    ) -> List[Crystal]:
        """
        Bir alanda kristalleri tespit eder.
        
        Args:
            scan_results: MapScanner'dan gelen tarama sonuçları
            
        Returns:
            List[Crystal]: Tespit edilen kristaller
        """
        self.logger.info("Alan kristal tespiti başlatılıyor...")
        
        detected = []
        
        for result in scan_results:
            crystal = self.detect_crystal_at_position(
                result.position,
                result.terrain_level
            )
            
            if crystal:
                # Filtreleme kontrolü
                if self.should_include_crystal(crystal):
                    detected.append(crystal)
                    self.detected_crystals.append(crystal)
                    
                    # İstatistikleri güncelle
                    self.detection_count[crystal.level] += 1
                    self.total_detected += 1
        
        self.logger.info(
            f"Kristal tespiti tamamlandı - Toplam: {len(detected)}"
        )
        
        return detected
    
    def should_include_crystal(self, crystal: Crystal) -> bool:
        """
        Kristalin filtreleme kurallarına göre dahil edilip edilmeyeceğini kontrol eder.
        
        Args:
            crystal: Kristal
            
        Returns:
            bool: Dahil edilecekse True
        """
        if not self.enable_filtering:
            return True
        
        # Göz ardı edilecek seviyeler
        if crystal.level in FilterSettings.IGNORE_LEVELS:
            self.logger.debug(f"Kristal filtrelendi (ignore): {crystal}")
            return False
        
        # Hedef seviyeler
        if FilterSettings.TARGET_LEVELS:
            if crystal.level not in FilterSettings.TARGET_LEVELS:
                self.logger.debug(f"Kristal filtrelendi (target): {crystal}")
                return False
        
        return True
    
    def filter_by_level(
        self,
        crystals: List[Crystal],
        levels: List[int]
    ) -> List[Crystal]:
        """
        Kristalleri seviyeye göre filtreler.
        
        Args:
            crystals: Kristal listesi
            levels: İstenilen seviyeler
            
        Returns:
            List[Crystal]: Filtrelenmiş kristaller
        """
        filtered = [c for c in crystals if c.level in levels]
        self.logger.debug(
            f"{len(crystals)} kristalden {len(filtered)} tanesi filtrelendi"
        )
        return filtered
    
    def filter_by_terrain(
        self,
        crystals: List[Crystal],
        terrain_levels: List[int]
    ) -> List[Crystal]:
        """
        Kristalleri arazi seviyesine göre filtreler.
        
        Args:
            crystals: Kristal listesi
            terrain_levels: İstenilen arazi seviyeleri
            
        Returns:
            List[Crystal]: Filtrelenmiş kristaller
        """
        filtered = [c for c in crystals if c.terrain_level in terrain_levels]
        self.logger.debug(
            f"{len(crystals)} kristalden {len(filtered)} tanesi arazi seviyesine göre filtrelendi"
        )
        return filtered
    
    def sort_by_priority(self, crystals: List[Crystal]) -> List[Crystal]:
        """
        Kristalleri önceliğe göre sıralar.
        
        Args:
            crystals: Kristal listesi
            
        Returns:
            List[Crystal]: Sıralanmış kristaller
        """
        if not FilterSettings.PRIORITY_BASED:
            return crystals
        
        # Yüksek seviye önce ise
        if FilterSettings.COLLECT_HIGHEST_FIRST:
            sorted_crystals = sorted(crystals, key=lambda c: c.level, reverse=True)
        else:
            sorted_crystals = sorted(crystals, key=lambda c: c.level)
        
        self.logger.debug(f"{len(crystals)} kristal önceliğe göre sıralandı")
        return sorted_crystals
    
    def get_highest_level_crystals(
        self,
        crystals: Optional[List[Crystal]] = None,
        min_level: int = 3
    ) -> List[Crystal]:
        """
        En yüksek seviye kristalleri döndürür.
        
        Args:
            crystals: Kristal listesi (None ise tümü)
            min_level: Minimum seviye
            
        Returns:
            List[Crystal]: Yüksek seviye kristaller
        """
        crystal_list = crystals if crystals else self.detected_crystals
        
        high_level = [c for c in crystal_list if c.level >= min_level]
        
        self.logger.info(
            f"{len(high_level)} adet seviye {min_level}+ kristal bulundu"
        )
        
        return high_level
    
    def get_crystals_by_level(self, level: int) -> List[Crystal]:
        """
        Belirli bir seviyedeki kristalleri döndürür.
        
        Args:
            level: Kristal seviyesi
            
        Returns:
            List[Crystal]: İlgili seviyedeki kristaller
        """
        if not validate_crystal_level(level):
            self.logger.warning(f"Geçersiz kristal seviyesi: {level}")
            return []
        
        crystals = [c for c in self.detected_crystals if c.level == level]
        
        self.logger.debug(f"Seviye {level}: {len(crystals)} kristal")
        return crystals
    
    def get_uncollected_crystals(self) -> List[Crystal]:
        """
        Henüz toplanmamış kristalleri döndürür.
        
        Returns:
            List[Crystal]: Toplanmamış kristaller
        """
        uncollected = [c for c in self.detected_crystals if not c.collected]
        self.logger.debug(f"{len(uncollected)} kristal henüz toplanmadı")
        return uncollected
    
    def mark_as_collected(self, crystal: Crystal) -> None:
        """
        Kristali toplanmış olarak işaretler.
        
        Args:
            crystal: Kristal
        """
        crystal.collected = True
        self.logger.debug(f"Kristal toplanmış olarak işaretlendi: {crystal}")
    
    def get_statistics(self) -> Dict:
        """
        Tespit istatistiklerini döndürür.
        
        Returns:
            Dict: İstatistik bilgileri
        """
        uncollected = len(self.get_uncollected_crystals())
        collected = self.total_detected - uncollected
        
        return {
            "total_detected": self.total_detected,
            "by_level": self.detection_count.copy(),
            "uncollected": uncollected,
            "collected": collected,
            "filtering_enabled": self.enable_filtering
        }
    
    def reset(self) -> None:
        """Dedektörü sıfırlar."""
        self.detected_crystals.clear()
        self.detection_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.total_detected = 0
        self.logger.info("CrystalDetector sıfırlandı")
