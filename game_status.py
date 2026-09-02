# 游戏信息统计类
class GameStatus:

    def __init__(self, ai_game):
        # 获取配置信息对象
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.__ships_left = 0  # 飞船剩余数量
        self.reset_stats()
        self.__high_score = 0  # 最高分

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        # self.bullets_left = self.settings.bullets_limit
        self.__score = 0  # 得分
        self.level = 1

    @property  # 当在外面访问stats.ships_left时触发
    def ships_left(self):
        return self.__ships_left

    @ships_left.setter  # 当给stats.ships_left赋值时触发
    def ships_left(self, new_val):
        self.__ships_left = new_val
        if hasattr(self.ai_game, "sb"):
            self.ai_game.sb.prep_ships()
        # try:
        #     self.ai_game.sb.prep_ships()
        # except:
        #     print("pass")

    @property
    def high_score(self):
        return self.__high_score

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, new_val):
        self.sb.prep_score()  # type: ignore[reportArgumentType]
        self.__score = new_val
        if new_val > self.__high_score:
            self.__high_score = new_val
            self.sb.prep_high_score()  # type: ignore[reportArgumentType]
