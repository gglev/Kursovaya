from image_processor import ImageProcessor
from lsb_algorithm import LSBAlgorithm
from typing import List

class Steganography:
    def __init__(self, bits_per_channel: int = 1):
        self.image_processor = ImageProcessor()
        self.lsb_algorithm = LSBAlgorithm(bits_per_channel)
    
    def embed_message(self, image_path: str, text: str, output_path: str) -> bool:
        try:
            # Загружаем изображение
            self.image_processor.load_image(image_path)
            self.image_processor.convert_to_rgb()
            
            # Получаем пиксели
            pixels = self.image_processor.get_pixels()
            
            # Проверяем вместимость
            max_chars = self.calculate_capacity(pixels)
            if len(text) > max_chars:
                raise Exception(f"Сообщение слишком длинное. Максимум: {max_chars} символов")
            
            # Встраиваем текст
            new_pixels = self.lsb_algorithm.embed_text(pixels, text)
            
            # Сохраняем результат
            self.image_processor.save_image(output_path, new_pixels, self.image_processor.size)
            return True
            
        except Exception as e:
            raise Exception(f"Ошибка встраивания сообщения: {str(e)}")
    
    def extract_message(self, image_path: str) -> str:
        try:
            # Загружаем изображение
            self.image_processor.load_image(image_path)
            self.image_processor.convert_to_rgb()
            
            # Получаем пиксели
            pixels = self.image_processor.get_pixels()
            
            # Извлекаем текст
            text = self.lsb_algorithm.extract_text(pixels)
            return text
            
        except Exception as e:
            raise Exception(f"Ошибка извлечения сообщения: {str(e)}")
    
    def calculate_capacity(self, pixels: List) -> int:
        height = len(pixels)
        width = len(pixels[0])
        total_bits = height * width * 3 * self.lsb_algorithm.bits_per_channel
        return total_bits // 8 - 1  # Учитываем маркер конца сообщения