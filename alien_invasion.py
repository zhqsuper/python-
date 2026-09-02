import sys
import time

import pygame

from alien import Alien
from bullet import Bullet
from button import BUtton
from game_status import GameStatus
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


# 游戏主体对象
class AlienInvasion:
    def __init__(self):
        pygame.init()  # 初始化 pygame 模块
        self.settings = Settings()
        # 设置屏幕尺寸,并且保存返回的屏幕对象
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # 改变全屏
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        # 设置标题
        pygame.display.set_caption("外星人入侵!")
        # 时钟对象
        self.clock = pygame.time.Clock()
        # 创建飞船对象
        self.ship = Ship(self)
        # 创建子弹组
        self.bullets = pygame.sprite.Group()
        # 创建外星人组
        self.aliens = pygame.sprite.Group()

        # 创建外星人舰队
        self._creat_fleet()

        # 实例化游戏统计信息类
        self.stats = GameStatus(self)

        # 游戏是否为激活状态
        self.game_active = False
        self.play_button = BUtton(self, "Play")

        # 实例化积分榜对象
        self.sb = Scoreboard(self)
        self.stats.sb = self.sb  # type: ignore[reportArgumentType]

        # ==========新增自动发射冷却==========
        self.last_fire_time = 0  # 上一次发射子弹的时间戳

    # 创建外星人舰队
    def _creat_fleet(self):
        # 获取外星人宽高
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                new_alien = Alien(self, current_x, current_y)
                self.aliens.add(new_alien)
                # 下个外星人坐标
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    # 让整个舰队进行移动更新
    def _update_fleet(self):
        is_out_of_bounds = self._check_fleet_edges()
        if is_out_of_bounds:
            self.settings.fleet_direction *= -1
        self.aliens.update(is_out_of_bounds)
        # 外星人与飞船碰撞处理
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  # type: ignore[reportArgumentType]
            self._reset_game()

        # 外星人是否到达底部
        self._check_aliens_bottom()

    # 外星人是否到达底部
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom > self.settings.screen_height:
                self._reset_game()
                break

    # 重置游戏场景
    def _reset_game(self):
        # 玩家可用飞船-1
        self.stats.ships_left -= 1
        if self.stats.ships_left > 0:
            # 清空子弹和外星人
            self.aliens.empty()
            self.bullets.empty()
            # 重新创建
            self._creat_fleet()
            self.ship.center_ship()
            # 暂停0.5s
            time.sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    # 检查整个舰队是否超出边界
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                return True
        return False

    # 封装发射子弹方法
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet = Bullet(self)
            self.bullets.add(bullet)

    # 新增：自动发射，带冷却判断
    def _auto_fire(self):
        current_time = pygame.time.get_ticks()  # 获取程序运行总毫秒数
        # 当前时间 - 上次发射时间 >= 冷却时间，才允许发射
        if current_time - self.last_fire_time >= self.settings.fire_cd:
            self._fire_bullet()
            self.last_fire_time = current_time  # 更新上次发射时间

    # 子弹移动方法
    def _update_bullets(self):
        self.bullets.update()
        # 检查子弹与外星人的碰撞情况
        self._check_bullet_alien()

    # 检查子弹与外星人的碰撞情况
    def _check_bullet_alien(self):
        # 检查两个组之间的碰撞情况
        # 参数1 self.bullets 子弹组
        # 参数2 self.aliens  外星人组
        # 参数3 True        碰撞后 删除相应的子弹
        # 参数4 True      碰撞后 删除相应的外星人
        # 返回值 collisions  是一个字典
        # 键: 某个子弹
        # 值: 被该子弹击中的目标列表(只有一个外星人时, 也是列表形式)
        # pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)
        collisions = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            # 统计得分后生成计分板图片
            # self.sb.prep_score()
            # self.sb.prep_high_score()
        # 如果外星人被清空
        if not self.aliens:
            self.bullets.empty()
            self._creat_fleet()
            self.ship.center_ship()
            # 提速
            self.settings.increase_speed()
            self.stats.level += 1  # 等级加1
            self.sb.prep_level()  # 重绘等级图片

    # 提取封装键盘-按下的代码
    def _check_keydown_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        # elif event.key == pygame.K_SPACE:
        #     self._fire_bullet()

    # 提取封装键盘-抬起的代码
    def _check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    # 单独提取_事件处理方法
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标点击的坐标
                mouse_pos = pygame.mouse.get_pos()
                # 检查鼠标点击按钮
                self.check_play_button(mouse_pos)

    def check_play_button(self, mouse_pos):
        button_checked = self.play_button.rect.collidepoint(mouse_pos)
        if button_checked and not self.game_active:
            # 初始化统计信息
            self.stats.reset_stats()
            self.game_active = True

            # 清空子弹和外星人
            self.aliens.empty()
            self.bullets.empty()

            # 重新创建
            self._creat_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

            # 恢复初始的速度
            self.settings.initialize_dynamic_settings()
            # 得分清0
            self.sb.prep_score()
            # self.stats.level = 1  # 等级1
            self.sb.prep_level()  # 重绘等级图片

    # 单独提取_屏幕重绘与刷新
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)  # 背景填充色
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()  # 画到屏幕上
        self.aliens.draw(self.screen)
        if not self.game_active:
            self.play_button.draw_button()
        self.sb.show_score()
        pygame.display.flip()  # 刷新

    # 真正运行游戏是要调用的方法
    def run_game(self):
        while True:
            # 第一部分:事件处理
            self._check_events()
            # 第二部分:位置,数量修改更新,碰撞检测
            if self.game_active:
                self.ship.update()

                # =====替换原来直接调用_fire_bullet()，调用带冷却的自动开火=====
                self._auto_fire()

                self._update_bullets()  # 让子弹移动起来

                self._update_fleet()  # 外星人动起来

            # 第三部分:重新绘制屏幕,并刷新
            self._update_screen()

            # 如果当前循环比较快,少于1/60秒,就等到1/60后在进入下一次循环
            self.clock.tick(60)


if __name__ == "__main__":
    alien = AlienInvasion()
    alien.run_game()
