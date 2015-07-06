"""
Move projectile to target and dispatch event on_target_hit.
"""

from cocos import sprite
from cocos import actions
import math
import pyglet


class PyFenseProjectile(sprite.Sprite, pyglet.event.EventDispatcher):
    """
    Cocos Sprite that moves to the target and dispatches event on_target_hit.
    """
    
    is_event_handler = True
    
    def __init__(
            self, towerParent, target, image, towerNumber, rotation,
            velocity, damage, effect, effectduration, effectfactor):
        """
        Create a projectile.
        
        :Parameters:
            `towerParent`: tower object
                Tower that launched the projectile.
            `target` : enemy object
                Enemy that is targeted.
            `image` : image.
                Image of the projectile.
            `towerNumber` : int
                Number of the parent tower. 
            `rotation` : int
                Rotation of the parent tower.
            `velocity` : int
                Velocity of the projectile.
            `damage` : int
                Damage the projectile causes.
            `effect` : string
                Effect that is caused by projectile (like poison or normal)
            `effectduration` : int
                Duration that the effect is active.
            `effectfactor` : int
                How strong the effect is.
        """
                
        super().__init__(image, position=towerParent.position,
                         scale=1)
        self.rotation = rotation
        self.damage = damage
        self.velocity = velocity
        self.distance = self._distance(target.position, self.position)
        self.duration = self._duration()
        self.do(actions.MoveTo(target.position, self.duration))
        self.schedule_interval(
            self._dispatch_hit_event, self.duration, target, towerNumber,
            effect, effectduration, effectfactor)

    def _dispatch_hit_event(self, dt, target, towerNumber, effect,
                         effectduration, effectfactor):
        """
        Dispatch event when enemy is hit.
        The event is then handled by the enitites class in order to subtract
        health points from the enemy and to handle the different effects. 
        """

        self.unschedule(self._dispatch_hit_event)     
        self.dispatch_event('on_target_hit', self, target, towerNumber,
                            effect, effectduration, effectfactor)

    def _duration(self):
        """
        Compute duration, that the projectile flies.
        """
        dur = self.distance/self.velocity
        return dur

    def _distance(self, a, b):
        """
        Compute distance between two tupels (= position).
        """
        dis = math.sqrt((b[0] - a[0])**2 + (b[1]-a[1])**2)
        return dis

PyFenseProjectile.register_event_type('on_target_hit')
