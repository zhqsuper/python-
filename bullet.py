import pygame
from pygame.sprite import Sprite


# 子弹类,继承Sprite类
class Bullet(Sprite):

    def __init__(self, ai_game):
        super().__init__()  # 父类2初始化方法
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # 创建子弹的rect对象
        self.rect = pygame.Rect(
            0,  # x轴的值
            0,  # y轴的值
            self.settings.bullet_width,
            self.settings.bullet_height,
        )
        # 子弹定位
        self.rect.midtop = ai_game.ship.rect.midtop

    # 子弹画到屏幕对象上
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    # 让子弹移动
    def update(self):
        self.rect.bottom -= self.settings.bullet_speed
        if self.rect.bottom < 0:
            self.kill()
