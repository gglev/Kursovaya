from typing import List, Optional
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

class LSBAlgorithm:
    def __init__(self, bits_per_channel: int = 1):
        self.bits_per_channel = bits_per_channel
    
    @staticmethod
    def encrypt_message(text: str, password: str) -> bytes:
        """Шифрование сообщения с использованием AES-256 (CBC режим)"""
        try:
            # Генерируем соль для ключа
            salt = get_random_bytes(16)
            
            # Создаем ключ из пароля с использованием PBKDF2
            key = PBKDF2(password.encode('utf-8'), salt, dkLen=32, count=1000000)
            
            # Создаем шифр
            cipher = AES.new(key, AES.MODE_CBC)
            iv = cipher.iv
            
            # Шифруем сообщение
            ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))

            return salt + iv + ct_bytes
        except Exception as e:
            raise ValueError(f"Ошибка шифрования: {str(e)}")
    
    @staticmethod
    def decrypt_message(encrypted_data: bytes, password: str) -> str:
        """Расшифрование сообщения"""
        try:
            # Проверяем минимальный размер
            if len(encrypted_data) < 48:  # Соль(16) + IV(16) + хотя бы 16 байт шифртекста
                raise ValueError("Недостаточный размер данных для расшифровки")
            
            # Разбираем данные
            salt = encrypted_data[:16]
            iv = encrypted_data[16:32]
            ct = encrypted_data[32:]
            
            # Восстанавливаем ключ
            key = PBKDF2(password.encode('utf-8'), salt, dkLen=32, count=1000000)
            
            # Создаем шифр для расшифровки
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            
            # Расшифровываем
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Неверный пароль или поврежденные данные: {str(e)}")
    
    @staticmethod
    def bytes_to_binary(data: bytes) -> str:
        """Преобразование байтов в бинарную строку"""
        binary_string = ''
        for byte in data:
            binary_string += format(byte, '08b')
        
        # Добавляем маркер конца сообщения (0x00 0x00)
        binary_string += '00000000' * 2
        return binary_string
    
    @staticmethod
    def binary_to_bytes(binary: str) -> Optional[bytes]:
        """Преобразование бинарной строки обратно в байты"""
        bytes_list = []
        
        # Проходим по 8 бит за раз
        for i in range(0, len(binary), 8):
            if i + 8 > len(binary):
                break
                
            byte_str = binary[i:i+8]
            
            # Проверяем маркер конца (два нулевых байта подряд)
            if byte_str == '00000000':
                # Проверяем следующий байт, если он есть
                if i + 16 <= len(binary):
                    next_byte_str = binary[i+8:i+16]
                    if next_byte_str == '00000000':
                        break  # Нашли маркер конца
            
            bytes_list.append(int(byte_str, 2))
        
        try:
            return bytes(bytes_list)
        except Exception:
            return None
    
    @staticmethod
    def text_to_binary(text: str) -> str:
        """Преобразование текста в бинарную строку (для обратной совместимости)"""
        encoded_text = text.encode('utf-8')
        binary = ''.join(format(byte, '08b') for byte in encoded_text)
        return binary + '00000000'  # Маркер конца сообщения
    
    @staticmethod
    def binary_to_text(binary: str) -> str:
        """Преобразование бинарной строки в текст (для обратной совместимости)"""
        bytes_list = []
        for i in range(0, len(binary), 8):
            if i + 8 > len(binary):
                break
            byte_str = binary[i:i+8]
            if byte_str == '00000000':
                break
            bytes_list.append(int(byte_str, 2))
        
        try:
            return bytes(bytes_list).decode('utf-8')
        except UnicodeDecodeError:
            return ""
    
    def embed_text(self, pixels: List, text: str, password: str = None) -> List:
        """Встраивание текста в пиксели"""
        # Преобразуем текст в байты
        if password:
            # Шифруем сообщение и получаем байты
            encrypted_bytes = self.encrypt_message(text, password)
            binary_data = self.bytes_to_binary(encrypted_bytes)
        else:
            # Просто текст (без шифрования)
            binary_data = self.text_to_binary(text)
        
        binary_index = 0
        height = len(pixels)
        width = len(pixels[0])
        
        new_pixels = []
        for i in range(height):
            new_row = []
            for j in range(width):
                r, g, b = pixels[i][j]
                
                # Встраиваем в красный канал
                if binary_index < len(binary_data):
                    r = self._set_bits(r, binary_data, binary_index)
                    binary_index += self.bits_per_channel
                
                # Встраиваем в зеленый канал
                if binary_index < len(binary_data):
                    g = self._set_bits(g, binary_data, binary_index)
                    binary_index += self.bits_per_channel
                
                # Встраиваем в синий канал
                if binary_index < len(binary_data):
                    b = self._set_bits(b, binary_data, binary_index)
                    binary_index += self.bits_per_channel
                
                new_row.append((r, g, b))
            new_pixels.append(new_row)
        
        return new_pixels
    
    def extract_text(self, pixels: List, password: str = None) -> str:
        """Извлечение текста из пикселей"""
        # Сначала извлекаем все биты
        binary_text = ''
        height = len(pixels)
        width = len(pixels[0])
        
        for i in range(height):
            for j in range(width):
                r, g, b = pixels[i][j]
                binary_text += self._get_bits(r)
                binary_text += self._get_bits(g)
                binary_text += self._get_bits(b)
        
        # Пытаемся сначала как зашифрованные данные
        if password:
            try:
                encrypted_bytes = self.binary_to_bytes(binary_text)
                if encrypted_bytes and len(encrypted_bytes) >= 48:
                    decrypted_text = self.decrypt_message(encrypted_bytes, password)
                    return decrypted_text
            except ValueError:
                # Не удалось расшифровать - возможно, не зашифровано
                pass
        
        # Пытаемся как обычный текст
        text = self.binary_to_text(binary_text)
        return text
    
    def embed_data(self, pixels: List, data: bytes, password: str = None) -> List:
        """Встраивание байтов в пиксели (альтернативный метод)"""
        if password:
            # Шифруем данные (предполагаем, что data это текст в байтах)
            data = self.encrypt_message(data.decode('utf-8'), password)
        
        binary_data = self.bytes_to_binary(data)
        return self._embed_binary(pixels, binary_data)
    
    def extract_data(self, pixels: List, password: str = None) -> Optional[bytes]:
        """Извлечение байтов из пикселей"""
        binary_text = ''
        height = len(pixels)
        width = len(pixels[0])
        
        for i in range(height):
            for j in range(width):
                r, g, b = pixels[i][j]
                binary_text += self._get_bits(r)
                binary_text += self._get_bits(g)
                binary_text += self._get_bits(b)
        
        data_bytes = self.binary_to_bytes(binary_text)
        
        if password and data_bytes:
            try:
                if len(data_bytes) >= 48:
                    decrypted_text = self.decrypt_message(data_bytes, password)
                    return decrypted_text.encode('utf-8')
            except ValueError:
                pass
        
        return data_bytes
    
    def _embed_binary(self, pixels: List, binary_data: str) -> List:
        """Вспомогательный метод для встраивания бинарных данных"""
        binary_index = 0
        height = len(pixels)
        width = len(pixels[0])
        
        new_pixels = []
        for i in range(height):
            new_row = []
            for j in range(width):
                r, g, b = pixels[i][j]
                
                if binary_index < len(binary_data):
                    r = self._set_bits(r, binary_data, binary_index)
                    binary_index += self.bits_per_channel
                
                if binary_index < len(binary_data):
                    g = self._set_bits(g, binary_data, binary_index)
                    binary_index += self.bits_per_channel
                
                if binary_index < len(binary_data):
                    b = self._set_bits(b, binary_data, binary_index)
                    binary_index += self.bits_per_channel
                
                new_row.append((r, g, b))
            new_pixels.append(new_row)
        
        return new_pixels
    
    def _set_bits(self, value: int, binary_text: str, index: int) -> int:
        """Установка битов в значение канала"""
        if index >= len(binary_text):
            return value
        
        # Очищаем младшие биты
        mask = (1 << self.bits_per_channel) - 1
        value = value & ~mask
        
        # Получаем биты для вставки
        bits_str = binary_text[index:index+self.bits_per_channel]
        if len(bits_str) < self.bits_per_channel:
            bits_str = bits_str.ljust(self.bits_per_channel, '0')
        
        bits = int(bits_str, 2)
        return value | bits
    
    def _get_bits(self, value: int) -> str:
        """Извлечение битов из значения канала"""
        mask = (1 << self.bits_per_channel) - 1
        bits = value & mask
        return format(bits, f'0{self.bits_per_channel}b')
    
    def calculate_max_bytes(self, width: int, height: int) -> int:
        """Рассчитывает максимальное количество байт для встраивания"""
        total_bits = width * height * 3 * self.bits_per_channel
        total_bytes = total_bits // 8
        # Вычитаем 2 байта для маркера конца
        return max(0, total_bytes - 2)
    
    def calculate_max_chars(self, width: int, height: int) -> int:
        """Рассчитывает максимальное количество символов для встраивания"""
        max_bytes = self.calculate_max_bytes(width, height)
        # Ориентировочно 2 байта на символ UTF-8
        return max_bytes // 2