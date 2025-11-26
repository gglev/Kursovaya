from PIL import Image
from typing import List, Tuple

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.mode = None
        self.size = None
    
    def load_image(self, image_path: str) -> bool:
        try:
            self.image = Image.open(image_path)
            self.mode = self.image.mode
            self.size = self.image.size
            return True
        except Exception as e:
            raise Exception(f"Ошибка загрузки изображения: {str(e)}")
    
    def convert_to_rgb(self) -> None:
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')
            self.mode = 'RGB'
    
    def get_pixels(self) -> List[List[Tuple[int, int, int]]]:
        if self.image is None:
            raise Exception("Изображение не загружено")
        
        pixels = list(self.image.getdata())
        width, height = self.image.size
        return [pixels[i * width:(i + 1) * width] for i in range(height)]
    
    def save_image(self, image_path: str, pixels: List, size: Tuple[int, int]) -> None:
        try:
            flat_pixels = [pixel for row in pixels for pixel in row]
            new_image = Image.new('RGB', size)
            new_image.putdata(flat_pixels)
            new_image.save(image_path, format='PNG')
        except Exception as e:
            raise Exception(f"Ошибка сохранения изображения: {str(e)}")