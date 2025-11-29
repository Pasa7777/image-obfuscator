from PIL import Image
import random
import argparse
import hashlib

def shuffle_image_pixels(image_path, key, output_path, reverse=False):
    # Загружаем изображение
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # Создаем список всех координат пикселей
    coords = [(x, y) for x in range(width) for y in range(height)]

    # Инициализируем генератор случайных чисел с ключом
    random.seed(key)
    
    # Перемешиваем координаты
    shuffled_coords = coords.copy()
    random.shuffle(shuffled_coords)

    # Создаем новое изображение для результата
    new_img = Image.new(img.mode, (width, height))
    new_pixels = new_img.load()

    if reverse:
        # Восстанавливаем изображение
        for orig_pos, new_pos in zip(coords, shuffled_coords):
            new_pixels[orig_pos] = pixels[new_pos]
    else:
        # Перемешиваем изображение
        for orig_pos, new_pos in zip(coords, shuffled_coords):
            new_pixels[new_pos] = pixels[orig_pos]

    # Сохраняем результат
    new_img.save(output_path)
    print(f"Изображение сохранено как {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Перемешивание пикселей изображения')
    parser.add_argument('input', help='Входное изображение')
    parser.add_argument('output', help='Выходное изображение')
    parser.add_argument('key', help='Ключ для перемешивания', type=str)
    parser.add_argument('--reverse', action='store_true', help='Восстановить исходное изображение')
    
    args = parser.parse_args()
    hash = hashlib.new('sha512')
    hash.update((args.key).encode())
    shuffle_image_pixels(args.input, int(hash.hexdigest(), 16), args.output, args.reverse)