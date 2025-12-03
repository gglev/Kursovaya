from typing import List, Tuple
import os
from image_processor import ImageProcessor
from lsb_algorithm import LSBAlgorithm
import hashlib

class Steganography:
    def __init__(self, bits_per_channel: int = 1):
        if not 1 <= bits_per_channel <= 4:
            raise ValueError("bits_per_channel должен быть между 1 и 4")
        self.image_processor = ImageProcessor()
        self.lsb_algorithm = LSBAlgorithm(bits_per_channel)
    
    def validate_image_format(self, image_path: str) -> bool:
        """Проверяет поддерживаемый формат изображения"""
        supported_formats = {'.png', '.bmp', '.jpg', '.jpeg', '.tiff'}
        return any(image_path.lower().endswith(fmt) for fmt in supported_formats)
    
    def calculate_hash(self, text: str) -> str:
        """Вычисляет хеш сообщения для проверки целостности"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]  # Берем первые 16 символов
    
    def embed_message(self, image_path: str, text: str, output_path: str, password: str = None) -> bool:
        try:
            # Валидация входных данных
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Файл не найден: {image_path}")
            
            if not self.validate_image_format(image_path):
                raise ValueError("Неподдерживаемый формат изображения. Используйте PNG или BMP")
            
            if not text.strip():
                raise ValueError("Сообщение не может быть пустым")
            
            # Добавляем хеш для проверки целостности
            text_with_hash = f"{self.calculate_hash(text)}:{text}"
            
            # Загружаем изображение
            self.image_processor.load_image(image_path)
            self.image_processor.convert_to_rgb()
            
            # Получаем пиксели
            pixels = self.image_processor.get_pixels()
            
            # Проверяем вместимость (в БАЙТАХ)
            max_bytes = self.calculate_capacity_bytes(pixels)
            text_bytes = text_with_hash.encode('utf-8')
            
            if len(text_bytes) > max_bytes:
                raise ValueError(f"Сообщение слишком длинное. Максимум: {max_bytes} байт ({max_bytes // 2} символов примерно)")
            
            # Встраиваем текст (как байты)
            new_pixels = self.lsb_algorithm.embed_text(pixels, text_with_hash, password)
            
            # Сохраняем результат
            self.image_processor.save_image(output_path, new_pixels, self.image_processor.size)
            return True
            
        except Exception as e:
            raise Exception(f"Ошибка встраивания сообщения: {str(e)}")
    
    def extract_message(self, image_path: str, password: str = None) -> str:
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Файл не найден: {image_path}")
            
            if not self.validate_image_format(image_path):
                raise ValueError("Неподдерживаемый формат изображения. Используйте PNG или BMP")
            
            # Загружаем изображение
            self.image_processor.load_image(image_path)
            self.image_processor.convert_to_rgb()
            
            # Получаем пиксели
            pixels = self.image_processor.get_pixels()
            
            # Извлекаем текст
            extracted_text = self.lsb_algorithm.extract_text(pixels, password)
            
            if not extracted_text:
                raise ValueError("Сообщение не найдено. Возможно, неверный пароль или изображение не содержит скрытых данных")
            
            # Проверяем целостность
            if ':' in extracted_text:
                hash_part, message = extracted_text.split(':', 1)
                calculated_hash = self.calculate_hash(message)
                
                if hash_part != calculated_hash:
                    raise ValueError("Целостность данных нарушена. Возможно, изображение было изменено")
                
                return message
            else:
                # Для обратной совместимости с сообщениями без хеша
                return extracted_text
            
        except Exception as e:
            raise Exception(f"Ошибка извлечения сообщения: {str(e)}")
    
    def calculate_capacity(self, pixels: List) -> int:
        """Рассчитывает вместимость в СИМВОЛАХ (для обратной совместимости)"""
        height = len(pixels)
        width = len(pixels[0])
        total_bits = height * width * 3 * self.lsb_algorithm.bits_per_channel
        total_bytes = total_bits // 8
        # Вычитаем место для маркера конца и небольшого запаса
        return (total_bytes - 4) // 2  # Примерно 2 байта на символ UTF-8
    
    def calculate_capacity_bytes(self, pixels: List) -> int:
        """Рассчитывает вместимость в БАЙТАХ (более точно)"""
        height = len(pixels)
        width = len(pixels[0])
        total_bits = height * width * 3 * self.lsb_algorithm.bits_per_channel
        total_bytes = total_bits // 8
        # Вычитаем место для маркера конца сообщения (2 байта)
        return total_bytes - 2
    
    def get_image_info(self, image_path: str) -> dict:
        """Получает информацию об изображении"""
        try:
            self.image_processor.load_image(image_path)
            self.image_processor.convert_to_rgb()
            pixels = self.image_processor.get_pixels()
            
            width, height = self.image_processor.size
            max_chars = self.calculate_capacity(pixels)
            max_bytes = self.calculate_capacity_bytes(pixels)
            
            return {
                'width': width,
                'height': height,
                'pixels': width * height,
                'max_chars': max_chars,
                'max_bytes': max_bytes,
                'bits_per_channel': self.lsb_algorithm.bits_per_channel,
                'format': os.path.splitext(image_path)[1].upper()
            }
        except Exception as e:
            raise Exception(f"Ошибка получения информации: {str(e)}")