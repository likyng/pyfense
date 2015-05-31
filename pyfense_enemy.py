# pyfense_enemy.py
# contains PyFenseEnemy class
import cocos
import pyglet
from cocos import sprite
from cocos import actions
from pyglet.image.codecs.png import PNGImageDecoder


class PyFenseEnemy(sprite.Sprite):
    def __init__(self, lvl, wave):
        # TODO: Different assets and values for stronger enemies to be loaded from textfile
        self.currentPos = (0, 340) 
        image = pyglet.image.load("assets/enemy1.png", decoder=PNGImageDecoder())
        super(PyFenseEnemy, self).__init__(image, position = self.currentPos)
        self.healthPoints = 40
        #self.drawHealthBar()
        self.speed = 10
        self.reward = 20
        self.damage = 1
        self.worth = 5
        self.move(lvl)

    movePathlvl1 = (actions.MoveBy((195, 0)) + actions.MoveBy((0, 230))
                    + actions.MoveBy((230, 0)) + actions.MoveBy((0, -300))
                    + actions.MoveBy((300, 0)) + actions.MoveBy((0, 130))
                    + actions.MoveBy((400, 0), 3))

    def move(self, lvl):
        self.do(self.movePathlvl1)
        
    def drawHealthBar(self):
        (x, y) = self.position
        bar_x = x - self.width / 2 
        bar_y = y + self.height / 2 + 20
        #print("barx: " + str(bar_x) + ", bary: " + str(bar_y))
        self.healthBar = cocos.draw.Line((bar_x, bar_y), (bar_x + self.healthPoints, bar_y), (123, 123, 123, 123), 15)
        return self.healthBar
