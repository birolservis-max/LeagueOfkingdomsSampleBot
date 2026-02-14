"""
Ekran Otomasyonu Modül Testleri
"""

import unittest
from unittest.mock import Mock, patch, MagicMock


class TestScreenAutomation(unittest.TestCase):
    """ScreenAutomation modülü testleri."""
    
    @patch('src.screen_automation.mss')
    @patch('src.screen_automation.gw')
    @patch('src.screen_automation.pyautogui')
    def test_initialization(self, mock_pyautogui, mock_gw, mock_mss):
        """ScreenAutomation başlatma testi."""
        from src.screen_automation import ScreenAutomation
        
        screen = ScreenAutomation()
        
        self.assertIsNotNone(screen)
        self.assertEqual(screen.game_window, None)
    
    @patch('src.screen_automation.gw')
    def test_find_game_window_success(self, mock_gw):
        """Oyun penceresini bulma testi - başarılı."""
        from src.screen_automation import ScreenAutomation
        
        # Mock pencere
        mock_window = Mock()
        mock_window.title = "League of Kingdoms"
        mock_window.left = 0
        mock_window.top = 0
        mock_window.width = 1920
        mock_window.height = 1080
        mock_window.isActive = True
        
        mock_gw.getWindowsWithTitle.return_value = [mock_window]
        
        screen = ScreenAutomation()
        result = screen.find_game_window("League of Kingdoms")
        
        self.assertTrue(result)
        self.assertEqual(screen.game_window, mock_window)
    
    @patch('src.screen_automation.gw')
    def test_find_game_window_failure(self, mock_gw):
        """Oyun penceresini bulma testi - başarısız."""
        from src.screen_automation import ScreenAutomation
        
        mock_gw.getWindowsWithTitle.return_value = []
        mock_gw.getAllTitles.return_value = []
        
        screen = ScreenAutomation()
        result = screen.find_game_window("League of Kingdoms")
        
        self.assertFalse(result)
        self.assertIsNone(screen.game_window)


class TestImageDetector(unittest.TestCase):
    """ImageDetector modülü testleri."""
    
    def test_initialization(self):
        """ImageDetector başlatma testi."""
        from src.image_detector import ImageDetector
        
        detector = ImageDetector()
        
        self.assertIsNotNone(detector)
        self.assertEqual(len(detector.crystal_colors), 5)
    
    def test_crystal_colors_initialized(self):
        """Kristal renk aralıkları başlatma testi."""
        from src.image_detector import ImageDetector
        
        detector = ImageDetector()
        
        # Her seviye için renk aralığı olmalı
        for level in [1, 2, 3, 4, 5]:
            self.assertIn(level, detector.crystal_colors)
            self.assertIn('lower', detector.crystal_colors[level])
            self.assertIn('upper', detector.crystal_colors[level])
            self.assertIn('name', detector.crystal_colors[level])


class TestGameNavigator(unittest.TestCase):
    """GameNavigator modülü testleri."""
    
    @patch('src.game_navigator.ScreenAutomation')
    def test_initialization(self, mock_screen):
        """GameNavigator başlatma testi."""
        from src.game_navigator import GameNavigator
        
        navigator = GameNavigator(mock_screen)
        
        self.assertIsNotNone(navigator)
        self.assertEqual(navigator.current_position, (0, 0))
        self.assertIsNone(navigator.map_center)
    
    @patch('src.game_navigator.ScreenAutomation')
    def test_calibrate_map(self, mock_screen):
        """Harita kalibrasyon testi."""
        from src.game_navigator import GameNavigator
        
        # Mock screen region
        mock_screen.get_game_region.return_value = (0, 0, 1920, 1080)
        
        navigator = GameNavigator(mock_screen)
        result = navigator.calibrate_map()
        
        self.assertTrue(result)
        self.assertIsNotNone(navigator.map_center)
        self.assertIsNotNone(navigator.map_bounds)


class TestModuleIntegration(unittest.TestCase):
    """Modül entegrasyon testleri."""
    
    def test_modules_can_be_imported(self):
        """Tüm modüllerin import edilebilirliği testi."""
        try:
            from src.screen_automation import ScreenAutomation
            from src.image_detector import ImageDetector
            from src.game_navigator import GameNavigator
            
            # Import başarılı
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Modül import hatası: {e}")
    
    def test_crystal_collector_accepts_screen_automation(self):
        """CrystalCollector'ın screen automation parametrelerini kabul etmesi testi."""
        from src.crystal_collector import CrystalCollector
        
        mock_screen = Mock()
        mock_navigator = Mock()
        
        collector = CrystalCollector(
            auto_collect=True,
            dry_run=True,
            screen_automation=mock_screen,
            game_navigator=mock_navigator
        )
        
        self.assertEqual(collector.screen, mock_screen)
        self.assertEqual(collector.navigator, mock_navigator)


if __name__ == '__main__':
    unittest.main()
