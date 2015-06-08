# projectile class

import cocos
from cocos import sprite
from cocos import actions
from cocos.actions import *
import math
from math import sqrt
import pyglet
from pyglet import clock
import pyfense_resources


class PyFenseProjectile(sprite.Sprite, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self, towerParent, target, velocity, damage):
        projectilePng = pyfense_resources.projectile
        super().__init__(projectilePng, position=towerParent.position,
                         scale=0.3)
        self.moveVel(self, target, velocity)
        self.damage = damage
        clock.schedule_once(self.dispatchHitEvent, self.duration, target)

        # Dispatch event, when enemy is hit
    def dispatchHitEvent(self, dt, target):
        self.dispatch_event('on_enemy_hit', self, target)

    # Move to position of target with certain velocity
    def moveVel(self, projectile, target, velocity):
        dist = self.distance(target.position, self.position)
        self.duration = dist/velocity
        projectile.do(MoveTo(target.position, self.duration))

    def distance(self, a, b):
        return math.sqrt((b[0] - a[0])**2 + (b[1]-a[1])**2)

PyFenseProjectile.register_event_type('on_enemy_hit')