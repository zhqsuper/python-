import pygame

from ship import Ship


# 积计分面板
class Scoreboard:
    def __init__(self, ai_game) -> None:
        self.ai_game = ai_game  # 保存游戏主体对象，实例化飞船使用
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font(None, 48)
        # 将得分从文字的形式转为图片
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    # 最高分转为图片
    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        # 1.图片-内容
        self.high_score_image = self.font.render(
            high_score_str,
            True,
            self.text_color,
            self.settings.bg_color,  # 具体内容
        )
        # 2.图片-rect对象
        self.high_score_rect = self.high_score_image.get_rect()
        # 3.定位
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    # 将得分从文字的形式转为图片
    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        # 1.图片-内容
        self.score_image = self.font.render(
            score_str,
            True,
            self.text_color,
            self.settings.bg_color,  # 具体内容
        )
        # 2.图片-rect对象
        self.score_rect = self.score_image.get_rect()
        # 3.定位
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    # 战斗等级转为图片
    def prep_level(self):
        level_str = str(self.stats.level)
        # 1.图片-内容
        self.level_image = self.font.render(
            level_str,
            True,
            self.text_color,
            self.settings.bg_color,  # 具体内容
        )
        # 2.图片-rect对象
        self.level_rect = self.level_image.get_rect()
        # 3.定位
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 20

    # 准备飞船组
    def prep_ships(self):
        # BUG:cuowu
        self.ships = pygame.sprite.Group()
        for ship_num in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_num * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    # 画到屏幕对象上
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
