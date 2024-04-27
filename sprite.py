import pygame


# КЛАСС ПОЗВОЛЯЮЩИЙ ЗАГРУЖАТЬ ЛИСТЫ СПРАЙТОВ, И ИЗВЛЕКАТЬ ОТДЕЛЬНЫЕ СПРАЙТЫ ИЗ ЭТОГО ЛИСТА
class SpriteSheet(object):
    # ЗАГРУЖАЕМ ИЗОБРАЖЕНИЕ
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
        except pygame.error as message:
            print(message)

    # МЕТОД ДЛЯ ПОЛУЧЕНИЯ ОТДЕЛЬНОГО СПРАЙТА ИЗ ЛИСТА ПО УКАЗАННОМУ ПРЯМОУГОЛЬНИКУ
    def image_at(self, rectangle, color_key=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)
        return image

    # ПОЛУЧАЕМ ОТДЕЛЬНЫЙ СПИСОК ИЗОБРАЖЕНИЙ СПРАЙТОВ ПО СПИСКУ ПРЯМОУГОЛЬНИКВ
    def images_at(self, rects, color_key=None):
        return [self.image_at(rect, color_key) for rect in rects]

    # МЕТОД КОТОРЫЙ ЗАГРУЖАЕТ ПОСЛЕДОВАТЕЛЬНОСТЬ СПРАЙТОВ ИЗ ЛИСТА
    def load_strip(self, rect, image_count, color_key=None):
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, color_key)


# КЛАСС ОТДЕЛЬНОГО СПРАЙТА
class Sprite(object):
    def __init__(self, filename, rect, count, color_key=None, frames=1):
        self.filename = filename
        ss = SpriteSheet(f"./images/sprites/{filename}")
        self.images = ss.load_strip(rect, count, color_key)
        self.i = 0
        self.frames = frames
        self.frame_num = frames

    # МЕТОД ДЛЯ ПЕРЕКЛЮЧЕНИЯ КАДРОВ АНИМАЦИИ
    def next(self):
        if self.frame_num == 0:
            self.i = (self.i + 1) % len(self.images)
            self.frame_num = self.frames
        else:
            self.frame_num -= 1
        return self.images[self.i]
