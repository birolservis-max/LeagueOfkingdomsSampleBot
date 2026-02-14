"""
Oyun Navigasyon Modülü
Bu modül oyun içinde gezinme ve harita üzerinde hareket için gerekli fonksiyonları sağlar.
"""

import logging
import time
import random
from typing import Tuple, List, Optional
import math

from src.screen_automation import ScreenAutomation
from config.settings import SecuritySettings


class GameNavigator:
    """
    Oyun navigasyon sınıfı.
    
    Oyun haritasında gezinme, kristallere gitme ve harita kaydırma işlemlerini yönetir.
    """
    
    def __init__(self, screen_automation: ScreenAutomation):
        """
        GameNavigator başlatıcı.
        
        Args:
            screen_automation: ScreenAutomation nesnesi
        """
        self.logger = logging.getLogger("CrystalBot.GameNavigator")
        self.screen = screen_automation
        
        # Navigasyon durumu
        self.current_position = (0, 0)
        self.map_center = None
        self.zoom_level = 1.0
        
        # Harita sınırları (piksel cinsinden, oyun penceresine göre)
        self.map_bounds = None
        
        self.logger.info("GameNavigator başlatıldı")
    
    def calibrate_map(self) -> bool:
        """
        Harita ayarlarını kalibre eder (merkez, sınırlar).
        
        Returns:
            bool: Başarılı ise True
        """
        self.logger.info("Harita kalibrasyonu yapılıyor...")
        
        try:
            region = self.screen.get_game_region()
            if not region:
                self.logger.error("Oyun penceresi bulunamadı")
                return False
            
            x, y, w, h = region
            
            # Harita merkezini belirle (genellikle oyun penceresinin ortası)
            self.map_center = (x + w // 2, y + h // 2)
            
            # Harita sınırlarını belirle (oyun penceresinin %80'i güvenli alan)
            margin_x = int(w * 0.1)
            margin_y = int(h * 0.1)
            
            self.map_bounds = {
                "left": x + margin_x,
                "right": x + w - margin_x,
                "top": y + margin_y,
                "bottom": y + h - margin_y
            }
            
            self.logger.info(
                f"Harita kalibrasyonu tamamlandı - "
                f"Merkez: {self.map_center}, "
                f"Sınırlar: {self.map_bounds}"
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Kalibrasyon hatası: {e}")
            return False
    
    def move_to_position(
        self,
        target_x: int,
        target_y: int,
        smooth: bool = True
    ) -> bool:
        """
        Harita üzerinde belirtilen pozisyona gider.
        
        Args:
            target_x: Hedef X koordinatı (ekran koordinatı)
            target_y: Hedef Y koordinatı (ekran koordinatı)
            smooth: Yumuşak hareket (insan benzeri)
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            if not self.map_center:
                self.logger.warning("Harita kalibre edilmemiş, kalibrasyon yapılıyor...")
                if not self.calibrate_map():
                    return False
            
            self.logger.info(f"Pozisyona hareket ediliyor: ({target_x}, {target_y})")
            
            # Harita merkezinden hedefe olan mesafeyi hesapla
            center_x, center_y = self.map_center
            delta_x = target_x - center_x
            delta_y = target_y - center_y
            
            # Eğer hedef zaten merkezde ise hareket etme
            if abs(delta_x) < 20 and abs(delta_y) < 20:
                self.logger.debug("Hedef zaten merkeze yakın")
                return True
            
            # Haritayı kaydırarak hedefe git
            if smooth:
                # İnsan benzeri hareket: küçük adımlarla
                steps = max(5, int(math.sqrt(delta_x**2 + delta_y**2) / 50))
                
                for i in range(1, steps + 1):
                    step_x = center_x + int(delta_x * i / steps)
                    step_y = center_y + int(delta_y * i / steps)
                    
                    # Haritayı kaydır
                    self._pan_map(-delta_x / steps, -delta_y / steps)
                    time.sleep(random.uniform(0.1, 0.3))
            else:
                # Doğrudan git
                self._pan_map(-delta_x, -delta_y)
            
            self.current_position = (target_x, target_y)
            self.logger.info(f"Pozisyona ulaşıldı: ({target_x}, {target_y})")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Pozisyon hareketi hatası: {e}")
            return False
    
    def _pan_map(self, delta_x: float, delta_y: float) -> None:
        """
        Haritayı kaydırır (sürükle-bırak).
        
        Args:
            delta_x: X ekseninde kaydırma miktarı
            delta_y: Y ekseninde kaydırma miktarı
        """
        if not self.map_center:
            return
        
        center_x, center_y = self.map_center
        
        # Başlangıç ve bitiş noktalarını hesapla
        start_x = center_x
        start_y = center_y
        end_x = int(center_x + delta_x)
        end_y = int(center_y + delta_y)
        
        # Haritayı sürükle
        duration = random.uniform(0.5, 1.0)
        self.screen.drag(start_x, start_y, end_x, end_y, duration=duration, human_like=True)
        
        # Haritanın stabilize olmasını bekle
        time.sleep(0.3)
    
    def navigate_to_crystal(
        self,
        crystal_position: Tuple[int, int],
        click_to_collect: bool = False
    ) -> bool:
        """
        Kristal pozisyonuna gider ve isteğe bağlı olarak tıklar.
        
        Args:
            crystal_position: Kristal pozisyonu (ekran koordinatı)
            click_to_collect: Kristale tıklayarak topla
            
        Returns:
            bool: Başarılı ise True
        """
        self.logger.info(f"Kristale gidiliyor: {crystal_position}")
        
        # Kristal pozisyonuna git
        if not self.move_to_position(crystal_position[0], crystal_position[1], smooth=True):
            return False
        
        # Kristalın merkeze gelmesini bekle
        time.sleep(0.5)
        
        # Tıklayarak topla
        if click_to_collect:
            if not self.map_center:
                return False
            
            # Harita merkezine tıkla (kristal artık orada olmalı)
            self.screen.click(
                self.map_center[0],
                self.map_center[1],
                button="left"
            )
            
            self.logger.info("Kristale tıklandı")
            
            # Toplama animasyonunu bekle
            time.sleep(random.uniform(1.0, 2.0))
        
        return True
    
    def scan_area_spiral(
        self,
        center: Tuple[int, int],
        radius: int,
        step: int = 50
    ) -> List[Tuple[int, int]]:
        """
        Belirli bir alan etrafında spiral şekilde tarama yapar.
        
        Args:
            center: Merkez koordinat
            radius: Tarama yarıçapı (piksel)
            step: Adım büyüklüğü (piksel)
            
        Returns:
            List[Tuple[int, int]]: Tarama pozisyonları
        """
        positions = []
        x, y = center
        
        # Spiral koordinatları hesapla
        angle = 0
        current_radius = 0
        
        while current_radius <= radius:
            pos_x = int(x + current_radius * math.cos(angle))
            pos_y = int(y + current_radius * math.sin(angle))
            
            positions.append((pos_x, pos_y))
            
            # Spiral genişlet
            angle += 0.5
            current_radius = angle * step / (2 * math.pi)
        
        self.logger.debug(f"Spiral tarama: {len(positions)} pozisyon oluşturuldu")
        return positions
    
    def scan_area_grid(
        self,
        top_left: Tuple[int, int],
        bottom_right: Tuple[int, int],
        step: int = 50
    ) -> List[Tuple[int, int]]:
        """
        Grid şeklinde alan tarar.
        
        Args:
            top_left: Sol üst köşe
            bottom_right: Sağ alt köşe
            step: Adım büyüklüğü (piksel)
            
        Returns:
            List[Tuple[int, int]]: Tarama pozisyonları
        """
        positions = []
        
        x1, y1 = top_left
        x2, y2 = bottom_right
        
        y = y1
        direction = 1  # 1: sağa, -1: sola (yılan deseni)
        
        while y <= y2:
            if direction == 1:
                x_range = range(x1, x2 + 1, step)
            else:
                x_range = range(x2, x1 - 1, -step)
            
            for x in x_range:
                positions.append((x, y))
            
            y += step
            direction *= -1  # Yön değiştir
        
        self.logger.debug(f"Grid tarama: {len(positions)} pozisyon oluşturuldu")
        return positions
    
    def zoom_in(self, clicks: int = 1) -> None:
        """
        Haritayı yakınlaştırır.
        
        Args:
            clicks: Yakınlaştırma sayısı
        """
        if not self.map_center:
            return
        
        self.screen.scroll(clicks, self.map_center[0], self.map_center[1])
        self.zoom_level *= (1.1 ** clicks)
        
        self.logger.debug(f"Yakınlaştırıldı: Zoom seviyesi {self.zoom_level:.2f}")
        time.sleep(0.3)
    
    def zoom_out(self, clicks: int = 1) -> None:
        """
        Haritayı uzaklaştırır.
        
        Args:
            clicks: Uzaklaştırma sayısı
        """
        if not self.map_center:
            return
        
        self.screen.scroll(-clicks, self.map_center[0], self.map_center[1])
        self.zoom_level *= (0.9 ** clicks)
        
        self.logger.debug(f"Uzaklaştırıldı: Zoom seviyesi {self.zoom_level:.2f}")
        time.sleep(0.3)
    
    def reset_zoom(self) -> None:
        """Zoom seviyesini sıfırlar."""
        # Zoom seviyesine göre geri al
        if self.zoom_level > 1.0:
            clicks = int(math.log(self.zoom_level) / math.log(1.1))
            self.zoom_out(clicks)
        elif self.zoom_level < 1.0:
            clicks = int(math.log(1.0 / self.zoom_level) / math.log(1.1))
            self.zoom_in(clicks)
        
        self.zoom_level = 1.0
        self.logger.info("Zoom sıfırlandı")
    
    def center_map(self) -> bool:
        """
        Haritayı başlangıç pozisyonuna ortalar.
        
        Returns:
            bool: Başarılı ise True
        """
        if not self.map_center:
            return False
        
        # Merkeze tıkla ve haritayı sıfırla
        self.screen.click(self.map_center[0], self.map_center[1])
        time.sleep(0.5)
        
        self.current_position = self.map_center
        self.logger.info("Harita merkezlendi")
        
        return True
    
    def is_position_visible(self, position: Tuple[int, int]) -> bool:
        """
        Pozisyonun ekranda görünür olup olmadığını kontrol eder.
        
        Args:
            position: Kontrol edilecek pozisyon
            
        Returns:
            bool: Görünür ise True
        """
        if not self.map_bounds:
            return False
        
        x, y = position
        
        return (
            self.map_bounds["left"] <= x <= self.map_bounds["right"] and
            self.map_bounds["top"] <= y <= self.map_bounds["bottom"]
        )
    
    def get_statistics(self) -> dict:
        """
        Navigasyon istatistiklerini döndürür.
        
        Returns:
            dict: İstatistik bilgileri
        """
        return {
            "current_position": self.current_position,
            "map_center": self.map_center,
            "zoom_level": self.zoom_level,
            "map_bounds": self.map_bounds
        }
