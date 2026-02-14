"""
Yardımcı Fonksiyonlar
Bu modül bot genelinde kullanılan yardımcı fonksiyonları içerir.
"""

import logging
import time
import random
import json
import os
from typing import Tuple, Dict, Any, Optional
from datetime import datetime
from pathlib import Path


def setup_logging(
    log_file: str = "logs/crystal_bot.log",
    level: int = logging.INFO,
    debug_mode: bool = False
) -> logging.Logger:
    """
    Logging sistemini yapılandırır.
    
    Args:
        log_file: Log dosyası yolu
        level: Log seviyesi
        debug_mode: Debug modu aktif mi
        
    Returns:
        logging.Logger: Yapılandırılmış logger
    """
    # Log dizinini oluştur
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Logger oluştur
    logger = logging.getLogger("CrystalBot")
    logger.setLevel(logging.DEBUG if debug_mode else level)
    
    # Formatı ayarla
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Dosya handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Konsol handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def calculate_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    İki koordinat arasındaki mesafeyi hesaplar.
    
    Args:
        pos1: İlk koordinat (x, y)
        pos2: İkinci koordinat (x, y)
        
    Returns:
        float: Mesafe
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def is_within_range(
    pos: Tuple[int, int],
    center: Tuple[int, int],
    max_range: int
) -> bool:
    """
    Bir koordinatın belirli bir menzil içinde olup olmadığını kontrol eder.
    
    Args:
        pos: Kontrol edilecek koordinat
        center: Merkez koordinat
        max_range: Maksimum menzil
        
    Returns:
        bool: Menzil içindeyse True
    """
    return calculate_distance(pos, center) <= max_range


def format_coordinates(x: int, y: int) -> str:
    """
    Koordinatları okunabilir formata çevirir.
    
    Args:
        x: X koordinatı
        y: Y koordinatı
        
    Returns:
        str: Formatlanmış koordinat
    """
    return f"({x}, {y})"


def get_timestamp() -> str:
    """
    Mevcut zaman damgasını döndürür.
    
    Returns:
        str: ISO formatında zaman damgası
    """
    return datetime.now().isoformat()


def get_readable_timestamp() -> str:
    """
    Okunabilir zaman damgası döndürür.
    
    Returns:
        str: Okunabilir zaman damgası
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def random_delay(min_delay: float, max_delay: float) -> None:
    """
    Rastgele bir süre bekler (anti-detection).
    
    Args:
        min_delay: Minimum bekleme süresi (saniye)
        max_delay: Maksimum bekleme süresi (saniye)
    """
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


def save_session(data: Dict[str, Any], filepath: str) -> bool:
    """
    Oturum verilerini kaydeder.
    
    Args:
        data: Kaydedilecek veri
        filepath: Dosya yolu
        
    Returns:
        bool: Başarılı ise True
    """
    try:
        # Dizini oluştur
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Veriyi kaydet
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logging.error(f"Oturum kaydetme hatası: {e}")
        return False


def load_session(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Oturum verilerini yükler.
    
    Args:
        filepath: Dosya yolu
        
    Returns:
        Optional[Dict[str, Any]]: Yüklenen veri veya None
    """
    try:
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Oturum yükleme hatası: {e}")
        return None


def validate_crystal_level(level: int) -> bool:
    """
    Kristal seviyesinin geçerli olup olmadığını kontrol eder.
    
    Args:
        level: Kristal seviyesi
        
    Returns:
        bool: Geçerli ise True
    """
    return 1 <= level <= 5


def validate_terrain_level(level: int) -> bool:
    """
    Arazi seviyesinin geçerli olup olmadığını kontrol eder.
    
    Args:
        level: Arazi seviyesi
        
    Returns:
        bool: Geçerli ise True
    """
    return 1 <= level <= 5


def get_crystal_name(level: int) -> str:
    """
    Kristal seviyesine göre isim döndürür.
    
    Args:
        level: Kristal seviyesi
        
    Returns:
        str: Kristal ismi
    """
    if not validate_crystal_level(level):
        return "Bilinmeyen Kristal"
    return f"Seviye {level} Kristal"


def generate_spiral_coordinates(
    center: Tuple[int, int],
    max_radius: int
) -> list[Tuple[int, int]]:
    """
    Merkez noktadan spiral şeklinde koordinatlar üretir.
    
    Args:
        center: Merkez koordinat
        max_radius: Maksimum yarıçap
        
    Returns:
        list[Tuple[int, int]]: Koordinat listesi
    """
    cx, cy = center
    coordinates = [(cx, cy)]
    
    x, y = 0, 0
    dx, dy = 0, -1
    
    for _ in range((max_radius * 2) ** 2):
        if (-max_radius <= x <= max_radius) and (-max_radius <= y <= max_radius):
            coordinates.append((cx + x, cy + y))
        
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
            dx, dy = -dy, dx
        
        x, y = x + dx, y + dy
    
    return coordinates


def generate_grid_coordinates(
    start: Tuple[int, int],
    width: int,
    height: int
) -> list[Tuple[int, int]]:
    """
    Grid şeklinde koordinatlar üretir.
    
    Args:
        start: Başlangıç koordinatı
        width: Grid genişliği
        height: Grid yüksekliği
        
    Returns:
        list[Tuple[int, int]]: Koordinat listesi
    """
    sx, sy = start
    coordinates = []
    
    for y in range(sy, sy + height):
        for x in range(sx, sx + width):
            coordinates.append((x, y))
    
    return coordinates


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Bir değeri belirli bir aralıkta sınırlar.
    
    Args:
        value: Değer
        min_value: Minimum değer
        max_value: Maksimum değer
        
    Returns:
        float: Sınırlanmış değer
    """
    return max(min_value, min(value, max_value))


def create_directory(path: str) -> bool:
    """
    Dizin oluşturur (yoksa).
    
    Args:
        path: Dizin yolu
        
    Returns:
        bool: Başarılı ise True
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Dizin oluşturma hatası: {e}")
        return False
