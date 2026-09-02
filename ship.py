import pygame
from pygame.sprite import Sprite


class BaseSprite(Sprite):
    # """自己封装的基类，专门解决Pylance误报"""
    def __init__(self):
        super().__init__()
        # 在这里一次性告诉Pylance允许动态增加任意实例属性
        self.__dict__: dict


# 飞船类
class Ship(BaseSprite):
    # ai_game 是实例时要传的 游戏主体对象
    def __init__(self, ai_game):
        super().__init__()
        # 获取屏幕对象
        self.screen = ai_game.screen
        # 获取屏幕对象的尺寸坐标信息(rect对象)
        self.screen_rect = ai_game.screen.get_rect()
        # 获取配置信息对象
        self.settings = ai_game.settings

        # 飞船+图像
        self.image = pygame.image.load("./images/plane_80.png")
        # 飞船-尺寸坐标
        self.rect = self.image.get_rect()

        # 飞船定位到屏幕底部中英位置
        self.center_ship()

        # 给飞船设置移动标志位
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    # 根据不同的标志位状态,进行移动
    def update(self):
        if self.moving_left and self.rect.left >= 0:
            self.rect.left -= self.settings.ship_speed  # 持续向左移动
        if self.moving_right and self.rect.right <= self.screen_rect.right:
            self.rect.right += self.settings.ship_speed  # 持续向右移动
        if self.moving_up and self.rect.top >= 0:
            self.rect.top -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.rect.bottom += self.settings.ship_speed

    # 飞船定位到屏幕底部中英位置
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom

    # 将飞船画到屏幕对象上
    def blitme(self):
        self.screen.blit(self.image, self.rect)
