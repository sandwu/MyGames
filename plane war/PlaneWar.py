import pygame
from pygame.locals import *
import sys
import time
import random

enemyplane_list = []
score = 0
is_restart = False
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 512

class Item:
    window = None
    def __init__(self, image, x, y):
        self.img = pygame.image.load(image)
        self.x = x
        self.y = y
        # self.window = window

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

class Map(Item):
    def __init__(self, img_path):
        self.x = 0
        self.bg_img1 = pygame.image.load(img_path)
        self.bg_img2 = pygame.image.load(img_path)
        self.bg1_y = - 768
        self.bg2_y = 0

    def move(self):
        # 当地图1的 y轴移动到0，则重置
        if self.bg1_y >= 0:
            self.bg1_y = - 768

        # 当地图2的 y轴移动到 窗口底部，则重置
        if self.bg2_y >= 768:
            self.bg2_y = 0

        # 每次循环都移动1个像素
        self.bg1_y += 3
        self.bg2_y += 3

    def display(self):
        """贴图"""
        self.window.blit(self.bg_img1, (self.x, self.bg1_y))
        self.window.blit(self.bg_img2, (self.x, self.bg2_y))

class BasePlane(Item):
    pass

class EnemyPlane(BasePlane):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.is_hited = False

    def display(self):
        super().display()
        if self.is_hited:
            self.x = random.randint(0, 412)
            self.y = random.randint(-300, -68)
            self.is_hited = False
        self.window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += 10
        #回调敌机
        if self.y >= 768:
            self.y = random.randint(-300, -68)
            self.x = random.randint(0, 412)
            self.img = pygame.image.load("res/img-plane_%d.png" % random.randint(1, 7))

    def plane_down_anim(self):
        """敌机被击中动画"""
        if self.anim_index >= 21:  # 动画执行完
            self.anim_index = 0
            self.img = pygame.image.load("res/img-plane_%d.png" % random.randint(1, 7))
            self.x = random.randint(0, WINDOW_WIDTH - 100)
            self.y = 0
            self.is_hited = False
            return
        elif self.anim_index == 0:
            self.hit_sound.play()
        self.img = pygame.image.load("res/bomb-%d.png" % (self.anim_index // 3 + 1))
        self.anim_index += 1


class HeroBullet(Item):
    def move(self):
        self.y -= 10

    #判断是否交叉
    def is_hit_enemy(self, enemy):
        if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, 20, 29),
                                   pygame.Rect(enemy.x, enemy.y, 100, 68)):
            return True
        else:
            return False

class HeroPlane(BasePlane):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.bullets = []
        self.is_hited = False
        self.is_anim_down = False
        self.anim_index = 0

    def display(self):
        """贴图"""
        super().display()
        for enemy in enemyplane_list:
            if self.is_hit_enemy(enemy):
                enemy.is_hited = True
                self.is_hited = True
                self.plane_down_anim()
                break

    def plane_down_anim(self):
        """敌机被击中动画"""
        if self.anim_index >= 1:  # 动画执行完
            self.is_hited = False
            self.is_anim_down = True
            return

        self.img = pygame.image.load("res/bomb-%d.png" % (self.anim_index // 3 + 1))
        self.anim_index += 1

    def is_hit_enemy(self, enemy):
        if pygame.Rect.colliderect(
            pygame.Rect(self.x, self.y, 120, 68),
            pygame.Rect(enemy.x, enemy.y, 100, 48)
        ):  # 判断是否交叉
            return True
        else:
            return False

    def left_move(self):
        if self.x > 0:
            self.x -= 10

    def right_move(self):
        if self.x <= 392:
            self.x += 10

    def up_move(self):
        if self.y > 0:
            self.y -= 10

    def down_move(self):
        if self.y <= 690:
            self.y += 10

    def fire(self):
        bullet = HeroBullet("res/bullet_13.png", self.x+50, self.y-29)
        self.bullets.append(bullet)

    def delete_bullet(self):
        temp_list = []

        for bullet in self.bullets:
            if bullet.y > -29:
                bullet.display()
                bullet.move()
                for enemy in enemyplane_list:
                    if bullet.is_hit_enemy(enemy):
                        enemy.is_hited = True
                        temp_list.append(bullet)
                        global score
                        score += 10
                        break
            # 多余子弹删除
            else:
                temp_list.append(bullet)
        # if len(temp_list) > 0:
        for temp in temp_list:
            # print("子弹删除了")
            self.bullets.remove(temp)


class Game:
    def __init__(self):
        #初始化，为防止加载音乐等出现异常
        pygame.init()
        #加载背景音乐
        # pygame.mixer.init()
        pygame.mixer.music.load("res/bg2.ogg")
        # 循环播放背景音乐
        self.gameover_sound = pygame.mixer.Sound("res/gameover.wav")
        pygame.mixer.music.play(-1)
        #设置窗口
        self.window = pygame.display.set_mode((512, 768))
        Item.window = self.window
        pygame.display.set_caption("专属飞机大战")
        # image = pygame.image.load("res/img_bg_level_2.jpg")
        self.map = Map("res/img_bg_level_2.jpg")
        self.heroplane = HeroPlane("res/hero2.png", 196, 550)
        for i in range(5):
            self.enemyplane = EnemyPlane("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, 412),
                                    random.randint(-200, -68))
            enemyplane_list.append(self.enemyplane)
        # 创建文字对象
        self.score_font = pygame.font.Font("res/SIMHEI.TTF", 40)

    def draw_text(self, content, size, x, y):
        # font_obj = pygame.font.SysFont("simhei", size)
        font_obj = pygame.font.Font("res/SIMHEI.TTF", size)
        text = font_obj.render(content, 1, (255, 255, 255))
        self.window.blit(text, (x, y))

    def wait_game_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                        pygame.quit()
                    elif event.key == K_RETURN:
                        global is_restart, score
                        is_restart = True
                        score = 0
                        return

    def game_start(self):
        # 贴背景图片
        self.map.display()
        self.draw_text("飞机大战", 40, WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 3)
        self.draw_text("按下enter开始游戏, Esc退出游戏.", 28, WINDOW_WIDTH / 3 - 140, WINDOW_HEIGHT / 2)
        pygame.display.update()
        self.wait_game_input()

    def game_over(self):
        # 先停止背景音乐
        pygame.mixer.music.stop()
        # 再播放音效
        self.gameover_sound.play()
        # 贴背景图片
        self.map.display()
        self.draw_text("战机被击落,得分为 %d" % score, 28, WINDOW_WIDTH / 3 - 100, WINDOW_HEIGHT / 3)
        self.draw_text("按下enter开始游戏, Esc退出游戏.", 28, WINDOW_WIDTH / 3 - 140, WINDOW_HEIGHT / 2)
        pygame.display.update()
        self.wait_game_input()
        self.gameover_sound.stop()

    def run(self):
        if not is_restart:
            self.game_start()
        while True:
            #背景贴图
            # window.blit(image, (0, 0))
            self.map.display()
            self.map.move()
            #飞机贴图
            self.heroplane.display()
            if self.heroplane.is_anim_down:
                self.heroplane.is_anim_down = False
                global enemyplane_list
                enemyplane_list = []
                break
            #子弹贴图
            self.heroplane.delete_bullet()
            # for bullet in heroplane.bullets:
            #     bullet.display()
            #     bullet.move()
            #     #多余子弹删除
            #     temp_list = []
            #     if bullet.y < -29:
            #         temp_list.append(bullet)
            #     for temp in temp_list:
            #         print("子弹删除了")
            #         heroplane.bullets.remove(temp)
            #敌机贴图
            for enemyplane in enemyplane_list:
                enemyplane.display()
                if not enemyplane.is_hited:
                    enemyplane.move()
            # 贴得分文字
            score_text = self.score_font.render("得分:%d" % score, 1, (255, 255, 255))
            self.window.blit(score_text, (10, 10))
            #统一刷新
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                    pygame.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.heroplane.fire()

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_a] or pressed_keys[K_LEFT]:
                self.heroplane.left_move()
            if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
                self.heroplane.right_move()
            if pressed_keys[K_w] or pressed_keys[K_UP]:
                self.heroplane.up_move()
            if pressed_keys[K_s] or pressed_keys[K_DOWN]:
                self.heroplane.down_move()

            time.sleep(0.01)
        self.game_over()

def main():
    """主函数  一般将程序的入口"""
    # 运行游戏
    while True:
        # 创建游戏对象
        game = Game()
        game.run()

if __name__ == '__main__':
    main()