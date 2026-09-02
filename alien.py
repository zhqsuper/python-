import pygame
from pygame.sprite import Sprite


# 外星人类,继承Sprite类
class Alien(Sprite):
    def __init__(self, ai_game, alien_x=0, alien_y=0):
        super().__init__()
        # 获取屏幕对象
        self.screen = ai_game.screen
        # 获取屏幕对象的尺寸坐标信息(rect对象)
        self.screen_rect = ai_game.screen.get_rect()
        # 获取配置信息对象
        self.settings = ai_game.settings

        # 外星人图像和尺寸信息
        self.image = pygame.image.load("./images/alien_64.bmp")
        self.rect = self.image.get_rect()

        # 定位
        self.rect.x = alien_x
        self.rect.y = alien_y

    # 更新移动外星人
    def update(self, is_move_down=False):
        if is_move_down:
            self.rect.y += self.settings.fleet_drop_speed
        self.rect.x += self.settings.aliens_speed * self.settings.fleet_direction

    # 检查外星人是否超出边界
    def check_edges(self):
        return (self.rect.left < 0) or (self.rect.right > self.screen_rect.right)
