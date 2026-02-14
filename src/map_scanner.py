"""
Harita Tarayıcı Modülü
Bu modül oyun haritasını sistematik olarak tarar ve arazi seviyelerini tespit eder.
"""

import logging
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
import time

from config.settings import (
    ScanSettings,
    TERRAIN_CRYSTAL_MAPPING,
    PerformanceSettings
)
from src.utils import (
    generate_spiral_coordinates,
    generate_grid_coordinates,
    is_within_range,
    random_delay,
    validate_terrain_level
)


@dataclass
class ScanResult:
    """Tarama sonucu bilgilerini tutar."""
    position: Tuple[int, int]
    terrain_level: int
    possible_crystals: List[int]
    timestamp: float
    scanned: bool = False


class MapScanner:
    """
    Harita Tarayıcı Sınıfı
    
    Oyun haritasını sistematik olarak tarar, arazi seviyelerini tespit eder
    ve hangi seviyelerde kristaller bulunabileceğini belirler.
    """
    
    def __init__(
        self,
        center_position: Tuple[int, int] = (0, 0),
        scan_range: int = ScanSettings.MAX_SCAN_RANGE,
        scan_pattern: str = ScanSettings.SCAN_PATTERN
    ):
        """
        MapScanner başlatıcı.
        
        Args:
            center_position: Tarama merkez noktası
            scan_range: Tarama menzili
            scan_pattern: Tarama deseni ("spiral", "grid", "random")
        """
        self.logger = logging.getLogger("CrystalBot.MapScanner")
        self.center_position = center_position
        self.scan_range = scan_range
        self.scan_pattern = scan_pattern
        
        # Taranmış alanları takip et
        self.scanned_positions: Set[Tuple[int, int]] = set()
        self.scan_results: List[ScanResult] = []
        
        # İstatistikler
        self.total_scanned = 0
        self.terrain_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        self.logger.info(
            f"MapScanner başlatıldı - Merkez: {center_position}, "
            f"Menzil: {scan_range}, Desen: {scan_pattern}"
        )
    
    def generate_scan_path(self) -> List[Tuple[int, int]]:
        """
        Tarama desenine göre koordinat yolu oluşturur.
        
        Returns:
            List[Tuple[int, int]]: Taranacak koordinatlar
        """
        if self.scan_pattern == "spiral":
            return generate_spiral_coordinates(self.center_position, self.scan_range)
        elif self.scan_pattern == "grid":
            start_x = self.center_position[0] - self.scan_range
            start_y = self.center_position[1] - self.scan_range
            grid_size = self.scan_range * 2
            return generate_grid_coordinates((start_x, start_y), grid_size, grid_size)
        else:
            # Random pattern için spiral kullan ama karıştır
            coords = generate_spiral_coordinates(self.center_position, self.scan_range)
            import random
            random.shuffle(coords)
            return coords
    
    def detect_terrain_level(self, position: Tuple[int, int]) -> int:
        """
        Verilen koordinattaki arazi seviyesini tespit eder.
        
        Bu fonksiyon gerçek bir oyun entegrasyonunda ekran tarama
        veya API çağrısı yapacaktır. Şimdilik simülasyon için basit bir
        algoritma kullanıyoruz.
        
        Args:
            position: Koordinat
            
        Returns:
            int: Arazi seviyesi (1-5)
        """
        # Simülasyon: Merkeze uzaklığa göre arazi seviyesi
        # Gerçek implementasyonda burası ekran tarama veya API çağrısı olacak
        x, y = position
        cx, cy = self.center_position
        
        distance = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        
        # Merkeze yakınsa düşük seviye, uzaksa yüksek seviye
        if distance < 10:
            return 1
        elif distance < 20:
            return 2
        elif distance < 30:
            return 3
        elif distance < 40:
            return 4
        else:
            return 5
    
    def get_possible_crystals(self, terrain_level: int) -> List[int]:
        """
        Arazi seviyesine göre bulunabilecek kristal seviyelerini döndürür.
        
        Args:
            terrain_level: Arazi seviyesi
            
        Returns:
            List[int]: Olası kristal seviyeleri
        """
        if not validate_terrain_level(terrain_level):
            self.logger.warning(f"Geçersiz arazi seviyesi: {terrain_level}")
            return []
        
        return TERRAIN_CRYSTAL_MAPPING.get(terrain_level, [])
    
    def scan_position(self, position: Tuple[int, int]) -> Optional[ScanResult]:
        """
        Tek bir koordinatı tarar.
        
        Args:
            position: Taranacak koordinat
            
        Returns:
            Optional[ScanResult]: Tarama sonucu veya None
        """
        # Daha önce tarandı mı kontrol et
        if position in self.scanned_positions:
            self.logger.debug(f"Pozisyon zaten tarandı: {position}")
            return None
        
        # Menzil içinde mi kontrol et
        if not is_within_range(position, self.center_position, self.scan_range):
            self.logger.debug(f"Pozisyon menzil dışında: {position}")
            return None
        
        try:
            # Arazi seviyesini tespit et
            terrain_level = self.detect_terrain_level(position)
            
            # Olası kristalleri bul
            possible_crystals = self.get_possible_crystals(terrain_level)
            
            # Sonucu oluştur
            result = ScanResult(
                position=position,
                terrain_level=terrain_level,
                possible_crystals=possible_crystals,
                timestamp=time.time(),
                scanned=True
            )
            
            # Kaydet
            self.scanned_positions.add(position)
            self.scan_results.append(result)
            
            # İstatistikleri güncelle
            self.total_scanned += 1
            self.terrain_counts[terrain_level] = self.terrain_counts.get(terrain_level, 0) + 1
            
            self.logger.debug(
                f"Pozisyon tarandı: {position}, Arazi Seviye: {terrain_level}, "
                f"Olası Kristaller: {possible_crystals}"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Tarama hatası ({position}): {e}")
            return None
    
    def scan_area(
        self,
        target_terrain_levels: Optional[List[int]] = None,
        max_scans: Optional[int] = None
    ) -> List[ScanResult]:
        """
        Belirli bir alanı tarar.
        
        Args:
            target_terrain_levels: Hedef arazi seviyeleri (None ise tümü)
            max_scans: Maksimum tarama sayısı (None ise sınırsız)
            
        Returns:
            List[ScanResult]: Tarama sonuçları
        """
        self.logger.info("Alan taraması başlatılıyor...")
        
        scan_path = self.generate_scan_path()
        results = []
        scanned_count = 0
        
        for position in scan_path:
            # Maksimum tarama sayısına ulaşıldı mı?
            if max_scans and scanned_count >= max_scans:
                break
            
            # Pozisyonu tara
            result = self.scan_position(position)
            
            if result:
                # Hedef arazi seviyeleri belirtilmişse filtrele
                if target_terrain_levels is None or result.terrain_level in target_terrain_levels:
                    results.append(result)
                    scanned_count += 1
                
                # Anti-detection için rastgele gecikme
                if PerformanceSettings.USE_ASYNC:
                    time.sleep(ScanSettings.SCAN_INTERVAL)
        
        self.logger.info(
            f"Alan taraması tamamlandı - Toplam: {scanned_count}, "
            f"Sonuçlar: {len(results)}"
        )
        
        return results
    
    def find_high_level_terrains(self, min_level: int = 3) -> List[ScanResult]:
        """
        Yüksek seviye arazileri bulur.
        
        Args:
            min_level: Minimum arazi seviyesi
            
        Returns:
            List[ScanResult]: Yüksek seviye arazi sonuçları
        """
        self.logger.info(f"Minimum {min_level} seviye araziler aranıyor...")
        
        high_level_results = [
            result for result in self.scan_results
            if result.terrain_level >= min_level
        ]
        
        self.logger.info(f"{len(high_level_results)} yüksek seviye arazi bulundu")
        return high_level_results
    
    def get_statistics(self) -> dict:
        """
        Tarama istatistiklerini döndürür.
        
        Returns:
            dict: İstatistik bilgileri
        """
        return {
            "total_scanned": self.total_scanned,
            "terrain_counts": self.terrain_counts,
            "scanned_positions": len(self.scanned_positions),
            "results_count": len(self.scan_results),
            "center_position": self.center_position,
            "scan_range": self.scan_range,
            "scan_pattern": self.scan_pattern
        }
    
    def reset(self) -> None:
        """Tarayıcıyı sıfırlar."""
        self.scanned_positions.clear()
        self.scan_results.clear()
        self.total_scanned = 0
        self.terrain_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.logger.info("MapScanner sıfırlandı")
