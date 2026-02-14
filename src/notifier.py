"""
Bildirim Modülü
Bu modül kristal tespit ve toplama olaylarını bildirir.
"""

import logging
from typing import Optional, Dict, Any
import json
from datetime import datetime

from config.settings import NotificationSettings
from src.utils import format_coordinates, get_readable_timestamp


class Notifier:
    """
    Bildirim Sınıfı
    
    Kristal tespit ve toplama olaylarını konsol, dosya ve
    opsiyonel olarak Discord/Telegram üzerinden bildirir.
    """
    
    def __init__(
        self,
        console_enabled: bool = NotificationSettings.CONSOLE_ENABLED,
        file_logging: bool = NotificationSettings.FILE_LOGGING,
        log_file_path: str = NotificationSettings.LOG_FILE_PATH
    ):
        """
        Notifier başlatıcı.
        
        Args:
            console_enabled: Konsol bildirimi aktif mi
            file_logging: Dosya loglaması aktif mi
            log_file_path: Log dosyası yolu
        """
        self.logger = logging.getLogger("CrystalBot.Notifier")
        self.console_enabled = console_enabled
        self.file_logging = file_logging
        self.log_file_path = log_file_path
        
        # Bildirim sayaçları
        self.notification_count = 0
        self.notifications_by_type = {
            "crystal_detected": 0,
            "crystal_collected": 0,
            "error": 0,
            "info": 0
        }
        
        self.logger.info(
            f"Notifier başlatıldı - Konsol: {console_enabled}, "
            f"Dosya: {file_logging}"
        )
    
    def notify_crystal_detected(self, crystal) -> None:
        """
        Kristal tespit edildiğinde bildirim gönderir.
        
        Args:
            crystal: Tespit edilen kristal (Crystal objesi)
        """
        message = self._format_crystal_detection_message(crystal)
        
        self._send_notification(
            message=message,
            notification_type="crystal_detected",
            data={
                "crystal_level": crystal.level,
                "position": crystal.position,
                "terrain_level": crystal.terrain_level
            }
        )
    
    def notify_crystal_collected(self, crystal) -> None:
        """
        Kristal toplandığında bildirim gönderir.
        
        Args:
            crystal: Toplanan kristal (Crystal objesi)
        """
        message = self._format_crystal_collection_message(crystal)
        
        self._send_notification(
            message=message,
            notification_type="crystal_collected",
            data={
                "crystal_level": crystal.level,
                "position": crystal.position,
                "terrain_level": crystal.terrain_level
            }
        )
    
    def notify_multiple_detected(self, crystals: list) -> None:
        """
        Birden fazla kristal tespit edildiğinde bildirim gönderir.
        
        Args:
            crystals: Tespit edilen kristaller
        """
        if not crystals:
            return
        
        # Seviyeye göre grupla
        by_level = {}
        for crystal in crystals:
            level = crystal.level
            by_level[level] = by_level.get(level, 0) + 1
        
        message = f"🔍 {len(crystals)} Kristal Tespit Edildi!\n"
        message += "Seviye Dağılımı:\n"
        
        for level in sorted(by_level.keys(), reverse=True):
            count = by_level[level]
            message += f"  • Seviye {level}: {count} adet\n"
        
        if NotificationSettings.INCLUDE_TIMESTAMP:
            message += f"\nZaman: {get_readable_timestamp()}"
        
        self._send_notification(
            message=message,
            notification_type="crystal_detected",
            data={"count": len(crystals), "by_level": by_level}
        )
    
    def notify_collection_summary(self, stats: Dict) -> None:
        """
        Toplama özeti bildirir.
        
        Args:
            stats: Toplama istatistikleri
        """
        successful = stats.get("successful", 0)
        failed = stats.get("failed", 0)
        total = stats.get("total", 0)
        
        message = f"📊 Toplama Özeti\n"
        message += f"Başarılı: {successful}\n"
        message += f"Başarısız: {failed}\n"
        message += f"Toplam: {total}\n"
        
        if total > 0:
            success_rate = (successful / total) * 100
            message += f"Başarı Oranı: {success_rate:.1f}%"
        
        self._send_notification(
            message=message,
            notification_type="info",
            data=stats
        )
    
    def notify_error(self, error_message: str, exception: Optional[Exception] = None) -> None:
        """
        Hata bildirimi gönderir.
        
        Args:
            error_message: Hata mesajı
            exception: İstisna objesi (opsiyonel)
        """
        message = f"❌ HATA: {error_message}"
        
        if exception:
            message += f"\nDetay: {str(exception)}"
        
        self._send_notification(
            message=message,
            notification_type="error",
            data={"error": error_message, "exception": str(exception) if exception else None}
        )
    
    def notify_info(self, info_message: str) -> None:
        """
        Bilgi mesajı gönderir.
        
        Args:
            info_message: Bilgi mesajı
        """
        message = f"ℹ️ {info_message}"
        
        self._send_notification(
            message=message,
            notification_type="info",
            data={"message": info_message}
        )
    
    def _format_crystal_detection_message(self, crystal) -> str:
        """
        Kristal tespit mesajını formatlar.
        
        Args:
            crystal: Kristal objesi
            
        Returns:
            str: Formatlanmış mesaj
        """
        message = f"💎 {crystal.name} Tespit Edildi!\n"
        
        if NotificationSettings.INCLUDE_LEVEL:
            message += f"Seviye: {crystal.level}\n"
        
        if NotificationSettings.INCLUDE_COORDINATES:
            message += f"Konum: {format_coordinates(*crystal.position)}\n"
            message += f"Arazi Seviyesi: {crystal.terrain_level}\n"
        
        if NotificationSettings.INCLUDE_TIMESTAMP:
            message += f"Zaman: {get_readable_timestamp()}"
        
        return message
    
    def _format_crystal_collection_message(self, crystal) -> str:
        """
        Kristal toplama mesajını formatlar.
        
        Args:
            crystal: Kristal objesi
            
        Returns:
            str: Formatlanmış mesaj
        """
        message = f"✅ {crystal.name} Toplandı!\n"
        
        if NotificationSettings.INCLUDE_LEVEL:
            message += f"Seviye: {crystal.level}\n"
        
        if NotificationSettings.INCLUDE_COORDINATES:
            message += f"Konum: {format_coordinates(*crystal.position)}\n"
        
        if NotificationSettings.INCLUDE_TIMESTAMP:
            message += f"Zaman: {get_readable_timestamp()}"
        
        return message
    
    def _send_notification(
        self,
        message: str,
        notification_type: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Bildirim gönderir.
        
        Args:
            message: Bildirim mesajı
            notification_type: Bildirim tipi
            data: Ek veri
        """
        self.notification_count += 1
        self.notifications_by_type[notification_type] += 1
        
        # Konsol bildirimi
        if self.console_enabled:
            self._send_console_notification(message)
        
        # Dosya loglaması
        if self.file_logging:
            self._send_file_notification(message, notification_type, data)
        
        # Discord bildirimi
        if NotificationSettings.DISCORD_ENABLED and NotificationSettings.DISCORD_WEBHOOK_URL:
            self._send_discord_notification(message, data)
        
        # Telegram bildirimi
        if NotificationSettings.TELEGRAM_ENABLED and NotificationSettings.TELEGRAM_BOT_TOKEN:
            self._send_telegram_notification(message, data)
    
    def _send_console_notification(self, message: str) -> None:
        """
        Konsola bildirim gönderir.
        
        Args:
            message: Mesaj
        """
        print("\n" + "=" * 50)
        print(message)
        print("=" * 50 + "\n")
    
    def _send_file_notification(
        self,
        message: str,
        notification_type: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Dosyaya bildirim kaydeder.
        
        Args:
            message: Mesaj
            notification_type: Bildirim tipi
            data: Ek veri
        """
        try:
            # Log dizinini oluştur
            import os
            log_dir = os.path.dirname(self.log_file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            # Log dosyasına yaz
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                timestamp = get_readable_timestamp()
                f.write(f"\n[{timestamp}] [{notification_type.upper()}]\n")
                f.write(message + "\n")
                
                if data:
                    f.write(f"Data: {json.dumps(data, ensure_ascii=False)}\n")
                
                f.write("-" * 50 + "\n")
                
        except Exception as e:
            self.logger.error(f"Dosya bildirimi hatası: {e}")
    
    def _send_discord_notification(
        self,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Discord'a webhook ile bildirim gönderir.
        
        Args:
            message: Mesaj
            data: Ek veri
        """
        try:
            import requests
            
            webhook_url = NotificationSettings.DISCORD_WEBHOOK_URL
            
            payload = {
                "content": message,
                "username": "League of Kingdoms Bot"
            }
            
            if data:
                payload["embeds"] = [{
                    "title": "Detaylı Bilgi",
                    "description": json.dumps(data, ensure_ascii=False, indent=2),
                    "color": 3447003  # Mavi
                }]
            
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code == 204:
                self.logger.debug("Discord bildirimi gönderildi")
            else:
                self.logger.warning(f"Discord bildirimi başarısız: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Discord bildirimi hatası: {e}")
    
    def _send_telegram_notification(
        self,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Telegram'a bot ile bildirim gönderir.
        
        Args:
            message: Mesaj
            data: Ek veri
        """
        try:
            import requests
            
            bot_token = NotificationSettings.TELEGRAM_BOT_TOKEN
            chat_id = NotificationSettings.TELEGRAM_CHAT_ID
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                self.logger.debug("Telegram bildirimi gönderildi")
            else:
                self.logger.warning(f"Telegram bildirimi başarısız: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Telegram bildirimi hatası: {e}")
    
    def get_statistics(self) -> Dict:
        """
        Bildirim istatistiklerini döndürür.
        
        Returns:
            Dict: İstatistik bilgileri
        """
        return {
            "total_notifications": self.notification_count,
            "by_type": self.notifications_by_type.copy(),
            "console_enabled": self.console_enabled,
            "file_logging": self.file_logging,
            "discord_enabled": NotificationSettings.DISCORD_ENABLED,
            "telegram_enabled": NotificationSettings.TELEGRAM_ENABLED
        }
