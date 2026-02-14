"""
Ekran Otomasyonu Modülü
Bu modül oyun ekranı ile etkileşim için gerekli fonksiyonları sağlar.
"""

import logging
import time
import random
from typing import Optional, Tuple, List
import pyautogui
import pygetwindow as gw
from PIL import Image
import mss

from config.settings import GameIntegrationSettings, SecuritySettings


class ScreenAutomation:
    """
    Ekran otomasyonu sınıfı.
    
    Oyun penceresini bulur, ekran görüntüsü alır ve fare/klavye etkileşimi sağlar.
    """
    
    def __init__(self):
        """ScreenAutomation başlatıcı."""
        self.logger = logging.getLogger("CrystalBot.ScreenAutomation")
        self.game_window = None
        self.sct = mss.mss()
        
        # PyAutoGUI güvenlik ayarları
        pyautogui.FAILSAFE = True  # Köşeye sürükleyerek durdur
        pyautogui.PAUSE = 0.1  # İşlemler arası varsayılan bekleme
        
        self.logger.info("ScreenAutomation başlatıldı")
    
    def find_game_window(self, window_title: str = "League of Kingdoms") -> bool:
        """
        Oyun penceresini bulur.
        
        Args:
            window_title: Pencere başlığı (varsayılan: "League of Kingdoms")
            
        Returns:
            bool: Pencere bulunduysa True
        """
        self.logger.info(f"Oyun penceresi aranıyor: '{window_title}'")
        
        try:
            # Tüm pencereleri listele
            windows = gw.getWindowsWithTitle(window_title)
            
            if not windows:
                self.logger.warning(f"'{window_title}' penceresi bulunamadı")
                # Benzer başlıkları ara
                all_windows = gw.getAllTitles()
                similar = [w for w in all_windows if "kingdom" in w.lower() or "league" in w.lower()]
                if similar:
                    self.logger.info(f"Benzer pencereler bulundu: {similar}")
                return False
            
            # İlk pencereyi kullan
            self.game_window = windows[0]
            self.logger.info(
                f"Oyun penceresi bulundu: {self.game_window.title} "
                f"(Konum: {self.game_window.left}, {self.game_window.top}, "
                f"Boyut: {self.game_window.width}x{self.game_window.height})"
            )
            
            # Pencereyi aktif hale getir
            if not self.game_window.isActive:
                self.game_window.activate()
                time.sleep(0.5)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Pencere bulma hatası: {e}")
            return False
    
    def get_game_region(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Oyun penceresinin ekran koordinatlarını döndürür.
        
        Returns:
            Optional[Tuple]: (x, y, width, height) veya None
        """
        if not self.game_window:
            self.logger.warning("Oyun penceresi bulunamadı")
            return None
        
        return (
            self.game_window.left,
            self.game_window.top,
            self.game_window.width,
            self.game_window.height
        )
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Image.Image]:
        """
        Ekran görüntüsü alır.
        
        Args:
            region: Bölge (x, y, width, height). None ise oyun penceresi kullanılır
            
        Returns:
            Optional[Image.Image]: PIL Image nesnesi veya None
        """
        try:
            if region is None:
                region = self.get_game_region()
            
            if region is None:
                self.logger.error("Ekran görüntüsü bölgesi belirlenemedi")
                return None
            
            # mss ile ekran görüntüsü al
            monitor = {
                "left": region[0],
                "top": region[1],
                "width": region[2],
                "height": region[3]
            }
            
            screenshot = self.sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            
            self.logger.debug(f"Ekran görüntüsü alındı: {region}")
            return img
            
        except Exception as e:
            self.logger.error(f"Ekran görüntüsü alma hatası: {e}")
            return None
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5, human_like: bool = True) -> None:
        """
        Fareyi belirtilen koordinata taşır.
        
        Args:
            x: X koordinatı
            y: Y koordinatı
            duration: Hareket süresi (saniye)
            human_like: İnsan benzeri hareket (eğri, değişken hızlı)
        """
        try:
            if human_like:
                # İnsan benzeri hareket için rastgelelik ekle
                duration = duration + random.uniform(-0.1, 0.2)
                duration = max(0.2, duration)  # Minimum süre
                
                # Rastgele bir ara nokta ekle (eğri hareket için)
                current_x, current_y = pyautogui.position()
                mid_x = (current_x + x) // 2 + random.randint(-20, 20)
                mid_y = (current_y + y) // 2 + random.randint(-20, 20)
                
                pyautogui.moveTo(mid_x, mid_y, duration=duration / 2)
                time.sleep(0.05)
                pyautogui.moveTo(x, y, duration=duration / 2)
            else:
                pyautogui.moveTo(x, y, duration=duration)
            
            self.logger.debug(f"Fare taşındı: ({x}, {y})")
            
        except Exception as e:
            self.logger.error(f"Fare taşıma hatası: {e}")
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = "left", clicks: int = 1, interval: float = 0.0) -> None:
        """
        Fare tıklaması yapar.
        
        Args:
            x: X koordinatı (None ise mevcut pozisyon)
            y: Y koordinatı (None ise mevcut pozisyon)
            button: Fare düğmesi ("left", "right", "middle")
            clicks: Tıklama sayısı
            interval: Tıklamalar arası bekleme
        """
        try:
            if x is not None and y is not None:
                self.move_mouse(x, y, duration=0.3, human_like=True)
                time.sleep(random.uniform(0.05, 0.15))
            
            pyautogui.click(button=button, clicks=clicks, interval=interval)
            self.logger.debug(f"Tıklama yapıldı: ({x}, {y}), Düğme: {button}")
            
            # Anti-detection için rastgele gecikme
            if SecuritySettings.RANDOM_DELAYS:
                time.sleep(random.uniform(
                    SecuritySettings.MIN_RANDOM_DELAY,
                    SecuritySettings.MAX_RANDOM_DELAY
                ))
            
        except Exception as e:
            self.logger.error(f"Tıklama hatası: {e}")
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             duration: float = 1.0, human_like: bool = True) -> None:
        """
        Sürükle ve bırak işlemi yapar.
        
        Args:
            start_x: Başlangıç X koordinatı
            start_y: Başlangıç Y koordinatı
            end_x: Bitiş X koordinatı
            end_y: Bitiş Y koordinatı
            duration: Sürükleme süresi
            human_like: İnsan benzeri hareket
        """
        try:
            self.move_mouse(start_x, start_y, duration=0.3, human_like=True)
            time.sleep(0.1)
            
            if human_like:
                duration = duration + random.uniform(-0.2, 0.3)
                duration = max(0.5, duration)
            
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, button='left')
            self.logger.debug(f"Sürükleme yapıldı: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
            
        except Exception as e:
            self.logger.error(f"Sürükleme hatası: {e}")
    
    def scroll(self, clicks: int = 1, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        Fare tekerleği ile kaydırma yapar.
        
        Args:
            clicks: Kaydırma miktarı (pozitif yukarı, negatif aşağı)
            x: X koordinatı (None ise mevcut pozisyon)
            y: Y koordinatı (None ise mevcut pozisyon)
        """
        try:
            if x is not None and y is not None:
                self.move_mouse(x, y, duration=0.2, human_like=True)
            
            pyautogui.scroll(clicks)
            self.logger.debug(f"Kaydırma yapıldı: {clicks}")
            
        except Exception as e:
            self.logger.error(f"Kaydırma hatası: {e}")
    
    def press_key(self, key: str, presses: int = 1, interval: float = 0.0) -> None:
        """
        Klavye tuşuna basar.
        
        Args:
            key: Tuş adı (örn: 'enter', 'space', 'esc')
            presses: Basma sayısı
            interval: Basmalar arası bekleme
        """
        try:
            pyautogui.press(key, presses=presses, interval=interval)
            self.logger.debug(f"Tuş basıldı: {key}")
            
        except Exception as e:
            self.logger.error(f"Tuş basma hatası: {e}")
    
    def type_text(self, text: str, interval: float = 0.1) -> None:
        """
        Metin yazar.
        
        Args:
            text: Yazılacak metin
            interval: Karakterler arası bekleme
        """
        try:
            pyautogui.write(text, interval=interval)
            self.logger.debug(f"Metin yazıldı: {text}")
            
        except Exception as e:
            self.logger.error(f"Metin yazma hatası: {e}")
    
    def get_pixel_color(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """
        Belirtilen koordinattaki pixel rengini döndürür.
        
        Args:
            x: X koordinatı
            y: Y koordinatı
            
        Returns:
            Optional[Tuple[int, int, int]]: RGB renk değeri veya None
        """
        try:
            screenshot = self.capture_screen()
            if screenshot is None:
                return None
            
            # Oyun penceresi koordinatlarına göre düzelt
            region = self.get_game_region()
            if region:
                rel_x = x - region[0]
                rel_y = y - region[1]
                pixel = screenshot.getpixel((rel_x, rel_y))
                return pixel[:3]  # RGB
            
            return None
            
        except Exception as e:
            self.logger.error(f"Pixel rengi alma hatası: {e}")
            return None
    
    def wait_for_color(self, x: int, y: int, color: Tuple[int, int, int], 
                       timeout: float = 5.0, tolerance: int = 10) -> bool:
        """
        Belirtilen koordinatta belirtilen rengin görünmesini bekler.
        
        Args:
            x: X koordinatı
            y: Y koordinatı
            color: Beklenen RGB renk
            timeout: Maksimum bekleme süresi
            tolerance: Renk toleransı (0-255)
            
        Returns:
            bool: Renk bulunursa True
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            pixel_color = self.get_pixel_color(x, y)
            
            if pixel_color:
                # Renk eşleşmesini kontrol et (tolerans ile)
                if all(abs(pixel_color[i] - color[i]) <= tolerance for i in range(3)):
                    self.logger.debug(f"Renk bulundu: {pixel_color} ~ {color}")
                    return True
            
            time.sleep(0.1)
        
        self.logger.warning(f"Renk bulunamadı: {color} (timeout)")
        return False
    
    def close(self) -> None:
        """Kaynakları temizler."""
        if self.sct:
            self.sct.close()
        self.logger.info("ScreenAutomation kapatıldı")
