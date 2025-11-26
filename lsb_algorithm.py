from typing import List

class LSBAlgorithm:
    def __init__(self, bits_per_channel: int = 1):
        self.bits_per_channel = bits_per_channel
    
    @staticmethod
    def text_to_binary(text: str) -> str:
        # Кодируем текст в UTF-8, затем преобразуем в биты
        encoded_text = text.encode('utf-8')
        binary = ''.join(format(byte, '08b') for byte in encoded_text)
        return binary + '00000000'  # Добавляем маркер конца сообщения
    
    @staticmethod
    def binary_to_text(binary: str) -> str:
        # Собираем байты из бинарной строки
        bytes_list = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if byte == '00000000':  # Маркер конца сообщения
                break
            if len(byte) == 8:  # Проверяем, что байт полный
                bytes_list.append(int(byte, 2))
        
        # Декодируем из UTF-8
        try:
            return bytes(bytes_list).decode('utf-8')
        except UnicodeDecodeError:
            # Если не удается декодировать, возвращаем пустую строку
            return ""
    
    def embed_text(self, pixels: List, text: str) -> List:
        binary_text = self.text_to_binary(text)
        binary_index = 0
        
        height = len(pixels)
        width = len(pixels[0])
        
        new_pixels = []
        for i in range(height):
            new_row = []
            for j in range(width):
                if binary_index < len(binary_text):
                    r, g, b = pixels[i][j]
                    # Модифицируем младшие биты каждого канала
                    r = self._set_bits(r, binary_text, binary_index)
                    binary_index += self.bits_per_channel
                    g = self._set_bits(g, binary_text, binary_index)
                    binary_index += self.bits_per_channel
                    b = self._set_bits(b, binary_text, binary_index)
                    binary_index += self.bits_per_channel
                    new_row.append((r, g, b))
                else:
                    new_row.append(pixels[i][j])
            new_pixels.append(new_row)
        
        return new_pixels
    
    def _set_bits(self, value: int, binary_text: str, index: int) -> int:
        if index >= len(binary_text):
            return value
        
        # Очищаем младшие биты
        value = value & ~((1 << self.bits_per_channel) - 1)
        # Устанавливаем новые биты
        bits = int(binary_text[index:index+self.bits_per_channel], 2)
        return value | bits
    
    def extract_text(self, pixels: List) -> str:
        binary_text = ''
        height = len(pixels)
        width = len(pixels[0])
        
        for i in range(height):
            for j in range(width):
                r, g, b = pixels[i][j]
                # Извлекаем младшие биты каждого канала
                binary_text += self._get_bits(r)
                binary_text += self._get_bits(g)
                binary_text += self._get_bits(b)
        
        return self.binary_to_text(binary_text)
    
    def _get_bits(self, value: int) -> str:
        bits = value & ((1 << self.bits_per_channel) - 1)
        return format(bits, f'0{self.bits_per_channel}b')