"""
League of Kingdoms Crystal Bot - Ana Giriş Noktası
"""

import argparse
import sys
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import (
    BotSettings,
    ScanSettings,
    FilterSettings,
    CollectorSettings
)
from src.bot import CrystalBot


def parse_arguments():
    """Komut satırı argümanlarını parse eder."""
    parser = argparse.ArgumentParser(
        description="League of Kingdoms Crystal Bot - Kristal Tespit ve Toplama Botu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek Kullanım:
  python src/main.py                          # Varsayılan ayarlarla başlat
  python src/main.py --center 100 200         # Belirli bir merkez noktadan başlat
  python src/main.py --range 30               # 30 birimlik menzilde tara
  python src/main.py --levels 4 5             # Sadece seviye 4 ve 5 kristalleri topla
  python src/main.py --dry-run                # Test modunda çalıştır
  python src/main.py --debug                  # Debug modu ile çalıştır
        """
    )
    
    parser.add_argument(
        "--center",
        nargs=2,
        type=int,
        default=[0, 0],
        metavar=("X", "Y"),
        help="Tarama merkez koordinatı (varsayılan: 0 0)"
    )
    
    parser.add_argument(
        "--range",
        type=int,
        default=ScanSettings.MAX_SCAN_RANGE,
        help=f"Tarama menzili (varsayılan: {ScanSettings.MAX_SCAN_RANGE})"
    )
    
    parser.add_argument(
        "--pattern",
        choices=["spiral", "grid", "random"],
        default=ScanSettings.SCAN_PATTERN,
        help=f"Tarama deseni (varsayılan: {ScanSettings.SCAN_PATTERN})"
    )
    
    parser.add_argument(
        "--levels",
        nargs="+",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=FilterSettings.TARGET_LEVELS,
        help=f"Toplanacak kristal seviyeleri (varsayılan: {FilterSettings.TARGET_LEVELS})"
    )
    
    parser.add_argument(
        "--no-auto-collect",
        action="store_true",
        help="Otomatik toplamayı devre dışı bırak (sadece tespit et)"
    )
    
    parser.add_argument(
        "--max-collect",
        type=int,
        default=CollectorSettings.MAX_COLLECT_PER_CYCLE,
        help=f"Döngü başına maksimum toplama sayısı (varsayılan: {CollectorSettings.MAX_COLLECT_PER_CYCLE})"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test modu (gerçekten toplama yapmaz)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Debug modu (detaylı loglama)"
    )
    
    parser.add_argument(
        "--max-time",
        type=int,
        default=BotSettings.MAX_RUN_TIME,
        help=f"Maksimum çalışma süresi (saniye, 0 = sınırsız) (varsayılan: {BotSettings.MAX_RUN_TIME})"
    )
    
    return parser.parse_args()


def apply_arguments(args):
    """Komut satırı argümanlarını ayarlara uygular."""
    # Filtreleme ayarları
    if args.levels:
        FilterSettings.TARGET_LEVELS = args.levels
    
    # Toplama ayarları
    if args.no_auto_collect:
        CollectorSettings.AUTO_COLLECT = False
    
    if args.max_collect:
        CollectorSettings.MAX_COLLECT_PER_CYCLE = args.max_collect
    
    # Bot ayarları
    if args.dry_run:
        BotSettings.DRY_RUN = True
    
    if args.debug:
        BotSettings.DEBUG_MODE = True
    
    if args.max_time:
        BotSettings.MAX_RUN_TIME = args.max_time
    
    # Tarama ayarları
    if args.pattern:
        ScanSettings.SCAN_PATTERN = args.pattern


def print_banner():
    """Bot banner'ını yazdırır."""
    banner = f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        League of Kingdoms - Crystal Bot v{BotSettings.VERSION}         ║
║                                                           ║
║  Kristal Tespit ve Toplama Botu                          ║
║  Otomatik harita tarama ve kristal toplama sistemi       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_configuration(args):
    """Yapılandırmayı yazdırır."""
    print("\n" + "=" * 60)
    print("YAPILANDIRMA")
    print("=" * 60)
    print(f"Merkez Pozisyon:      ({args.center[0]}, {args.center[1]})")
    print(f"Tarama Menzili:       {args.range}")
    print(f"Tarama Deseni:        {args.pattern}")
    print(f"Hedef Seviyeler:      {FilterSettings.TARGET_LEVELS}")
    print(f"Otomatik Toplama:     {'Açık' if CollectorSettings.AUTO_COLLECT else 'Kapalı'}")
    print(f"Döngü Başı Toplama:   {CollectorSettings.MAX_COLLECT_PER_CYCLE}")
    print(f"Test Modu:            {'Açık' if BotSettings.DRY_RUN else 'Kapalı'}")
    print(f"Debug Modu:           {'Açık' if BotSettings.DEBUG_MODE else 'Kapalı'}")
    print(f"Maksimum Süre:        {BotSettings.MAX_RUN_TIME}s (0 = sınırsız)")
    print("=" * 60 + "\n")


def main():
    """Ana fonksiyon."""
    # Banner'ı göster
    print_banner()
    
    # Argümanları parse et
    args = parse_arguments()
    
    # Argümanları ayarlara uygula
    apply_arguments(args)
    
    # Yapılandırmayı göster
    print_configuration(args)
    
    # Onay al
    try:
        response = input("Bot'u başlatmak istiyor musunuz? (E/H): ").strip().lower()
        if response not in ['e', 'evet', 'y', 'yes']:
            print("Bot başlatılmadı.")
            return
    except KeyboardInterrupt:
        print("\nİptal edildi.")
        return
    
    print("\nBot başlatılıyor...\n")
    
    # Bot'u oluştur ve başlat
    try:
        bot = CrystalBot(
            center_position=tuple(args.center),
            scan_range=args.range,
            debug_mode=args.debug
        )
        
        # Bot'u başlat
        bot.start()
        
    except KeyboardInterrupt:
        print("\n\nBot kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n\nBEKLENMEYEN HATA: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
