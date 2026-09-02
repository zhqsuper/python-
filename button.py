import pygame


class BUtton:
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 按钮相关信息
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 48)

        # 生成按钮的rect对象，并定位屏幕中心
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 准备-文字图片
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # 1.文字图片-内容
        self.msg_image = self.font.render(
            msg,
            True,
            self.text_color,
            self.button_color,  # 具体内容
        )
        # 2.文字图片-rect对象
        self.msg_image_rect = self.msg_image.get_rect()
        # 3.定位
        self.msg_image_rect.center = self.rect.center

    # 绘画到屏幕上
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
