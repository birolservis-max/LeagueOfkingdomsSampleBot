"""
CrystalCollector Modülü için Birim Testleri
"""

import pytest
from src.crystal_collector import CrystalCollector
from src.crystal_detector import Crystal
import time


class TestCrystalCollector:
    """CrystalCollector sınıfı için test suite."""
    
    def test_init(self):
        """CrystalCollector başlatma testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        assert collector.auto_collect is True
        assert collector.dry_run is True
        assert collector.total_collected == 0
        assert collector.failed_collections == 0
    
    def test_collect_crystal_dry_run(self):
        """Test modunda kristal toplama testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystal = Crystal((10, 10), 3, "Test Crystal", "#00F", 3, time.time())
        
        result = collector.collect_crystal(crystal)
        
        assert result is True
        assert crystal.collected is True
        assert collector.total_collected == 1
    
    def test_collect_crystal_auto_collect_off(self):
        """Otomatik toplama kapalı testi."""
        collector = CrystalCollector(auto_collect=False, dry_run=False)
        
        crystal = Crystal((10, 10), 3, "Test Crystal", "#00F", 3, time.time())
        
        result = collector.collect_crystal(crystal)
        
        assert result is False
    
    def test_collect_multiple(self):
        """Birden fazla kristal toplama testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystals = [
            Crystal((0, 0), 1, "Test 1", "#FFF", 1, time.time()),
            Crystal((1, 1), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((2, 2), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        
        results = collector.collect_multiple(crystals)
        
        assert results["total"] == 3
        assert results["successful"] >= 0
        assert results["failed"] >= 0
        assert results["successful"] + results["failed"] == results["total"]
    
    def test_collect_multiple_with_max(self):
        """Maksimum limit ile toplama testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystals = [
            Crystal((0, 0), 1, "Test 1", "#FFF", 1, time.time()),
            Crystal((1, 1), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((2, 2), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        
        results = collector.collect_multiple(crystals, max_collect=2)
        
        assert results["total"] <= 2
    
    def test_collect_by_level(self):
        """Seviye bazlı toplama testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystals = [
            Crystal((0, 0), 1, "Test 1", "#FFF", 1, time.time()),
            Crystal((1, 1), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((2, 2), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        
        # Sadece seviye 3 ve 5 topla
        results = collector.collect_by_level(crystals, [3, 5])
        
        assert results["total"] == 2
    
    def test_collect_highest_priority(self):
        """Öncelikli toplama testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystals = [
            Crystal((0, 0), 1, "Test 1", "#FFF", 1, time.time()),
            Crystal((1, 1), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((2, 2), 5, "Test 5", "#FFD700", 5, time.time()),
            Crystal((3, 3), 4, "Test 4", "#F0F", 4, time.time()),
        ]
        
        results = collector.collect_highest_priority(crystals, count=2)
        
        assert results["total"] <= 2
    
    def test_get_collection_rate(self):
        """Toplama başarı oranı testi."""
        collector = CrystalCollector()
        
        collector.total_collected = 8
        collector.failed_collections = 2
        
        rate = collector.get_collection_rate()
        
        assert rate == 0.8  # 8/10
    
    def test_get_collection_rate_no_attempts(self):
        """Hiç toplama yapılmadığında oran testi."""
        collector = CrystalCollector()
        
        rate = collector.get_collection_rate()
        
        assert rate == 0.0
    
    def test_get_statistics(self):
        """İstatistik testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystals = [
            Crystal((0, 0), 3, "Test 3", "#00F", 3, time.time()),
            Crystal((1, 1), 5, "Test 5", "#FFD700", 5, time.time()),
        ]
        
        collector.collect_multiple(crystals)
        
        stats = collector.get_statistics()
        
        assert "total_collected" in stats
        assert "by_level" in stats
        assert "failed_collections" in stats
        assert "success_rate" in stats
        assert stats["auto_collect"] is True
        assert stats["dry_run"] is True
    
    def test_get_recent_collections(self):
        """Son toplamalar testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystals = [
            Crystal((i, i), 3, f"Test {i}", "#00F", 3, time.time())
            for i in range(5)
        ]
        
        collector.collect_multiple(crystals)
        
        recent = collector.get_recent_collections(count=3)
        
        assert len(recent) <= 3
    
    def test_reset_statistics(self):
        """İstatistik sıfırlama testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystal = Crystal((0, 0), 3, "Test", "#00F", 3, time.time())
        collector.collect_crystal(crystal)
        
        assert collector.total_collected > 0
        
        collector.reset_statistics()
        
        assert collector.total_collected == 0
        assert collector.failed_collections == 0
        assert len(collector.collection_history) == 0
    
    def test_enable_auto_collect(self):
        """Otomatik toplama aktif etme testi."""
        collector = CrystalCollector(auto_collect=False)
        
        assert collector.auto_collect is False
        
        collector.enable_auto_collect()
        
        assert collector.auto_collect is True
    
    def test_disable_auto_collect(self):
        """Otomatik toplama devre dışı bırakma testi."""
        collector = CrystalCollector(auto_collect=True)
        
        assert collector.auto_collect is True
        
        collector.disable_auto_collect()
        
        assert collector.auto_collect is False
    
    def test_collect_already_collected_crystal(self):
        """Zaten toplanmış kristal toplama testi."""
        collector = CrystalCollector(auto_collect=True, dry_run=True)
        
        crystal = Crystal((0, 0), 3, "Test", "#00F", 3, time.time())
        crystal.collected = True
        
        crystals = [crystal]
        
        results = collector.collect_multiple(crystals)
        
        # Zaten toplanmış, atlanmalı
        assert results["total"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
