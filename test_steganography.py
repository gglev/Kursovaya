import pytest
import tempfile
import os
from PIL import Image

# Добавляем путь к проекту для импорта модулей
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steganography import Steganography


class TestSteganographyBasic:
    """Базовые тесты системы стеганографии"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.stego = Steganography(bits_per_channel=1)
        
        # Создаем тестовое изображение
        self.test_image_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        self.create_test_image(self.test_image_path, size=(100, 100))
        
        # Тестовый текст
        self.test_message = "Секретное сообщение для теста"
    
    def teardown_method(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.test_image_path):
            os.unlink(self.test_image_path)
    
    def create_test_image(self, path, size=(100, 100)):
        """Создает тестовое изображение"""
        img = Image.new('RGB', size, color='blue')
        img.save(path, format='PNG')
        return path
    
    def test_1_basic_embed_and_extract(self):
        """Тест 1: Базовое встраивание и извлечение сообщения"""
        output_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        
        try:
            # Встраивание сообщения
            success = self.stego.embed_message(
                self.test_image_path, 
                self.test_message, 
                output_path
            )
            
            # Проверка успешности встраивания
            assert success == True, "Встраивание сообщения не удалось"
            assert os.path.exists(output_path), "Выходной файл не создан"
            
            # Проверка размера файла
            original_size = os.path.getsize(self.test_image_path)
            output_size = os.path.getsize(output_path)
            assert abs(original_size - output_size) < 1000, "Размер файла изменился слишком сильно"
            
            # Извлечение сообщения
            extracted_message = self.stego.extract_message(output_path)
            
            # Проверка корректности извлечения
            assert extracted_message == self.test_message, f"Извлеченное сообщение не совпадает. Ожидалось: '{self.test_message}', получено: '{extracted_message}'"
            assert len(extracted_message) == len(self.test_message), f"Длина сообщения не совпадает. Ожидалось: {len(self.test_message)}, получено: {len(extracted_message)}"
            
            print(f" Тест 1 пройден: успешно встроено и извлечено сообщение длиной {len(self.test_message)} символов")
            
        finally:
            # Очистка временных файлов
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_2_message_automatic_truncation(self):
        """Тест 2: Проверка автоматической обрезки длинного сообщения"""
        # Создаем очень большое сообщение
        huge_message = "X" * 5000  # 5000 символов
        
        output_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        
        try:
            # Рассчитываем максимальную вместимость
            self.stego.image_processor.load_image(self.test_image_path)
            pixels = self.stego.image_processor.get_pixels()
            max_chars = self.stego.calculate_capacity(pixels)
            
            # Встраивание сообщения (должно автоматически обрезаться)
            success = self.stego.embed_message(
                self.test_image_path, 
                huge_message, 
                output_path
            )
            
            # Проверка успешности встраивания
            assert success == True, "Встраивание сообщения не удалось"
            assert os.path.exists(output_path), "Выходной файл не создан"
            
            # Извлечение сообщения
            extracted_message = self.stego.extract_message(output_path)
            
            # Проверка что сообщение было обрезано
            assert len(extracted_message) == max_chars, f"Сообщение не было обрезано. Длина: {len(extracted_message)}, ожидалось: {max_chars}"
            
            # Проверка что первые N символов сохранены
            assert extracted_message == huge_message[:max_chars], "Сообщение было обрезано некорректно"
            
            print(f" Тест 2 пройден: сообщение автоматически обрезано с {len(huge_message)} до {len(extracted_message)} символов")
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_3_extract_from_clean_image(self):
        """Тест 3: Извлечение из изображения без сообщения"""
        # Создаем новое чистое изображение без встроенного сообщения
        clean_image_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        self.create_test_image(clean_image_path, size=(50, 50))
        
        try:
            # Извлекаем сообщение из чистого изображения
            result = self.stego.extract_message(clean_image_path)
            
            # Ожидаем пустую строку для чистого изображения
            assert result == "", f"Ожидалась пустая строка, получено: '{result}'"
            
            print(f" Тест 3 пройден: из чистого изображения извлечена пустая строка")
            
        finally:
            if os.path.exists(clean_image_path):
                os.unlink(clean_image_path)
    
    @pytest.mark.parametrize("bits_per_channel, test_message", [
        (1, "Сообщение с 1 битом"),
        (2, "Сообщение с 2 битами"),
        (3, "Сообщение с 3 битами"),
        (4, "Сообщение с 4 битами"),
    ])
    def test_4_different_bits_per_channel(self, bits_per_channel, test_message):
        """Тест 4: Параметризованный тест - работа с разным количеством бит на канал"""
        # Создаем экземпляр с указанным количеством бит на канал
        stego = Steganography(bits_per_channel=bits_per_channel)
        
        output_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        
        try:
            # Встраивание сообщения
            success = stego.embed_message(
                self.test_image_path, 
                test_message, 
                output_path
            )
            
            # Проверка успешности
            assert success == True, f"Встраивание с {bits_per_channel} битами не удалось"
            
            # Извлечение сообщения
            extracted_message = stego.extract_message(output_path)
            
            # Проверка корректности
            assert extracted_message == test_message, \
                f"Ошибка при {bits_per_channel} битах: ожидалось '{test_message}', получено '{extracted_message}'"
            
            print(f"✅ Тест 4 пройден для {bits_per_channel} бит(а) на канал")
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


if __name__ == "__main__":
    # Запуск тестов с детальным выводом
    print("=" * 60)
    print("Запуск тестов системы стеганографии (автоматическая обрезка)")
    print("=" * 60)
    
    # Создаем экземпляр тестового класса
    test_class = TestSteganographyBasic()
    
    try:
        # Запускаем каждый тест по очереди
        test_class.setup_method()
        
        print("\nТест 1: Базовое встраивание и извлечение")
        test_class.test_1_basic_embed_and_extract()
        
        print("\nТест 2: Автоматическая обрезка длинного сообщения")
        test_class.test_2_message_automatic_truncation()
        
        print("\nТест 3: Извлечение из чистого изображения")
        test_class.test_3_extract_from_clean_image()
        
        print("\nТест 4: Разное количество бит на канал")
        
        # Запускаем параметризованный тест для каждого набора параметров
        test_params = [
            (1, "Сообщение с 1 битом"),
            (2, "Сообщение с 2 битами"),
            (3, "Сообщение с 3 битами"),
            (4, "Сообщение с 4 битами"),
        ]
        
        for bits, message in test_params:
            test_class.test_4_different_bits_per_channel(bits, message)
        
        print("\n" + "=" * 60)
        print("✅ Все тесты успешно пройдены!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n Ошибка при выполнении тестов: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        test_class.teardown_method()