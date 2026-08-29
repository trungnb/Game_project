# Complete your game here
import pygame
import random

class MyGame:
    highest_scores = 0

    def highest(self):
        if self.scores > MyGame.highest_scores:
            MyGame.highest_scores = self.scores

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1600,900))
        self.clock= pygame.time.Clock()
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.scores = 0
        pygame.display.set_caption("My Game")

        self.load_images()
        self.new_game()
        self.main_loop()

    def load_images(self):
        self.images = {}
        for name in ["coin", "door", "monster", "robot"]:
            self.images[name] = pygame.image.load(name + ".png")
    
    def new_game(self):
        self.robot = self.spawn_robot()
        self.door = self.spawn_door()
        self.coin_list = [] 
        for i in range(random.randint(3,6)):
            self.coin_list.append(self.spawn_coin())
        self.monster_list = []
        for i in range(random.randint(6,9)):
            self.monster_list.append(self.spawn_monster())

    def spawn_robot(self):
        x,y = random.choice([(0,0),(1600 - self.images["robot"].get_width(),0),(0,900 - self.images["robot"].get_height()),(1600 - self.images["robot"].get_width(), 900 - self.images["robot"].get_height())])
        return Robot(x,y,self.images["robot"])

    def spawn_door(self):
        if self.robot.x == 0 and self.robot.y == 0:
            (x,y) = (1600 - self.images["door"].get_width(), 900 - self.images["door"].get_height())
        elif self.robot.x == 0 and self.robot.y != 0:
            (x,y) = (1600 - self.images["door"].get_width(), 0)
        elif self.robot.x != 0 and self.robot.y == 0:
            (x,y) = (0, 900 - self.images["door"].get_height())
        else:
            (x,y) = (0,0)
        return Door(x,y,self.images["door"])

    def spawn_coin(self):
        x = random.randint(0, 1600 - self.images["coin"].get_width())
        y = random.randint(0, 900 - self.images["coin"].get_height())
        return Coin(x,y, self.images["coin"])
        
    def spawn_monster(self):
        x = random.randint(0, 1600 - self.images["monster"].get_width())
        y = random.randint(0, 900 - self.images["monster"].get_height())
        return Monster(x, y, self.images["monster"])

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            if self.reached_door():
                self.new_game()  

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.robot.command(event)

    def draw_window(self):
        
        self.window.fill((128,128,128))

        self.window.blit(self.door.image, (self.door.x, self.door.y))
        self.window.blit(self.robot.image, (self.robot.x, self.robot.y)) 
        self.robot.move()

        for coin in self.coin_list:
            self.window.blit(coin.image, (coin.x, coin.y))
            if self.get_coin(coin):
                self.scores += 1
                self.coin_list.remove(coin)
        for monster in self.monster_list:
            monster.move()
            self.window.blit(monster.image, (monster.x, monster.y))
            if self.died(monster):
                self.highest()
                self.scores = 0
                self.new_game()

        game_score = self.game_font.render(f"Points: {self.scores}", True, (0,0,0))
        high_score = self.game_font.render(f"Highest Points: {MyGame.highest_scores}", True, (0,0,0))
        introduction = self.game_font.render(f"Dodge monsters, grab coins, and make it to the door!", True, (0,0,0))
        self.window.blit(high_score, (1000,0))
        self.window.blit(game_score, (1400,0))
        self.window.blit(introduction, (200,0))

        pygame.display.flip()

        self.clock.tick(60)

    def get_coin(self,coin):
        return max(coin.x, self.robot.x) <= min(coin.x+coin.width, self.robot.x + self.robot.width) and max(coin.y, self.robot.y) <= min(coin.y+ coin.height, self.robot.y + self.robot.height)

    def died(self, monster):
        return max(monster.x, self.robot.x) <= min(monster.x+monster.width, self.robot.x + self.robot.width) and max(monster.y, self.robot.y) <= min(monster.y+ monster.height, self.robot.y + self.robot.height)
    
    def reached_door(self):
        return max(self.door.x, self.robot.x) <= min(self.door.x+self.door.width, self.robot.x + self.robot.width) and max(self.door.y, self.robot.y) <= min(self.door.y+ self.door.height, self.robot.y + self.robot.height)
        
    
class Robot:
    def __init__(self, x: int, y: int, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.up = False
        self.down = False
        self.right = False
        self.left = False

    def command(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.up = True
            if event.key == pygame.K_DOWN:
                self.down = True
            if event.key == pygame.K_RIGHT:
                self.right = True
            if event.key == pygame.K_LEFT:
                self.left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.up = False
            if event.key == pygame.K_DOWN:
                self.down = False
            if event.key == pygame.K_RIGHT:
                self.right = False
            if event.key == pygame.K_LEFT:
                self.left = False

    def move(self):
        if self.right and self.x + self.width <= 1600:
            self.x += 3
        if self.left and self.x >= 2:
            self.x -= 3
        if self.up and self.y >= 2:
            self.y -= 3
        if self.down and self.y + self.height <= 900:
            self.y += 3



class Monster:
    def __init__(self, x: int, y: int, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = random.randint(2,4)
        self.horizontal = 1
        self.vertical = 1
        self.movement = random.choice([self.fall, self.run, self.bounce])

    def move(self):
        self.movement()
    
    def fall(self):
        self.y += self.vertical * self.speed
        self.check()

    def run(self):
        self.x += self.horizontal * self.speed
        self.check()

    def bounce(self):
        self.x += self.horizontal * self.speed
        self.y += self.vertical * self.speed
        self.check()

    def check(self):
        if self.x <= 0 or self.x + self.width >= 1600:
            self.horizontal = - self.horizontal
        if self.y <= 0  or self.y + self.height >= 900:
            self.vertical = - self.vertical


class Door:
    def __init__(self, x: int, y: int, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()


class Coin:
    def __init__(self, x: int, y: int, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        
if __name__ == "__main__":
    MyGame()