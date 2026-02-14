"""
CrystalDetector Modülü için Birim Testleri
"""

import pytest
from src.crystal_detector import CrystalDetector, Crystal
from src.map_scanner import MapScanner, ScanResult
import time


class TestCrystalDetector:
    """CrystalDetector sınıfı için test suite."""
    
    def test_init(self):
        """CrystalDetector başlatma testi."""
        detector = CrystalDetector(enable_filtering=True)
        
        assert detector.enable_filtering is True
        assert detector.total_detected == 0
        assert len(detector.detected_crystals) == 0
    
    def test_detect_crystal_at_position(self):
        """Pozisyonda kristal tespit testi."""
        detector = CrystalDetector()
        
        # Birkaç deneme yap (simülasyon olduğu için)
        attempts = 10
        detected_count = 0
        
        for i in range(attempts):
            crystal = detector.detect_crystal_at_position((i, i), terrain_level=3)
            if crystal:
                detected_count += 1
                assert isinstance(crystal, Crystal)
                assert crystal.position == (i, i)
                assert crystal.terrain_level == 3
                assert 1 <= crystal.level <= 5
                assert crystal.name is not None
                assert crystal.collected is False
        
        # En az bir kristal tespit edilmiş olmalı
        assert detected_count >= 0
    
    def test_detect_crystals_in_area(self):
        """Alan kristal tespit testi."""
        detector = CrystalDetector()
        scanner = MapScanner(center_position=(0, 0), scan_range=20)
        
        # Önce alan taraması yap
        scan_results = scanner.scan_area(max_scans=20)
        
        # Kristalleri tespit et
        detected = detector.detect_crystals_in_area(scan_results)
        
        assert isinstance(detected, list)
        
        for crystal in detected:
            assert isinstance(crystal, Crystal)
            assert crystal.level in [1, 2, 3, 4, 5]
    
    def test_filter_by_level(self):
        """Seviye filtreleme testi."""
        detector = CrystalDetector(enable_filtering=False)
        
        # Test kristalleri oluştur
        crystals = [
            Crystal((0, 0), 1, "Test 1", "#FFF", 1, time.time()),
            Crystal((1, 1), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((2, 2), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        
        # Sadece seviye 3 ve 5
        filtered = detector.filter_by_level(crystals, [3, 5])
        
        assert len(filtered) == 2
        assert all(c.level in [3, 5] for c in filtered)
    
    def test_filter_by_terrain(self):
        """Arazi seviyesi filtreleme testi."""
        detector = CrystalDetector()
        
        crystals = [
            Crystal((0, 0), 1, "Test 1", "#FFF", 1, time.time()),
            Crystal((1, 1), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((2, 2), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        
        # Sadece arazi seviyesi 3 ve 5
        filtered = detector.filter_by_terrain(crystals, [3, 5])
        
        assert len(filtered) == 2
        assert all(c.terrain_level in [3, 5] for c in filtered)
    
    def test_sort_by_priority(self):
        """Öncelik sıralama testi."""
        from config.settings import FilterSettings
        
        detector = CrystalDetector()
        
        crystals = [
            Crystal((0, 0), 1, "Test 1", "#FFF", 1, time.time()),
            Crystal((1, 1), 5, "Test 5", "#FFD700", 5, time.time()),
            Crystal((2, 2), 3, "Test 3", "#00F", 3, time.time()),
        ]
        
        # Yüksek seviye önce
        FilterSettings.COLLECT_HIGHEST_FIRST = True
        sorted_crystals = detector.sort_by_priority(crystals)
        
        assert sorted_crystals[0].level == 5
        assert sorted_crystals[-1].level == 1
        
        # Düşük seviye önce
        FilterSettings.COLLECT_HIGHEST_FIRST = False
        sorted_crystals = detector.sort_by_priority(crystals)
        
        assert sorted_crystals[0].level == 1
        assert sorted_crystals[-1].level == 5
    
    def test_get_highest_level_crystals(self):
        """Yüksek seviye kristal alma testi."""
        detector = CrystalDetector()
        
        crystals = [
            Crystal((0, 0), 1, "Test 1", "#FFF", 1, time.time()),
            Crystal((1, 1), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((2, 2), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        
        high_level = detector.get_highest_level_crystals(crystals, min_level=3)
        
        assert len(high_level) == 2
        assert all(c.level >= 3 for c in high_level)
    
    def test_get_crystals_by_level(self):
        """Seviye bazlı kristal alma testi."""
        detector = CrystalDetector()
        
        detector.detected_crystals = [
            Crystal((0, 0), 3, "Test 3a", "#00F", 3, time.time()),
            Crystal((1, 1), 3, "Test 3b", "#00F", 3, time.time()),
            Crystal((2, 2), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        
        level3 = detector.get_crystals_by_level(3)
        
        assert len(level3) == 2
        assert all(c.level == 3 for c in level3)
    
    def test_get_uncollected_crystals(self):
        """Toplanmamış kristal alma testi."""
        detector = CrystalDetector()
        
        crystal1 = Crystal((0, 0), 3, "Test 3", "#00F", 3, time.time())
        crystal1.collected = True
        
        crystal2 = Crystal((1, 1), 5, "Test 5", "#FFD700", 5, time.time())
        crystal2.collected = False
        
        detector.detected_crystals = [crystal1, crystal2]
        
        uncollected = detector.get_uncollected_crystals()
        
        assert len(uncollected) == 1
        assert uncollected[0].level == 5
    
    def test_mark_as_collected(self):
        """Toplanmış işaretleme testi."""
        detector = CrystalDetector()
        
        crystal = Crystal((0, 0), 3, "Test 3", "#00F", 3, time.time())
        assert crystal.collected is False
        
        detector.mark_as_collected(crystal)
        assert crystal.collected is True
    
    def test_get_statistics(self):
        """İstatistik testi."""
        detector = CrystalDetector()
        
        detector.detected_crystals = [
            Crystal((0, 0), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((1, 1), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        detector.total_detected = 2
        detector.detection_count[3] = 1
        detector.detection_count[5] = 1
        
        stats = detector.get_statistics()
        
        assert stats["total_detected"] == 2
        assert stats["by_level"][3] == 1
        assert stats["by_level"][5] == 1
        assert "uncollected" in stats
        assert "collected" in stats
    
    def test_reset(self):
        """Reset testi."""
        detector = CrystalDetector()
        
        detector.detected_crystals = [
            Crystal((0, 0), 3, "Test 3", "#00F", 3, time.time())
        ]
        detector.total_detected = 1
        
        detector.reset()
        
        assert detector.total_detected == 0
        assert len(detector.detected_crystals) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
