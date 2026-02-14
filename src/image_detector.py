"""
Görüntü Tabanlı Kristal Tespit Modülü
Bu modül ekran görüntüsü analizi ile kristalleri tespit eder.
"""

import logging
from typing import List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image

from config.settings import CRYSTAL_LEVELS


class ImageDetector:
    """
    Görüntü tabanlı kristal tespit sınıfı.
    
    Ekran görüntüsünden kristalleri tespit eder ve konumlarını belirler.
    """
    
    def __init__(self):
        """ImageDetector başlatıcı."""
        self.logger = logging.getLogger("CrystalBot.ImageDetector")
        
        # Kristal renk aralıkları (HSV formatında)
        self.crystal_colors = self._init_crystal_colors()
        
        self.logger.info("ImageDetector başlatıldı")
    
    def _init_crystal_colors(self) -> dict:
        """
        Kristal renk aralıklarını HSV formatında başlatır.
        
        Returns:
            dict: Seviye bazlı HSV renk aralıkları
        """
        colors = {}
        
        # Seviye 1 - Beyaz kristaller
        colors[1] = {
            "lower": np.array([0, 0, 200]),  # Düşük doygunluk, yüksek parlaklık
            "upper": np.array([180, 30, 255]),
            "name": "Beyaz"
        }
        
        # Seviye 2 - Yeşil kristaller
        colors[2] = {
            "lower": np.array([40, 50, 50]),
            "upper": np.array([80, 255, 255]),
            "name": "Yeşil"
        }
        
        # Seviye 3 - Mavi kristaller
        colors[3] = {
            "lower": np.array([90, 50, 50]),
            "upper": np.array([130, 255, 255]),
            "name": "Mavi"
        }
        
        # Seviye 4 - Mor kristaller
        colors[4] = {
            "lower": np.array([130, 50, 50]),
            "upper": np.array([170, 255, 255]),
            "name": "Mor"
        }
        
        # Seviye 5 - Altın kristaller
        colors[5] = {
            "lower": np.array([15, 100, 100]),
            "upper": np.array([35, 255, 255]),
            "name": "Altın"
        }
        
        return colors
    
    def detect_crystals_in_image(
        self,
        image: Image.Image,
        target_levels: Optional[List[int]] = None,
        min_area: int = 50,
        max_area: int = 5000
    ) -> List[dict]:
        """
        Görüntüde kristalleri tespit eder.
        
        Args:
            image: PIL Image nesnesi
            target_levels: Aranacak kristal seviyeleri (None ise tümü)
            min_area: Minimum alan (pixel)
            max_area: Maksimum alan (pixel)
            
        Returns:
            List[dict]: Tespit edilen kristaller
        """
        if target_levels is None:
            target_levels = [1, 2, 3, 4, 5]
        
        # PIL Image'i OpenCV formatına dönüştür
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        detected_crystals = []
        
        for level in target_levels:
            if level not in self.crystal_colors:
                continue
            
            # Renk maskesi oluştur
            color_range = self.crystal_colors[level]
            mask = cv2.inRange(hsv_image, color_range["lower"], color_range["upper"])
            
            # Morfolojik işlemler ile gürültüyü azalt
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
            
            # Konturları bul
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Alan kontrolü
                if area < min_area or area > max_area:
                    continue
                
                # Merkez noktasını hesapla
                M = cv2.moments(contour)
                if M["m00"] == 0:
                    continue
                
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Kristal bilgilerini ekle
                crystal_info = {
                    "level": level,
                    "position": (cx, cy),
                    "area": area,
                    "contour": contour,
                    "color": color_range["name"],
                    "confidence": self._calculate_confidence(contour, area)
                }
                
                detected_crystals.append(crystal_info)
                
                self.logger.debug(
                    f"Kristal tespit edildi: Seviye {level} ({color_range['name']}), "
                    f"Konum: ({cx}, {cy}), Alan: {area}"
                )
        
        self.logger.info(f"{len(detected_crystals)} kristal tespit edildi")
        return detected_crystals
    
    def _calculate_confidence(self, contour, area: float) -> float:
        """
        Tespit güven skorunu hesaplar.
        
        Args:
            contour: OpenCV konturu
            area: Alan
            
        Returns:
            float: Güven skoru (0-1)
        """
        # Dairesellik kontrolü (kristaller genellikle yuvarlak)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            return 0.0
        
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # 0-1 arasına normalize et
        confidence = min(circularity, 1.0)
        
        return confidence
    
    def detect_crystal_by_template(
        self,
        image: Image.Image,
        template_path: str,
        threshold: float = 0.7
    ) -> List[Tuple[int, int]]:
        """
        Şablon eşleştirme ile kristal tespit eder.
        
        Args:
            image: PIL Image nesnesi
            template_path: Şablon görüntü yolu
            threshold: Eşleşme eşiği (0-1)
            
        Returns:
            List[Tuple[int, int]]: Tespit edilen konumlar
        """
        try:
            # Görüntüleri OpenCV formatına dönüştür
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            
            if template is None:
                self.logger.error(f"Şablon yüklenemedi: {template_path}")
                return []
            
            # Şablon eşleştirme
            result = cv2.matchTemplate(cv_image, template, cv2.TM_CCOEFF_NORMED)
            
            # Eşik değerinin üstündeki eşleşmeleri bul
            locations = np.where(result >= threshold)
            
            # Koordinatları listeye çevir
            matches = list(zip(*locations[::-1]))
            
            self.logger.info(f"Şablon eşleştirme: {len(matches)} konum bulundu")
            return matches
            
        except Exception as e:
            self.logger.error(f"Şablon eşleştirme hatası: {e}")
            return []
    
    def find_crystals_in_region(
        self,
        image: Image.Image,
        region: Tuple[int, int, int, int],
        target_levels: Optional[List[int]] = None
    ) -> List[dict]:
        """
        Belirli bir bölgede kristal arar.
        
        Args:
            image: PIL Image nesnesi
            region: Bölge (x, y, width, height)
            target_levels: Aranacak kristal seviyeleri
            
        Returns:
            List[dict]: Tespit edilen kristaller
        """
        # Bölgeyi kırp
        x, y, w, h = region
        cropped = image.crop((x, y, x + w, y + h))
        
        # Kristalleri tespit et
        crystals = self.detect_crystals_in_image(cropped, target_levels)
        
        # Koordinatları orijinal görüntüye göre düzelt
        for crystal in crystals:
            cx, cy = crystal["position"]
            crystal["position"] = (cx + x, cy + y)
        
        return crystals
    
    def detect_crystal_level_by_color(
        self,
        image: Image.Image,
        position: Tuple[int, int],
        sample_radius: int = 5
    ) -> Optional[int]:
        """
        Belirli bir konumdaki kristal seviyesini renk analizi ile tespit eder.
        
        Args:
            image: PIL Image nesnesi
            position: Kontrol edilecek konum
            sample_radius: Örnekleme yarıçapı
            
        Returns:
            Optional[int]: Kristal seviyesi veya None
        """
        try:
            x, y = position
            
            # Bölgeyi kırp
            left = max(0, x - sample_radius)
            top = max(0, y - sample_radius)
            right = min(image.width, x + sample_radius)
            bottom = min(image.height, y + sample_radius)
            
            sample = image.crop((left, top, right, bottom))
            
            # OpenCV formatına dönüştür
            cv_sample = cv2.cvtColor(np.array(sample), cv2.COLOR_RGB2HSV)
            
            # Her seviye için kontrol et
            best_match = None
            best_match_ratio = 0.0
            
            for level, color_range in self.crystal_colors.items():
                mask = cv2.inRange(cv_sample, color_range["lower"], color_range["upper"])
                match_ratio = np.count_nonzero(mask) / mask.size
                
                if match_ratio > best_match_ratio:
                    best_match_ratio = match_ratio
                    best_match = level
            
            # Minimum eşleşme oranı kontrolü
            if best_match_ratio > 0.1:
                self.logger.debug(
                    f"Seviye tespit edildi: {best_match} "
                    f"(Güven: {best_match_ratio:.2%})"
                )
                return best_match
            
            return None
            
        except Exception as e:
            self.logger.error(f"Seviye tespit hatası: {e}")
            return None
    
    def highlight_crystals(
        self,
        image: Image.Image,
        crystals: List[dict],
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Tespit edilen kristalleri görüntü üzerinde işaretler.
        
        Args:
            image: PIL Image nesnesi
            crystals: Kristal listesi
            output_path: Kaydedilecek dosya yolu (opsiyonel)
            
        Returns:
            Image.Image: İşaretlenmiş görüntü
        """
        # PIL Image'i OpenCV formatına dönüştür
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Her kristali işaretle
        for crystal in crystals:
            x, y = crystal["position"]
            level = crystal["level"]
            
            # Seviyeye göre renk seç
            color_map = {
                1: (255, 255, 255),  # Beyaz
                2: (0, 255, 0),      # Yeşil
                3: (255, 0, 0),      # Mavi (BGR)
                4: (255, 0, 255),    # Mor
                5: (0, 215, 255)     # Altın
            }
            
            color = color_map.get(level, (255, 255, 255))
            
            # Daire çiz
            cv2.circle(cv_image, (x, y), 10, color, 2)
            
            # Seviye yazısı ekle
            cv2.putText(
                cv_image,
                f"L{level}",
                (x - 15, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )
        
        # BGR'den RGB'ye dönüştür
        result_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        
        # Kaydedilecekse kaydet
        if output_path:
            result_image.save(output_path)
            self.logger.info(f"İşaretlenmiş görüntü kaydedildi: {output_path}")
        
        return result_image
    
    def get_statistics(self) -> dict:
        """
        Tespit istatistiklerini döndürür.
        
        Returns:
            dict: İstatistik bilgileri
        """
        return {
            "color_ranges": len(self.crystal_colors),
            "supported_levels": list(self.crystal_colors.keys())
        }
