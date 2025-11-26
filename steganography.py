from typing import List, Tuple
import os
from image_processor import ImageProcessor
from lsb_algorithm import LSBAlgorithm

class Steganography:
    def __init__(self, bits_per_channel: int = 1):
        if not 1 <= bits_per_channel <= 4:
            raise ValueError("bits_per_channel должен быть между 1 и 4")
        self.image_processor = ImageProcessor()
        self.lsb_algorithm = LSBAlgorithm(bits_per_channel)
    
    def validate_image_format(self, image_path: str) -> bool:
        """Проверяет поддерживаемый формат изображения"""
        supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}
        return any(image_path.lower().endswith(fmt) for fmt in supported_formats)
    
    def embed_message(self, image_path: str, text: str, output_path: str) -> bool:
        try:
            # Валидация входных данных
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Файл не найден: {image_path}")
            
            if not self.validate_image_format(image_path):
                raise ValueError("Неподдерживаемый формат изображения")
            
            if not text.strip():
                raise ValueError("Сообщение не может быть пустым")
            
            # Загружаем изображение
            self.image_processor.load_image(image_path)
            self.image_processor.convert_to_rgb()
            
            # Получаем пиксели
            pixels = self.image_processor.get_pixels()
            
            # Проверяем вместимость
            max_chars = self.calculate_capacity(pixels)
            if len(text) > max_chars:
                raise ValueError(f"Сообщение слишком длинное. Максимум: {max_chars} символов")
            
            # Встраиваем текст
            new_pixels = self.lsb_algorithm.embed_text(pixels, text)
            
            # Сохраняем результат
            self.image_processor.save_image(output_path, new_pixels, self.image_processor.size)
            return True
            
        except Exception as e:
            raise Exception(f"Ошибка встраивания сообщения: {str(e)}")
    
    def extract_message(self, image_path: str) -> str:
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Файл не найден: {image_path}")
            
            if not self.validate_image_format(image_path):
                raise ValueError("Неподдерживаемый формат изображения")
            
            # Загружаем изображение
            self.image_processor.load_image(image_path)
            self.image_processor.convert_to_rgb()
            
            # Получаем пиксели
            pixels = self.image_processor.get_pixels()
            
            # Извлекаем текст
            text = self.lsb_algorithm.extract_text(pixels)
            
            if not text:
                raise ValueError("Сообщение не найдено или повреждено")
                
            return text
            
        except Exception as e:
            raise Exception(f"Ошибка извлечения сообщения: {str(e)}")
    
    def calculate_capacity(self, pixels: List) -> int:
        height = len(pixels)
        width = len(pixels[0])
        total_bits = height * width * 3 * self.lsb_algorithm.bits_per_channel
        return total_bits // 8 - 1  # Учитываем маркер конца сообщения
    
    def get_image_info(self, image_path: str) -> dict:
        """Возвращает информацию об изображении"""
        self.image_processor.load_image(image_path)
        pixels = self.image_processor.get_pixels()
        
        return {
            'size': self.image_processor.size,
            'mode': self.image_processor.mode,
            'capacity': self.calculate_capacity(pixels),
            'bits_per_channel': self.lsb_algorithm.bits_per_channel
        }