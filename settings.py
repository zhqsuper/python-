# 配置信息类
class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船相关配置
        # self.ship_speed = 4.5
        self.ship_limit = 3

        # 子弹相关信息
        # self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # ==========新增自动发射冷却==========
        self.fire_cd = 250  # 发射间隔，单位毫秒；250=0.25秒一发，数值越大越慢

        # 外星人配置
        # self.aliens_speed = 1  # 每次水平移动1
        self.fleet_drop_speed = 10  # 每次向下移动的距离为10像素
        # self.fleet_direction = 1  # 1代表右移  -1代表左移

        self.initialize_dynamic_settings()

        # 加速度的倍数
        self.speedup_scale = 1.1
        self.score_scale = 1.5  # 每次过关成绩增长50%

    # 加速
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.aliens_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    # 恢复初始的速度
    def initialize_dynamic_settings(self):
        self.ship_speed = 4.5
        self.bullet_speed = 3.0
        self.aliens_speed = 1  # 每次水平移动1
        self.fleet_direction = 1  # 1代表右移  -1代表左移

        self.alien_points = 50  # 击落一个外星人得50分
