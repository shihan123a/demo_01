#!/usr/bin/env python
# -*- coding:utf-8 -*-
class GameStats():
    """追踪外星入侵的统计数据"""

    def __init__(self, ai_settings):
        """初始化信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # 在非活动状态下开始游戏。
        self.game_active = False

        # 高分不应重置。
        self.high_score = 0

    def reset_stats(self):
        """初始化可以在游戏期间更改的统计信息。"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1