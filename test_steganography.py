import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_processor import ImageProcessor
from PIL import Image

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        self.test_image = "test_image.png"
        
        # Создаем тестовое изображение
        img = Image.new('RGB', (10, 10), color='blue')
        img.save(self.test_image)
    
    def tearDown(self):
        if os.path.exists(self.test_image):
            os.remove(self.test_image)
    
    def test_load_image(self):
        success = self.processor.load_image(self.test_image)
        self.assertTrue(success)
        self.assertEqual(self.processor.size, (10, 10))
        self.assertEqual(self.processor.mode, 'RGB')
    
    def test_convert_to_rgb(self):
        self.processor.load_image(self.test_image)
        self.processor.convert_to_rgb()
        self.assertEqual(self.processor.mode, 'RGB')
    
    def test_get_pixels(self):
        self.processor.load_image(self.test_image)
        pixels = self.processor.get_pixels()
        self.assertEqual(len(pixels), 10)  # 10 строк
        self.assertEqual(len(pixels[0]), 10)  # 10 столбцов
    
    def test_save_image(self):
        self.processor.load_image(self.test_image)
        pixels = self.processor.get_pixels()
        output_path = "test_output.png"
        
        self.processor.save_image(output_path, pixels, self.processor.size)
        self.assertTrue(os.path.exists(output_path))
        
        # Очистка
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    unittest.main()