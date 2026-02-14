"""
MapScanner Modülü için Birim Testleri
"""

import pytest
from src.map_scanner import MapScanner, ScanResult


class TestMapScanner:
    """MapScanner sınıfı için test suite."""
    
    def test_init(self):
        """MapScanner başlatma testi."""
        scanner = MapScanner(center_position=(10, 20), scan_range=30)
        
        assert scanner.center_position == (10, 20)
        assert scanner.scan_range == 30
        assert scanner.total_scanned == 0
        assert len(scanner.scanned_positions) == 0
    
    def test_detect_terrain_level(self):
        """Arazi seviyesi tespit testi."""
        scanner = MapScanner(center_position=(0, 0), scan_range=50)
        
        # Merkeze yakın pozisyon - düşük seviye beklenir
        level1 = scanner.detect_terrain_level((0, 0))
        assert 1 <= level1 <= 5
        
        # Merkeze uzak pozisyon - yüksek seviye beklenir
        level2 = scanner.detect_terrain_level((40, 40))
        assert 1 <= level2 <= 5
    
    def test_get_possible_crystals(self):
        """Olası kristal seviyeleri testi."""
        scanner = MapScanner()
        
        # Seviye 1 arazi
        crystals = scanner.get_possible_crystals(1)
        assert crystals == [1]
        
        # Seviye 3 arazi
        crystals = scanner.get_possible_crystals(3)
        assert crystals == [2, 3]
        
        # Seviye 5 arazi
        crystals = scanner.get_possible_crystals(5)
        assert crystals == [4, 5]
    
    def test_scan_position(self):
        """Tek pozisyon tarama testi."""
        scanner = MapScanner(center_position=(0, 0), scan_range=50)
        
        result = scanner.scan_position((5, 5))
        
        assert result is not None
        assert isinstance(result, ScanResult)
        assert result.position == (5, 5)
        assert 1 <= result.terrain_level <= 5
        assert len(result.possible_crystals) > 0
        assert result.scanned is True
        
        # Aynı pozisyon tekrar tarandığında None dönmeli
        result2 = scanner.scan_position((5, 5))
        assert result2 is None
    
    def test_scan_position_out_of_range(self):
        """Menzil dışı pozisyon tarama testi."""
        scanner = MapScanner(center_position=(0, 0), scan_range=10)
        
        # Menzil dışında
        result = scanner.scan_position((100, 100))
        assert result is None
    
    def test_scan_area(self):
        """Alan tarama testi."""
        scanner = MapScanner(center_position=(0, 0), scan_range=20)
        
        results = scanner.scan_area(max_scans=10)
        
        assert len(results) <= 10
        assert scanner.total_scanned >= len(results)
        
        for result in results:
            assert isinstance(result, ScanResult)
            assert result.scanned is True
    
    def test_find_high_level_terrains(self):
        """Yüksek seviye arazi bulma testi."""
        scanner = MapScanner(center_position=(0, 0), scan_range=50)
        
        # Önce alan taraması yap
        scanner.scan_area(max_scans=50)
        
        # Yüksek seviye arazileri bul
        high_level = scanner.find_high_level_terrains(min_level=3)
        
        assert isinstance(high_level, list)
        
        for result in high_level:
            assert result.terrain_level >= 3
    
    def test_get_statistics(self):
        """İstatistik testi."""
        scanner = MapScanner(center_position=(10, 10), scan_range=20)
        scanner.scan_area(max_scans=5)
        
        stats = scanner.get_statistics()
        
        assert "total_scanned" in stats
        assert "terrain_counts" in stats
        assert "scanned_positions" in stats
        assert stats["total_scanned"] >= 0
        assert stats["center_position"] == (10, 10)
        assert stats["scan_range"] == 20
    
    def test_reset(self):
        """Reset testi."""
        scanner = MapScanner()
        scanner.scan_area(max_scans=5)
        
        assert scanner.total_scanned > 0
        
        scanner.reset()
        
        assert scanner.total_scanned == 0
        assert len(scanner.scanned_positions) == 0
        assert len(scanner.scan_results) == 0
    
    def test_generate_scan_path_spiral(self):
        """Spiral tarama deseni testi."""
        scanner = MapScanner(center_position=(0, 0), scan_range=5, scan_pattern="spiral")
        
        path = scanner.generate_scan_path()
        
        assert len(path) > 0
        assert (0, 0) in path  # Merkez nokta dahil olmalı
    
    def test_generate_scan_path_grid(self):
        """Grid tarama deseni testi."""
        scanner = MapScanner(center_position=(0, 0), scan_range=5, scan_pattern="grid")
        
        path = scanner.generate_scan_path()
        
        assert len(path) > 0
    
    def test_generate_scan_path_random(self):
        """Random tarama deseni testi."""
        scanner = MapScanner(center_position=(0, 0), scan_range=5, scan_pattern="random")
        
        path = scanner.generate_scan_path()
        
        assert len(path) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
